# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.finance import list_tickers, get_quote, get_candles, INDIAN_TICKERS
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

# ✅ New Root Route (Now homepage won’t return 404)
@app.get("/")
def home():
    return {
        "message": "✅ Surge Backend is Running",
        "routes": [
            "/tickers",
            "/quote/{symbol}",
            "/candles/{symbol}",
            "/news/{symbol}"
        ]
    }

@app.get("/tickers")
def api_list_tickers():
    return {"tickers": list_tickers()}

@app.get("/quote/{symbol}")
def api_quote(symbol: str):
    return get_quote(symbol)

@app.get("/candles/{symbol}")
def api_candles(symbol: str, period: str = "7d", interval: str = "1h"):
    return get_candles(symbol, period=period, interval=interval)

@app.get("/news/{symbol}")
def api_news(symbol: str, page_size: int = 10):
    company = INDIAN_TICKERS.get(symbol, symbol)
    return {"articles": search_news_for_company(company, page_size=page_size)}
