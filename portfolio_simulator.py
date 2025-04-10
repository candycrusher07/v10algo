import random
import datetime

# Capital parameters
INITIAL_CAPITAL = 1000000  # ₹10L paper money
LOT_SIZE = 50  # Nifty options lot size
portfolio = {"capital": INITIAL_CAPITAL, "trades": []}


# Position sizing logic
def calculate_position(confidence_score):
    if confidence_score > 0.85:
        risk_pct = 0.04
    elif confidence_score > 0.7:
        risk_pct = 0.025
    else:
        risk_pct = 0.015

    capital_to_use = portfolio["capital"] * risk_pct
    max_loss_per_trade = capital_to_use

    return capital_to_use, max_loss_per_trade


# Simulate option entry
def simulate_option_trade(signal, direction, confidence):
    capital_to_use, max_loss = calculate_position(confidence)
    spot = signal["entry"]
    strike = signal["strike_price"]
    option_price = round(random.uniform(100, 250), 2)  # Simulated LTP of CE/PE

    quantity = int(capital_to_use / option_price)
    cost = quantity * option_price

    if direction == "LONG":
        target = option_price * 1.3
        stop_loss = option_price * 0.8
    else:
        target = option_price * 1.3
        stop_loss = option_price * 0.8

    trade = {
        "date": str(datetime.date.today()),
        "ticker": signal["ticker"],
        "type": signal["option_type"],
        "strike": strike,
        "entry_price": option_price,
        "target": round(target, 2),
        "stop_loss": round(stop_loss, 2),
        "quantity": quantity,
        "cost": round(cost, 2),
        "status": "OPEN"
    }

    portfolio["trades"].append(trade)
    portfolio["capital"] -= cost
    return trade


# Real-time update (mocked with result randomizer)
def simulate_trade_outcome():
    for trade in portfolio["trades"]:
        if trade["status"] == "OPEN":
            result = random.choice(["TARGET", "STOPLOSS"])
            if result == "TARGET":
                profit = (trade["target"] - trade["entry_price"]) * trade["quantity"]
                portfolio["capital"] += trade["target"] * trade["quantity"]
            else:
                profit = (trade["stop_loss"] - trade["entry_price"]) * trade["quantity"]
                portfolio["capital"] += trade["stop_loss"] * trade["quantity"]

            trade["status"] = result
            trade["pnl"] = round(profit, 2)

    return portfolio


# 🔁 Sample run
if __name__ == "__main__":
    # Mock trade input from previous phase
    signal = {
        "ticker": "NIFTY",
        "entry": 22200,
        "strike_price": 22200,
        "option_type": "CE"
    }

    # Confidence from ML model (0 to 1)
    trade = simulate_option_trade(signal, "LONG", 0.88)
    print("🔔 Trade Taken:", trade)

    updated = simulate_trade_outcome()
    print("📊 Portfolio:", updated["capital"])
    print("📄 Trades:")
    for t in updated["trades"]:
        print(t)
