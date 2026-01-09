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
    data = stock.history(period="1mo")
    return data

# -------------------------------
# Home Route
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def home():

    # Get selected stock (default = TCS)
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

    # AI Prediction
    prediction = None
    if request.method == "POST":
        prediction = predict_next(open_p, high, low, volume)

    # -------------------------------
    # Generate Stock Market Graph
    # -------------------------------
    prices = data["Close"].values
    dates = data.index

    plt.figure(figsize=(9,4))

    for i in range(1, len(prices)):
        if prices[i] >= prices[i-1]:
            plt.plot(dates[i-1:i+1], prices[i-1:i+1], color="green", linewidth=2)
        else:
            plt.plot(dates[i-1:i+1], prices[i-1:i+1], color="red", linewidth=2)

    plt.fill_between(dates, prices, min(prices), where=(prices >= prices[0]), color="green", alpha=0.1)
    plt.fill_between(dates, prices, min(prices), where=(prices < prices[0]), color="red", alpha=0.1)

    plt.title(f"{symbol} Share Price - Last 30 Trading Days")
    plt.xlabel("Date")
    plt.ylabel("Price (₹)")
    plt.xticks(rotation=25)
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("static/graph.png")
    plt.close()

    # -------------------------------
    # Send data to UI
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
