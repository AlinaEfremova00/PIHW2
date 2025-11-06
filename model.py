from transformers import pipeline

# Загружаем модель один раз при старте сервера
nlp = pipeline("sentiment-analysis")

def analyze_text(text: str):
    """Анализирует эмоциональную окраску текста."""
    result = nlp(text)[0]
    return {
        "label": result["label"],
        "score": round(result["score"], 3)
    }
