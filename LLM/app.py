from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()
MODEL_NAME = "qwen3:0.6b"

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME],
            input=request.prompt,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при вызове модели:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return {"response": result.stdout.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при вызове модели: {str(e)}")
