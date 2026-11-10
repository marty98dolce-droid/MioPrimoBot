import os
import requests

# Leggiamo i dati protetti da GitHub Secrets
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

ASSET = "bitcoin"
FAST_PERIOD = 20
SLOW_PERIOD = 50

def send_telegram_message(message):
    """Invia la notifica sul tuo Telegram"""
    if not TOKEN or not CHAT_ID:
        print("Token o Chat ID di Telegram non configurati.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f5f5f5, f"Errore invio Telegram: {e}")

def get_market_data():
    url = f"https://api.coingecko.com/api/v3/coins/{ASSET}/market_chart?vs_currency=eur&days=30"
    try:
        response = requests.get(url)
        data = response.json()
        prices = [p[1] for p in data['prices']]
        return prices
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
    slow_ma = calculate_moving_average(prices, SLOW_PERIOD] if 'SLOW_PERIOD' in globals() else calculate_moving_average(prices, SLOW_PERIOD)

    # Messaggio da inviare
    if fast_ma > slow_ma:
        msg = f"🚀 *SEGNALE TRADING: BULLISH*\n\nAsset: {ASSET.upper()}\nPrezzo: €{current_price:.2f}\nMedia Veloce: €{fast_ma:.2f}\nMedia Lenta: €{slow_ma:.2f}\n*Stato:* Trend Rialzista 📈"
    else:
        msg = f"🔻 *SEGNALE TRADING: BEARISH*\n\nAsset: {ASSET.upper()}\nPrezzo: €{current_price:.2f}\nMedia Veloce: €{fast_ma:.2f}\nMedia Lenta: €{slow_ma:.2f}\n*Stato:* Trend Ribassista 📉"

    print(msg)
    send_telegram_message(msg)

if __name__ == "__main__":
    run_strategy()
