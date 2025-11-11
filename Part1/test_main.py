from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_positive_sentiment():
    response = client.post("/analyze", json={"text": "I love sunny days!"})
    assert response.status_code == 200
    assert response.json()["label"] == "POSITIVE"

def test_negative_sentiment():
    response = client.post("/analyze", json={"text": "I hate everything today."})
    assert response.status_code == 200
    assert response.json()["label"] == "NEGATIVE"

