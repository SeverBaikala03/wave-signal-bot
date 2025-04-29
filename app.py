from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400

    symbol = data.get("symbol")
    entry = data.get("entry")
    stop = data.get("stop")
    take = data.get("take")
    tf = data.get("tf")
    direction = data.get("direction")
    source = data.get("source", "WaveRSI")

    direction_emoji = "🟢" if direction == "LONG" else "🔴"
    msg = (
        f"{direction_emoji} Новый сигнал ({direction})\n"
        f"Источник: {source}\n"
        f"Актив: {symbol}\n"
        f"Цена входа: {entry}\n"
        f"Стоп-лосс: {stop}\n"
        f"Тейк-профит: {take}\n"
        f"Таймфрейм: {tf}"
    )

    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": msg}
        requests.post(url, json=payload)

    return jsonify({"ok": True})

# Пинг-маршрут для UptimeRobot
@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

if __name__ == "__main__":
    app.run()
