from app import chat, ChatRequest


def test_intelligence():
    prompts = [
        "Что будет, если смешать синий и жёлтый цвет?",
        "Реши пример: 7 * 8",
        "Напиши короткий рассказ про кота, который путешествует во времени"
    ]

    for prompt in prompts:
        response = chat(ChatRequest(prompt=prompt))
        print(f"Prompt: {prompt}\nResponse: {response['response']}\n")


def test_hallucinations():
    prompts = [
        "Расскажи о планете, которая не существует",
        "Составь список событий, которых никогда не было в истории"
    ]

    for prompt in prompts:
        response = chat(ChatRequest(prompt=prompt))
        print(f"Prompt: {prompt}\nResponse: {response['response']}\n")


if __name__ == "__main__":
    print("Тестируем интеллект модели:")
    test_intelligence()
    print("Тестируем склонность к галлюцинациям:")
    test_hallucinations()
