import time
from doctest import run_docstring_examples
from typing import List, Union

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
async def place_order(request: OrderRequest):
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

@router.put("/orders")
async def amend_order(
        request: AmendRequest
):
    # Ensure the request body contains at least one valid parameter
    if not request:
        raise HTTPException(status_code=400, detail="At least one parameter (quantity, price, or others) must be provided.")

    # Setting the expiry time for the API request signature (5 seconds from the current time)
    expires = int(round(time.time()) + 5)

    url = BITMEX_BASE_URL + "/order"

    # JSON format used for the request should match the one used for generating the signature
    request = to_valid_json(request)

    # Headers for the API request including the expiry time, API key, and signature
    headers = {
        "api-expires": str(expires),
        "api-key": BITMEX_API_KEY,
        "api-signature": generate_signature(BITMEX_SECRET_KEY, url=url, verb='PUT', nonce=expires, data=request)
    }

    response = requests.put(url, data=request, headers=headers)
    if response.status_code == 200:
        return JSONResponse(status_code=response.status_code, content=response.json())
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

@router.delete("/orders")
async def delete_orders(
        request: Union[CancelRequest, CancelAllRequest]
):
    # The request is for canceling a specific order (CancelRequest)
    if isinstance(request, CancelRequest):
        # Setting the expiry time for the API request signature (5 seconds from the current time)
        expires = int(round(time.time()) + 5)

        url = BITMEX_BASE_URL + "/order"

        # JSON format used for the request should match the one used for generating the signature
        request = to_valid_json(request)

        # Headers for the API request including the expiry time, API key, and signature
        headers = {
            "api-expires": str(expires),
            "api-key": BITMEX_API_KEY,
            "api-signature": generate_signature(BITMEX_SECRET_KEY, url=url, verb='DELETE', nonce=expires, data=request)
        }

        response = requests.delete(url, data=request, headers=headers)
        if response.status_code == 200:
            return JSONResponse(status_code=response.status_code, content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

    # The request is for canceling all orders (CancelAllRequest)
    elif isinstance(request, CancelAllRequest):
        # Setting the expiry time for the API request signature (5 seconds from the current time)
        expires = int(round(time.time()) + 5)

        url = BITMEX_BASE_URL + "/order/all"

        # If 'all' is set to True, prepare an empty request body
        if request.all:
            request = ""
        # If 'all' is set to False (Default), Ensure that at least one filter parameter is provided
        else:
            if not request.targetAccountIds and not request.filter and not request.symbol:
                raise HTTPException(
                    status_code=400,
                    detail="""At least one parameter (targetAccountIds, filter, or symbol) must be provided.
                    If you want to cancel all orders without a filter, please set the parameter ‘all’ to ‘true’."""
                )
            # JSON format used for the request should match the one used for generating the signature
            request = to_valid_json(request)

        # Headers for the API request including the expiry time, API key, and signature
        headers = {
            "api-expires": str(expires),
            "api-key": BITMEX_API_KEY,
            "api-signature": generate_signature(BITMEX_SECRET_KEY, url=url, verb='DELETE', nonce=expires, data=request)
        }

        response = requests.delete(url, data=request, headers=headers)
        if response.status_code == 200:
            return JSONResponse(status_code=response.status_code, content=response.json())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())