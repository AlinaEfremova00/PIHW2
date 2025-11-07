from transformers import pipeline

# создаём классификатор тональности
classifier = pipeline("sentiment-analysis")

def analyze_text(text: str):
    # text: str
    prediction = classifier(text)[0]  # pipeline возвращает список словарей
    return prediction
