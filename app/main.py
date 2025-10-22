# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.finance import list_tickers, get_quote, get_candles, search_ticker
from app.news import search_news_for_company

app = FastAPI(title="Surge Backend")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root Route
@app.get("/")
def home():
    return {
        "message": "✅ Surge Backend is Running",
        "routes": [
            "/tickers",
            "/search_ticker?query=XYZ",
            "/quote/{symbol}",
            "/candles/{symbol}",
            "/news/{symbol}"
        ]
    }

# ✅ Tickers (preferred stocks)
@app.get("/tickers")
def api_list_tickers(preferred: bool = True):
    return {"tickers": list_tickers(preferred=preferred)}

# ✅ Search any stock
@app.get("/search_ticker")
def api_search_ticker(query: str):
    return search_ticker(query)

# ✅ Quote for a stock
@app.get("/quote/{symbol}")
def api_quote(symbol: str):
    return get_quote(symbol)

# ✅ Candles (OHLCV)
@app.get("/candles/{symbol}")
def api_candles(symbol: str, period: str = "7d", interval: str = "1h"):
    return get_candles(symbol, period=period, interval=interval)

# ✅ News for a stock
@app.get("/news/{symbol}")
def api_news(symbol: str, page_size: int = 10):
    return {"articles": search_news_for_company(symbol, page_size=page_size)}
