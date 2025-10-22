from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Fetch the API key
api_key = os.getenv("NEWS_API_KEY")

# Verify
if api_key:
    print("✅ .env file loaded successfully!")
    print(f"NEWS_API_KEY = {api_key}")
else:
    print("❌ Failed to load .env file. Please check if it exists and is in the correct directory.")
