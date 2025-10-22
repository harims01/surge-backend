# app/config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access your News API key
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise ValueError("❌ NEWS_API_KEY is missing! Please add it to your .env file.")
