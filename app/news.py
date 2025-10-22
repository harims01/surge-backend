# app/news.py
import requests
from app.config import NEWS_API_KEY
from fastapi import HTTPException

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

def search_news_for_company(query, page_size=10):
    params = {
        "q": query,
        "pageSize": page_size,
        "language": "en",
        "apiKey": NEWS_API_KEY,
        "sortBy": "publishedAt"
    }
    r = requests.get(NEWS_ENDPOINT, params=params, timeout=10)
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="NewsAPI error")
    data = r.json()
    # return list of articles with needed fields
    articles = []
    for a in data.get("articles", []):
        articles.append({
            "title": a.get("title"),
            "description": a.get("description"),
            "url": a.get("url"),
            "source": a.get("source", {}).get("name"),
            "publishedAt": a.get("publishedAt"),
            "urlToImage": a.get("urlToImage")
        })
    return articles
