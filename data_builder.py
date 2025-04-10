import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from sentiment_mapper import analyze_sentiment, match_to_ticker

# Sample data: list of headlines + publish time (for demo)
news_data = [
    {"headline": "RBI keeps rates unchanged, market sees boost", "date": "2024-04-01"},
    {"headline": "US inflation data triggers selloff in global equities", "date": "2024-04-02"},
    {"headline": "Oil prices spike due to Middle East tensions", "date": "2024-04-03"}
]

df = pd.DataFrame(news_data)

# Build dataset
def build_training_data(df):
    rows = []
    for index, row in df.iterrows():
        sentiment = analyze_sentiment(row["headline"])
        ticker = match_to_ticker(row["headline"])
        if ticker in ["NIFTY", "BANKNIFTY"]:
            ticker_code = "^NSEI" if ticker == "NIFTY" else "^NSEBANK"
        else:
            ticker_code = "RELIANCE.NS"

        try:
            news_date = datetime.strptime(row["date"], "%Y-%m-%d")
            price_data = yf.Ticker(ticker_code).history(start=news_date, end=news_date + timedelta(days=2))
            if price_data.empty:
                continue

            open_price = price_data.iloc[0]["Open"]
            close_price = price_data.iloc[-1]["Close"]
            movement = "up" if close_price > open_price else "down"

            rows.append({
                "headline": row["headline"],
                "date": row["date"],
                "sentiment": sentiment,
                "ticker": ticker,
                "open_price": round(open_price, 2),
                "close_price": round(close_price, 2),
                "movement": movement
            })
        except Exception as e:
            print(f"Error processing row: {row['headline']} | {e}")
            continue

    return pd.DataFrame(rows)

# Build and save
df_out = build_training_data(df)
df_out.to_csv("training_dataset.csv", index=False)
