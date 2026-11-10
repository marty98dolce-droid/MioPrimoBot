import os
import requests

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

ASSET = "bitcoin"
FAST_PERIOD = 20
SLOW_PERIOD = 50

def send_telegram_message(message):
    if not TOKEN or not CHAT_ID:
        print("ATTENZIONE: Manca TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID nei Secrets di GitHub!")
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Risposta server Telegram: {response.status_code}")
        print(f"Dettaglio risposta: {response.text}")
    except Exception as e:
        print(f"Errore critico invio Telegram: {e}")

def get_market_data():
    url = f"https://api.coingecko.com/api/v3/coins/{ASSET}/market_chart?vs_currency=eur&days=30"
    try:
        response = requests.get(url)
        data = response.json()
        return [p[1] for p in data['prices']]
    except Exception as e:
        print(f"Errore nel recupero dati: {e}")
        return []

def calculate_moving_average(prices, period):
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def run_strategy():
    print("--- AVVIO ANALISI BOT TRADING ---")
    prices = get_market_data()
    if not prices:
        return

    current_price = prices[-1]
    fast_ma = calculate_moving_average(prices, FAST_PERIOD)
    slow_ma = calculate_moving_average(prices, SLOW_PERIOD)

    if fast_ma > slow_ma:
        msg = f"🚀 *SEGNALE TRADING: BULLISH*\n\nAsset: {ASSET.upper()}\nPrezzo: €{current_price:.2f}\nMedia Veloce: €{fast_ma:.2f}\nMedia Lenta: €{slow_ma:.2f}\n*Stato:* Trend Rialzista 📈"
    else:
        msg = f"🔻 *SEGNALE TRADING: BEARISH*\n\nAsset: {ASSET.upper()}\nPrezzo: €{current_price:.2f}\nMedia Veloce: €{fast_ma:.2f}\nMedia Lenta: €{slow_ma:.2f}\n*Stato:* Trend Ribassista 📉"

    print(msg)
    send_telegram_message(msg)

if __name__ == "__main__":
    run_strategy()
