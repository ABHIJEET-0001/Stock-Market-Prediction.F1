from flask import Flask, render_template, request
from predict import predict_next
import yfinance as yf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

# -------------------------------
# Fetch stock data from Yahoo NSE
# -------------------------------
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period="1mo")

# -------------------------------
# Home Route
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    symbol = request.args.get("stock", "TCS.NS")
    data = get_stock_data(symbol)

    # Latest OHLCV
    open_p = round(data["Open"].iloc[-1], 2)
    high = round(data["High"].iloc[-1], 2)
    low = round(data["Low"].iloc[-1], 2)
    volume = int(data["Volume"].iloc[-1])

    # Close prices
    today_close = round(data["Close"].iloc[-1], 2)
    yesterday_close = round(data["Close"].iloc[-2], 2)

    # Profit / Loss
    change = round(today_close - yesterday_close, 2)
    percent = round((change / yesterday_close) * 100, 2)

    if change > 0:
        trend = "Bullish 📈"
        color = "green"
    else:
        trend = "Bearish 📉"
        color = "red"

    # Market Prediction
    prediction = None
    if request.method == "POST":
        prediction = predict_next(open_p, high, low, volume)

    # -------------------------------
    # PRO Trading Chart
    # -------------------------------
    prices = data["Close"].values
    dates = data.index

    plt.figure(figsize=(20,9), facecolor="white")
    plt.grid(True, linestyle="--", alpha=0.3)

    # Main price line
    plt.plot(dates, prices, color="#1f77b4", linewidth=3, label="Closing Price")

    # Profit / Loss points
    profit_x, profit_y = [], []
    loss_x, loss_y = [], []

    for i in range(1, len(prices)):
        if prices[i] >= prices[i-1]:
            profit_x.append(dates[i])
            profit_y.append(prices[i])
        else:
            loss_x.append(dates[i])
            loss_y.append(prices[i])

    plt.scatter(profit_x, profit_y, color="#2ecc71", s=120, label="Profit Day ▲")
    plt.scatter(loss_x, loss_y, color="#e74c3c", s=120, label="Loss Day ▼")

    # Area under curve
    plt.fill_between(dates, prices, min(prices), color="#3498db", alpha=0.08)

    # Labels
    plt.title(f"{symbol} – 30 Day Market Trend", fontsize=24, fontweight="bold")
    plt.xlabel("Date", fontsize=18, fontweight="bold")
    plt.ylabel("Price (₹)", fontsize=18, fontweight="bold")

    plt.xticks(rotation=25, fontsize=14)
    plt.yticks(fontsize=14)

    plt.legend(fontsize=14, loc="upper left")

    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    plt.savefig("static/graph.png", dpi=180)
    plt.close()

    # -------------------------------
    # Render UI
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
