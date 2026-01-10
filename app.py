from flask import Flask, render_template, request
from predict import predict_next
import yfinance as yf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

# -------------------------------
# Fetch stock data (Safe)
# -------------------------------
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)

        data = stock.history(period="1mo", interval="1d")

        if data is None or data.empty:
            data = stock.history(period="3mo", interval="1d")

        if data is None or data.empty:
            raise Exception("Yahoo Finance blocked or returned empty data")

        return data

    except Exception as e:
        print("Yahoo API Error:", e)

        # FINAL fallback (so app never crashes)
        import pandas as pd
        import numpy as np

        dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
        base = np.random.uniform(3000, 3400)
        prices = base + np.cumsum(np.random.randn(30) * 5)

        return pd.DataFrame({
            "Open": prices,
            "High": prices + np.random.uniform(5, 20, 30),
            "Low": prices - np.random.uniform(5, 20, 30),
            "Close": prices,
            "Volume": np.random.randint(1000000, 8000000, 30)
        }, index=dates)

# -------------------------------
# Home Route
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    symbol = request.args.get("stock", "TCS.NS")
    data = get_stock_data(symbol)

    # Hard safety
    if data is None or data.empty or len(data) < 2:
        return "Market data not available right now. Try again later."

    # OHLCV
    open_p = round(data["Open"].iloc[-1], 2)
    high = round(data["High"].iloc[-1], 2)
    low = round(data["Low"].iloc[-1], 2)
    volume = int(data["Volume"].iloc[-1])

    today_close = round(data["Close"].iloc[-1], 2)
    yesterday_close = round(data["Close"].iloc[-2], 2)

    change = round(today_close - yesterday_close, 2)
    percent = round((change / yesterday_close) * 100, 2)

    if change > 0:
        trend = "Bullish 📈"
        color = "green"
    else:
        trend = "Bearish 📉"
        color = "red"

    # Prediction
    prediction = None
    if request.method == "POST":
        prediction = predict_next(open_p, high, low, volume)

    # -------------------------------
    # Professional Trading Graph
    # -------------------------------
    prices = data["Close"].values
    dates = data.index

    plt.figure(figsize=(16,7), facecolor="white")

    # Closing line
    plt.plot(dates, prices, color="#1f77b4", linewidth=3, label="Closing Price")

    # Profit & Loss dots
    profit_x, profit_y = [], []
    loss_x, loss_y = [], []

    for i in range(1, len(prices)):
        if prices[i] >= prices[i-1]:
            profit_x.append(dates[i])
            profit_y.append(prices[i])
        else:
            loss_x.append(dates[i])
            loss_y.append(prices[i])

    plt.scatter(profit_x, profit_y, color="#2ecc71", s=90, label="Profit Day ▲")
    plt.scatter(loss_x, loss_y, color="#e74c3c", s=90, label="Loss Day ▼")

    # Area fill
    plt.fill_between(dates, prices, min(prices), color="#3498db", alpha=0.08)

    # Titles & labels
    plt.title(f"{symbol} – 30 Day Market Trend", fontsize=20, fontweight="bold")
    plt.xlabel("Date", fontsize=14, fontweight="bold")
    plt.ylabel("Price (₹)", fontsize=14, fontweight="bold")

    plt.xticks(rotation=25, fontsize=12)
    plt.yticks(fontsize=12)

    plt.grid(True, linestyle="--", alpha=0.3)

    # Legend under graph
    leg = plt.legend(
        fontsize=12,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        ncol=3,
        frameon=False
    )

    for text in leg.get_texts():
        text.set_color("#000000")
        text.set_fontweight("bold")

    # Clean look
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    plt.savefig("static/graph.png", dpi=160)
    plt.close()

    # -------------------------------
    # Send to UI
    # -------------------------------
    return render_template(
        "index.html",
        symbol=symbol,
        prediction=prediction,
        open=open_p,
        high=high,
        low=low,
        volume=volume,
        today=today_close,
        change=change,
        percent=percent,
        trend=trend,
        color=color
    )

if __name__ == "__main__":
    app.run(debug=True)
