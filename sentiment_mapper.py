from transformers import BertTokenizer, BertForSequenceClassification
import torch
import yfinance as yf
import nltk
from nltk.tokenize import sent_tokenize

nltk.download("punkt")

# Load FinBERT model
model_path = "yiyanghkust/finbert-tone"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)

# Sample news headline (from Phase 1)
sample_news = "RBI keeps repo rate unchanged but signals dovish stance. Banking sector expected to benefit."

# Function: Perform sentiment analysis
def analyze_sentiment(news_text):
    sentences = sent_tokenize(news_text)
    sentiments = {"positive": 0, "negative": 0, "neutral": 0}
    
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=1).item()
            if predicted_class == 0:
                sentiments["negative"] += 1
            elif predicted_class == 1:
                sentiments["neutral"] += 1
            else:
                sentiments["positive"] += 1
    
    return max(sentiments, key=sentiments.get)

# Function: Match news to ticker/index
def match_to_ticker(news_text):
    news_lower = news_text.lower()
    if "rbi" in news_lower or "bank" in news_lower:
        return "BANKNIFTY"
    elif "fed" in news_lower or "us market" in news_lower:
        return "S&P 500"
    elif "sgx nifty" in news_lower:
        return "SGX NIFTY"
    elif "oil" in news_lower:
        return "RELIANCE"
    elif "nifty" in news_lower:
        return "NIFTY"
    return "GENERAL"

# Run analysis
if __name__ == "__main__":
    sentiment = analyze_sentiment(sample_news)
    ticker = match_to_ticker(sample_news)

    print(f"🧠 News: {sample_news}")
    print(f"📊 Sentiment: {sentiment}")
    print(f"🏷️ Mapped Ticker: {ticker}")
