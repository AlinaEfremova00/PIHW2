from fastapi import FastAPI
from pydantic import BaseModel
from model import analyze_text

app = FastAPI()

class TextItem(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Emotion Detection API!"}

@app.post("/analyze")
def analyze_text_endpoint(item: TextItem):
    result = analyze_text(item.text)
    return result

