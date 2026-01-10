# 📊 Stock Market Prediction System  
AI-Powered Trading Dashboard for Indian Stock Market (NSE)

🌐 Live Demo:
https://stock-market-prediction-f1.onrender.com

##🚀 Project Overview
A professional **AI-powered stock market prediction web application** that uses real-time NSE stock data and Machine Learning to predict future stock prices.  
The system supports multiple Indian companies such as **TCS, Infosys, Reliance, HDFC Bank and ICICI Bank** and displays live prices, trends, profit/loss, and interactive market charts through a modern dashboard.

---

## 🚀 Features  

- 📈 Live NSE stock prices (Yahoo Finance API)  
- 🤖 Machine Learning based price prediction  
- 📊 30-day stock market trend chart (green/red)  
- 📉 Profit & Loss indicator  
- 📈 Bullish / Bearish market trend  
- 🔄 Multi-company stock support  
- 🌐 Web-based FinTech dashboard (Flask)  

---

## 🧠 Technologies Used  

| Layer | Technology |
|------|-----------|
| Backend | Python, Flask |
| Machine Learning | Scikit-learn |
| Data Source | Yahoo Finance (yfinance) |
| Visualization | Matplotlib |
| Frontend | HTML, CSS |
| API | NSE Market Data |

---

## 📂 Project Structure  

StockVision/
│
├── data/
│ └── TCS.csv
│
├── model/
│ └── stock_model.pkl
│
├── static/
│ ├── style.css
│ └── graph.png
│
├── templates/
│ └── index.html
│
├── app.py
├── train.py
├── predict.py
└── README.md


---
## 🛡 Reliability

The system includes a fallback data engine.
If Yahoo Finance is unavailable, the app switches to simulated market data so the website never crashes — similar to real FinTech systems.

## ⚙️ Installation  

1. Clone or download the repository  
2. Open terminal inside the project folder  
3. Install dependencies  

```bash
pip install flask pandas numpy scikit-learn matplotlib yfinance

🧠 Train the Machine Learning Model
python train.py


This will generate the trained model:

model/stock_model.pkl

🌐 Run the Web Application
python app.py


Open in browser:

http://127.0.0.1:5000

## 👨‍💻 Author

Abhijeet Kasera
B.Tech Computer Science (AI & Software Development)

