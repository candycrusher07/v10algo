# 📦 NewsPulse AI - Phase 1: Global News Scraper (1-second polling)

import requests
import time
import json
from datetime import datetime

# --- CONFIG ---
GNEWS_API_KEY = "863fc85c3d89a83c25ce95ee13b6ee63"  # Replace with your actual API key
NEWS_QUERY = "(nifty OR banknifty OR sensex OR sgx nifty OR fed OR RBI OR inflation OR interest rate OR US markets OR earnings OR war OR oil)"

NEWS_ENDPOINT = f"https://gnews.io/api/v4/search?q={NEWS_QUERY}&lang=en&country=in&token={GNEWS_API_KEY}&max=10"

# --- MAIN FETCH FUNCTION ---
def fetch_news():
    try:
        response = requests.get(NEWS_ENDPOINT)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            for article in articles:
                print(f"[{datetime.now()}] 📰 {article['title']}")
                print(f"URL: {article['url']}")
                print(f"Published: {article['publishedAt']}")
                print("Summary:", article['description'][:150] + "...")
                print("-" * 80)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print("Exception occurred while fetching news:", str(e))

# --- LOOP ---
if __name__ == "__main__":
    print("\n🚀 Starting NewsPulse AI - Phase 1: Real-Time News Scanner\n")
    while True:
        fetch_news()
        time.sleep(1)  # Poll every second
