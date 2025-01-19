import os

from dotenv import load_dotenv
from fastapi import APIRouter

router = APIRouter(
    prefix="/binance"
)

load_dotenv()
