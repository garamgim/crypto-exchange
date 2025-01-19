import time
from encodings.iso8859_4 import decoding_table
from typing import List

import requests
from fastapi import APIRouter, Query, HTTPException
from starlette.responses import JSONResponse

from app.settings import *
from .auth import *
from .enums import OrderState
from .schemas import *

router = APIRouter(
    prefix="/bitmex"
)


@router.get("/orders")
async def get_orders(
        order_ids: Optional[List[str]] = Query(None, description="Order IDs to filter by."),
        start_time: Optional[str] = Query(None, description="Start time for date range filter (ISO 8601)."),
        end_time: Optional[str] = Query(None, description="End time for date range filter (ISO 8601)."),
        state: Optional[List[OrderState]] = Query(None,
                                                  description="Order state (e.g., NEW, PARTIALLY FILLED, FILLED, CANCELED)."),
        active: Optional[bool] = Query(False, description="Whether to filter only active orders."),
):
    # Setting the expiry time for the API request signature (5 seconds from the current time)
    expires = int(round(time.time()) + 5)

    url = BITMEX_BASE_URL + "/order"

    # Dictionary to store filters for the API request
    filters = {}
    if order_ids:
        filters["orderID"] = order_ids
    if state:
        filters["ordStatus"] = state
    if active:
        filters["workingIndicator"] = True

    # Parameters for the API request
    params = {}
    if filters:
        params["filter"] = json.dumps(filters)
    if start_time:
        params["startTime"] = start_time
    if end_time:
        params["endTime"] = end_time

    # Headers for the API request including the expiry time, API key, and signature
    headers = {
        "api-expires": str(expires),
        "api-key": BITMEX_API_KEY,
        "api-signature": generate_signature(BITMEX_SECRET_KEY, url=url, query_params=params, verb='GET', nonce=expires)
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return JSONResponse(status_code=response.status_code, content=response.json())
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())


@router.post("/orders")
async def place_orders(request: OrderRequest):
    # Setting the expiry time for the API request signature (5 seconds from the current time)
    expires = int(round(time.time()) + 5)

    url = BITMEX_BASE_URL + "/order"

    # JSON format used for the request should match the one used for generating the signature
    request = to_valid_json(request)

    # Headers for the API request including the expiry time, API key, and signature
    headers = {
        "api-expires": str(expires),
        "api-key": BITMEX_API_KEY,
        "api-signature": generate_signature(BITMEX_SECRET_KEY, url=url, verb='POST', nonce=expires, data=request)
    }

    response = requests.post(url, data=request, headers=headers)
    if response.status_code == 200:
        return JSONResponse(status_code=response.status_code, content=response.json())
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
