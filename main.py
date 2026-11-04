import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/")
async def main(request: Request):
    body = await request.json()
    user_text = body["request"]["original_utterance"]

    # Обработка проверочного запроса ping от Алисы
    if user_text.lower() == "ping":
        return {
            "version": body["version"],
            "session": body["session"],
            "response": {"end_session": False, "text": "pong"}
        }

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": "openai/gpt-oss-120b",
                "messages": [{"role": "user", "content": user_text}],
            },
            timeout=10
        )

        # Отладочный вывод, проверьте в Logs на Render
        print("Groq status:", response.status_code)
        print("Groq body:", response.text[:500])

        if response.status_code != 200:
            answer = "Сервис временно недоступен, попробуйте позже."
        else:
            data = response.json()
            if not data.get("choices"):
                answer = "Не удалось получить ответ, попробуйте ещё раз."
            else:
                answer = data["choices"][0]["message"]["content"]
    except Exception as e:
        print("Exception:", str(e))
        answer = "Произошла ошибка, попробуйте позже."

    return {
        "version": body["version"],
        "session": body["session"],
        "response": {"end_session": False, "text": answer}
    }
