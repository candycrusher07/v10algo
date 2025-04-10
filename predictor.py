import pickle
from sentiment_mapper import analyze_sentiment, match_to_ticker

# Load model + encoders
model = pickle.load(open("market_direction_model.pkl", "rb"))
le_sentiment = pickle.load(open("sentiment_encoder.pkl", "rb"))
le_ticker = pickle.load(open("ticker_encoder.pkl", "rb"))

def predict_direction(news):
    sentiment = analyze_sentiment(news)
    ticker = match_to_ticker(news)

    try:
        input_vector = [[
            le_sentiment.transform([sentiment])[0],
            le_ticker.transform([ticker])[0]
        ]]
        prediction = model.predict(input_vector)[0]
        confidence = model.predict_proba(input_vector)[0][prediction]
        return {
            "predicted_direction": "up" if prediction == 1 else "down",
            "confidence_score": round(confidence, 2)
        }
    except Exception as e:
        return {"error": str(e)}

# Example
news = "US Fed hints at pause in rate hikes, markets rally globally"
result = predict_direction(news)
print(result)
