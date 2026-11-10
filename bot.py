import os
import requests

# Parametri della Strategia Quantitativa
ASSET = "bitcoin"  # O un altro asset di riferimento
FAST_PERIOD = 20   # Media mobile veloce
SLOW_PERIOD = 50   # Media mobile lenta
CAPITAL = 100.0    # Il tuo capitale di partenza in euro

def get_market_data():
    """
    Scarica i dati storici dei prezzi in modo gratuito da un'API pubblica (es. CoinGecko o simili)
    """
    url = f"https://api.coingecko.com/api/v3/coins/{ASSET}/market_chart?vs_currency=eur&days=30"
    try:
        response = requests.get(url)
        data = response.json()
        # Estraiamo solo la lista dei prezzi di chiusura
        prices = [p[1] for p in data['prices']]
        return prices
    except Exception as e:
        print(f"Errore nel recupero dati: {e}")
        return []

def calculate_moving_average(prices, period):
    """Calcola la media mobile semplice (SMA)"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def run_strategy():
    print("--- AVVIO ANALISI BOT TRADING ---")
    prices = get_market_data()
    
    if not prices:
        print("Impossibile procedere senza dati di mercato.")
        return

    current_price = prices[-1]
    fast_ma = calculate_moving_average(prices, FAST_PERIOD)
    slow_ma = calculate_moving_average(prices, SLOW_PERIOD)

    print(f"Prezzo attuale di {ASSET}: €{current_price:.2f}")
    print(f"Media Mobile Veloce ({FAST_PERIOD}): €{fast_ma:.2f}")
    print(f"Media Mobile Lenta ({SLOW_PERIOD}): €{slow_ma:.2f}")

    # Logica di decisione del Trading System
    if fast_ma > slow_ma:
        print(">>> SEGNALE: TREND RIALZISTA (Possibile acquisto / Posizione Long)")
        # Qui in futuro inseriremo la chiamata API al broker per comprare
    else:
        print(">>> SEGNALE: TREND RIBASSISTA (Attendere / Posizione Flat o Short)")
        # Qui inseriremo la chiamata per vendere o stare fuori

if __name__ == "__main__":
    run_strategy()
