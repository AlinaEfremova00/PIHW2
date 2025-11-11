import requests
import time
import csv
import json
from typing import List, Dict
import os

API_URL = "http://127.0.0.1:8000/chat"

# классификация примитивом
def classify_prompt(prompt: str) -> str:
    p = prompt.lower()
    if any(w in p for w in ["как", "что такое", "кто", "где", "почему", "когда"]):
        return "informational"
    if any(w in p for w in ["напиши", "сгенерируй", "создай", "составь", "придумай"]):
        return "generate"
    if any(w in p for w in ["сделай", "автоматизируй", "выполни"]):
        return "task"
    return "unknown"

# вызов LLM
def call_llm(prompt: str, timeout: int = 60) -> Dict:
    payload = {"prompt": prompt}
    r = requests.post(API_URL, json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()

# эвристика уверенности/галлюцинации
def estimate_confidence(text: str) -> float:
    if not text:
        return 0.0
    low_markers = ["не уверен", "нужно уточнить", "i don't know", "can't", "не знаю"]
    txt = text.lower()
    if any(m in txt for m in low_markers):
        return 0.1
    l = len(text.split())
    return min(0.95, 0.25 + 0.02 * (l**0.5))

def detect_hallucination_by_keywords(text: str) -> bool:
    # если модель уверенно придумывает детали о реальных фактах
    halluc_keywords = ["не подтверждается", "нет данных", "этого не было", "вымышлен"]
    txt = text.lower()
    return any(k in txt for k in halluc_keywords)

def simple_fact_check(prompt: str, model_answer: str, gold_answer: str) -> bool:

    if gold_answer is None:
        return None
    ma = model_answer.lower()
    ga = gold_answer.lower()
    return ga in ma or ma in ga

# основная логика агента
def handle_user(prompt: str, history: List[str] = None, system_instruction: str = None) -> Dict:
    history = history or []
    typ = classify_prompt(prompt)
    system = system_instruction or "Ты — помощник-студент. Отвечай по-русски кратко и ясно. Если не знаешь — скажи 'нужно уточнить'."
    ctx = "\n".join(history[-5:]) if history else ""
    full_prompt = f"{system}\n\nКонтекст:\n{ctx}\n\nПользователь: {prompt}\nОтвет:"
    start = time.time()
    try:
        resp = call_llm(full_prompt)
        elapsed = time.time() - start
        text = resp.get("response", "").strip()
        confidence = estimate_confidence(text)
        halluc = detect_hallucination_by_keywords(text)
        return {"response": text, "confidence": confidence, "hallucination_guess": halluc, "type": typ, "time": elapsed}
    except Exception as e:
        return {"response": f"Ошибка агента: {str(e)}", "confidence": 0.0, "hallucination_guess": False, "type": typ, "time": 0.0}

# принимает JSON с тестами и сохраняет CSV
def run_tests(tests_file: str = "LLM/tests/test_prompts.json",
              out_csv: str = "LLM/tests/results.csv"):

    # проверяем/создаём папку для CSV
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)

    # загружаем тесты
    with open(tests_file, "r", encoding="utf-8") as f:
        tests = json.load(f)

    rows = []
    for t in tests:
        prompt = t["prompt"]
        gold = t.get("gold")
        print(f"Running: {t['id']} — {prompt}")
        res = handle_user(prompt)
        ok = simple_fact_check(prompt, res["response"], gold) if gold else ""
        rows.append({
            "id": t["id"],
            "prompt": prompt,
            "type": t.get("type", ""),
            "gold": gold or "",
            "response": res["response"],
            "confidence": res["confidence"],
            "hallucination_guess": res["hallucination_guess"],
            "fact_ok": ok,
            "time": res["time"]
        })

    # запись CSV
    fieldnames = ["id","prompt","type","gold","response","confidence","hallucination_guess","fact_ok","time"]
    with open(out_csv, "w", newline="", encoding="utf-8") as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved results to {out_csv}")
    return rows

if __name__ == "__main__":
    # локальный быстрый тест
    sample = "Кто написал Войну и мир?"
    print(handle_user(sample))
