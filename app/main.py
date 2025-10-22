# app/main.py
from fastapi import FastAPI
from app.finance import list_tickers, get_quote, get_candles
from app.news import search_news_for_company
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Surge Backend")

# allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    # get company name from symbol mapping if available
    company = symbol
    from app.finance import INDIAN_TICKERS
    company = INDIAN_TICKERS.get(symbol, symbol)
    return {"articles": search_news_for_company(company, page_size=page_size)}
