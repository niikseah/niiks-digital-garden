import os
from pathlib import Path

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("APIFY_TOKEN"):
    project_root = Path(__file__).resolve().parents[1]
    load_dotenv(project_root / ".venv/.env")

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
if not APIFY_TOKEN:
    print("⚠️  Warning: APIFY_TOKEN is missing from environment variables")
    print("   Instagram and TikTok extraction will not work without Apify token.")
    print("   Set APIFY_TOKEN in your .env file to enable these extractors.")
    client = None
else:
    client = ApifyClient(APIFY_TOKEN)
    print(f"✅ Apify client initialized (token: {APIFY_TOKEN[:10]}...)")

