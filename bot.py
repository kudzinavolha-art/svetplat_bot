import os
import requests
from time import sleep

API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{API_TOKEN}"
ADD_NUMBER = 2933
offset = 0

def get_updates(offset):
    url = f"{BASE_URL}/getUpdates?timeout=100&offset={offset}"
    response = requests.get(url)
    return response.json()

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

print("Бот запущен. Ожидание сообщений...")

while True:
    try:
        updates = get_updates(offset)
        for update in updates.get("result", []):
            offset = update["update_id"] + 1
            message = update.get("message")
            if message is None:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text == "/start":
                send_message(chat_id, f"Привет! Отправь мне число, и я прибавлю к нему {ADD_NUMBER} 🙂")
                continue

            try:
                num = float(text)
                result = num + ADD_NUMBER
                send_message(chat_id, f"{num} + {ADD_NUMBER} = {result}")
            except ValueError:
                send_message(chat_id, "Отправь число, пожалуйста 🤓")
    except Exception as e:
        print(f"Ошибка: {e}")
        sleep(1)
