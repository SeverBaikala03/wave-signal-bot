import os
from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route('/', methods=['POST'])
def receive_signal():
    data = request.json
    if not data:
        return "No data", 400

    try:
        symbol = data.get("symbol", "N/A")
        entry = round(float(data.get("entry", 0)), 2)
        stop = round(float(data.get("stop", 0)), 2)
        take = round(float(data.get("take", 0)), 2)
        tf = data.get("tf", "N/A")
        direction = data.get("direction", "N/A")

        msg = f"🟢 Новый сигнал ({direction})\n" \
              f"Актив: {symbol}\n" \
              f"Цена входа: {entry}\n" \
              f"Стоп-лосс: {stop}\n" \
              f"Тейк-профит: {take}\n" \
              f"Таймфрейм: {tf}"

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": msg
        }

        requests.post(url, json=payload)
        return "Message sent", 200

    except Exception as e:
        return str(e), 500
