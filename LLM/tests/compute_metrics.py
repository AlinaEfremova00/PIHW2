import csv
from collections import Counter

def compute(csv_path="LLM/tests/results.csv"):
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    total = len(rows)
    factual = [r for r in rows if r['type']=='factual']
    facts_total = len(factual)
    facts_ok = sum(1 for r in factual if r['fact_ok'].strip().lower()=='true' or r['fact_ok']=='True' or r['fact_ok']=='1')
    avg_time = sum(float(r['time'] or 0) for r in rows)/total if total else 0
    halluc_guess = sum(1 for r in rows if r['hallucination_guess'].lower()=='true' or r['hallucination_guess']=='True')
    print("Total prompts:", total)
    print("Factual prompts:", facts_total)
    print("Factual accuracy (simple):", f"{facts_ok}/{facts_total}" if facts_total else "N/A")
    print("Avg latency s:", round(avg_time,3))
    print("Hallucination guesses:", halluc_guess)
    return rows

if __name__ == "__main__":
    compute()
