from fastapi import FastAPI
from pydantic import BaseModel
from model import analyze_text

# Создаём экземпляр приложения
app = FastAPI(
    title="Emotion Detection API",
    description="API для определения эмоциональной окраски текста",
    version="1.0"
)

# Модель данных для запроса
class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze(request: TextRequest):
    """
    Принимает текст и возвращает результат анализа эмоций.
    """
    result = analyze_text(request.text)
    return {
        "input_text": request.text,
        "result": result
    }

@app.get("/")
def root():
    return {"message": "Добро пожаловать в Emotion Detection API!"}
