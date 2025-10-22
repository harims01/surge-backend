# app/finance.py
import yfinance as yf
from fastapi import FastAPI, HTTPException
import pandas as pd
import requests

app = FastAPI()

# Optionally keep your preferred tickers for homepage
PREFERRED_TICKERS = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "LT.NS": "Larsen & Toubro",
}

@app.get("/tickers")
def list_tickers(preferred: bool = True):
    """
    Return preferred stocks if preferred=True, else allow search on any stock
    """
    if preferred:
        return [{"symbol": s, "name": n} for s, n in PREFERRED_TICKERS.items()]
    else:
        return {"message": "Use /search_ticker?query=XYZ to search any stock"}

@app.get("/search_ticker")
def search_ticker(query: str):
    """
    Search for any stock using yfinance's ticker lookup
    """
    try:
        # yfinance has a built-in tickers search
        from yfinance import Ticker
        tk = yf.Ticker(query)
        info = tk.info
        return {
            "symbol": info.get("symbol", query),
            "name": info.get("shortName", "Unknown"),
            "exchange": info.get("exchange", "")
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ticker {query} not found")

@app.get("/quote/{symbol}")
def get_quote(symbol: str):
    try:
        tk = yf.Ticker(symbol)
        info = tk.info
        price = info.get("regularMarketPrice") or info.get("previousClose")
        change = info.get("regularMarketChange") or 0
        pct = info.get("regularMarketChangePercent") or 0

        # Fetch latest news (yfinance provides news list)
        news_list = info.get("news", [])  # list of dicts with title, link, provider
        news = [{"title": n.get("title"), "link": n.get("link")} for n in news_list] if news_list else []

        return {
            "symbol": symbol,
            "price": price,
            "change": change,
            "percent": pct,
            "news": news
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/candles/{symbol}")
def get_candles(symbol: str, period: str = "7d", interval: str = "1h"):
    try:
        tk = yf.Ticker(symbol)
        hist = tk.history(period=period, interval=interval, auto_adjust=False)
        hist = hist.reset_index()
        rows = []
        for _, row in hist.iterrows():
            rows.append({
                "datetime": row["Datetime"].isoformat() if hasattr(row["Datetime"], "isoformat") else str(row["Datetime"]),
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": int(row["Volume"])
            })
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
