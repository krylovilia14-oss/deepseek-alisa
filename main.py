from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),  # переменная окружения изменена на GROQ_API_KEY
    base_url="https://api.groq.com/openai/v1"  # официальный адрес Groq
)
