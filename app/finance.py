# app/finance.py
import yfinance as yf
import pandas as pd
from fastapi import HTTPException

# For a simple list of Indian tickers, create a small sample mapping.
# In production, you'd load a master list (NSE/BSE) from a file.
INDIAN_TICKERS = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFC.NS": "HDFC Bank",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "LT.NS": "Larsen & Toubro",
    "ITC.NS": "ITC",
    # add more tickers...
}

def list_tickers():
    # return list of dicts: symbol, name
    return [{"symbol": s, "name": n} for s, n in INDIAN_TICKERS.items()]

def get_quote(symbol):
    try:
        tk = yf.Ticker(symbol)
        info = tk.info
        # fallback price fields
        price = info.get("regularMarketPrice") or info.get("previousClose")
        change = info.get("regularMarketChange") or 0
        pct = info.get("regularMarketChangePercent") or 0
        return {"symbol": symbol, "price": price, "change": change, "percent": pct}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_candles(symbol, period="7d", interval="1h"):
    """
    returns OHLCV historical data as list of dicts with timestamp & ohlc
    period examples: '1d','5d','7d','1mo','6mo','1y'
    interval examples: '1m','2m','5m','15m','1h','1d'
    """
    try:
        tk = yf.Ticker(symbol)
        hist = tk.history(period=period, interval=interval, auto_adjust=False)
        hist = hist.reset_index()
        # convert pandas timestamp to iso
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
