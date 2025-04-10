import yfinance as yf
import datetime
from sentiment_mapper import analyze_sentiment, match_to_ticker

# Example input
news_text = "SGX Nifty rises 150 points as US Fed keeps interest rates unchanged. Positive sentiment across global markets."

# Get real-time price
def get_live_price(ticker_name):
    try:
        ticker = yf.Ticker("^NSEI") if ticker_name == "NIFTY" else (
            yf.Ticker("^NSEBANK") if ticker_name == "BANKNIFTY" else yf.Ticker("RELIANCE.NS")
        )
        price = ticker.history(period="1d").tail(1)["Close"].values[0]
        return round(price, 2)
    except:
        return None

# Generate option trade
def generate_trade(news_text):
    sentiment = analyze_sentiment(news_text)
    ticker = match_to_ticker(news_text)
    price = get_live_price(ticker)

    if price is None:
        return "Could not fetch live price."

    direction = "LONG" if sentiment == "positive" else "SHORT"
    option_type = "CE" if direction == "LONG" else "PE"

    # Target/SL logic (adaptive later with ML)
    target = round(price * 1.01, 2) if direction == "LONG" else round(price * 0.99, 2)
    stop_loss = round(price * 0.985, 2) if direction == "LONG" else round(price * 1.015, 2)

    # Suggest nearest ATM strike
    strike = round(price / 50) * 50  # Approx ATM
    expiry = (datetime.date.today() + datetime.timedelta((3 - datetime.date.today().weekday()) % 7)).strftime("%d-%b-%Y")

    return {
        "news": news_text,
        "ticker": ticker,
        "sentiment": sentiment,
        "direction": direction,
        "live_price": price,
        "entry": price,
        "target": target,
        "stop_loss": stop_loss,
        "option_type": option_type,
        "strike_price": strike,
        "expiry": expiry,
        "time_to_enter": "Immediately",
        "confidence": "High" if sentiment in ["positive", "negative"] else "Medium"
    }

# Example run
if __name__ == "__main__":
    trade_signal = generate_trade(news_text)
    for k, v in trade_signal.items():
        print(f"{k.capitalize()}: {v}")
