import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
df = pd.read_csv("training_dataset.csv")

# Encode inputs
le_sentiment = LabelEncoder()
le_ticker = LabelEncoder()

df["sentiment_code"] = le_sentiment.fit_transform(df["sentiment"])
df["ticker_code"] = le_ticker.fit_transform(df["ticker"])
df["label"] = df["movement"].apply(lambda x: 1 if x == "up" else 0)

X = df[["sentiment_code", "ticker_code"]]
y = df["label"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier(n_estimators=100, max_depth=5)
model.fit(X_train, y_train)

# Save model + encoders
pickle.dump(model, open("market_direction_model.pkl", "wb"))
pickle.dump(le_sentiment, open("sentiment_encoder.pkl", "wb"))
pickle.dump(le_ticker, open("ticker_encoder.pkl", "wb"))

accuracy = model.score(X_test, y_test)
print(f"✅ Model Trained — Accuracy: {accuracy*100:.2f}%")
