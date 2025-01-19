import os

from dotenv import load_dotenv

load_dotenv()

BITMEX_API_KEY = os.getenv("BITMEX_API_KEY")
BITMEX_BASE_URL = os.getenv("BITMEX_BASE_URL")
BITMEX_SECRET_KEY = os.getenv("BITMEX_SECRET_KEY")
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_BASE_URL = os.getenv("BINANCE_BASE_URL")