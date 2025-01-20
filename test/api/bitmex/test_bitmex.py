from fastapi.testclient import TestClient
from pydantic.dataclasses import dataclass
from starlette.testclient import TestClient as StartletteTestClient

from app.main import app
from unittest.mock import patch, call

from app.settings import BITMEX_BASE_URL

client = TestClient(app)
new_client = StartletteTestClient(app)

@patch("app.api.bitmex.main.requests.get")
def test_get_orders_success(mock_get):
    mock_success_response = {
        "status": "success",
    }

    # Set up the mock to return a successful response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_success_response

    response = client.get("/bitmex/orders", params={"order_ids": ["1"]})

    # Assert the mock API was called correctly
    mock_get.assert_called_once()
    assert response.status_code == 200
    assert response.json() == mock_success_response


@patch("app.api.bitmex.main.requests.get")
def test_get_orders_failure(mock_get):
    mock_error_response = {
        "error": "Invalid ID"
    }

    # Set up the mock to return an error response
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = mock_error_response

    response = client.get("/bitmex/orders", params={"order_ids": ["invalid"]})

    # Assert the mock API was called correctly
    mock_get.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {"detail": mock_error_response}


@patch("app.api.bitmex.main.requests.post")
def test_place_order_success(mock_post):
    mock_success_response = {
        "status": "success",
    }

    # Set up the mock to return a successful response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_success_response

    # Call the endpoint with mocked order request data
    response = client.post("/bitmex/orders", json={
        "symbol": "XBTUSD",
        "price": 50000,
        "orderQty": 1,
        "side": "Buy"
    })

    # Assert the mock API was called correctly
    mock_post.assert_called_once()
    assert response.status_code == 200
    assert response.json() == mock_success_response


@patch("app.api.bitmex.main.requests.post")
def test_place_order_failure(mock_post):
    mock_error_response = {
        "error": "error"
    }

    # Set up the mock to return an error response
    mock_post.return_value.status_code = 400
    mock_post.return_value.json.return_value = mock_error_response

    # Call the endpoint with mocked order request data
    response = client.post("/bitmex/orders", json={
        "symbol": "XBTUSD",
        "price": 50000,
        "orderQty": 1,
        "side": "Buy"
    })

    # Assert the mock API was called correctly
    mock_post.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {"detail": mock_error_response}


@patch("app.api.bitmex.main.requests.put")
def test_amend_order_success(mock_put):
    mock_success_response = {
        "status": "success",
    }

    # Set up the mock to return a successful response
    mock_put.return_value.status_code = 200
    mock_put.return_value.json.return_value = mock_success_response

    # Call the endpoint with mocked amend request data
    response = client.put("/bitmex/orders", json={
        "orderID": "12345",
        "price": 100.0,
        "orderQty": 5.0
    })

    # Assert the mock API was called correctly
    mock_put.assert_called_once()
    assert response.status_code == 200
    assert response.json() == mock_success_response


@patch("app.api.bitmex.main.requests.put")
def test_amend_order_failure(mock_put):
    mock_error_response = {
        "error": "Invalid ID"
    }

    # Set up the mock to return an error response
    mock_put.return_value.status_code = 400
    mock_put.return_value.json.return_value = mock_error_response

    # Call the endpoint with mocked amend request data
    response = client.put("/bitmex/orders", json={
        "orderID": "12345",
        "price": 100.0,
        "orderQty": 5.0
    })

    # Assert the mock API was called correctly
    mock_put.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {"detail": mock_error_response}


# Cancel an order by orderID or origClOrdID
@patch("app.api.bitmex.main.requests.delete")
def test_cancel_orders_success(mock_delete):
    mock_success_response = {
        "status": "success",
    }

    # Set up the mock to return a successful response
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = mock_success_response

    # Call the endpoint with mocked cancel request data
    response = client.request("DELETE", "/bitmex/orders", json={
        "orderID": "12345"
    })

    # Assert that the mock API was called once
    mock_delete.assert_called_once()

    # Get the actual call arguments
    args, kwargs = mock_delete.call_args

    # Check that the called URL is correct
    assert args[0] == BITMEX_BASE_URL + "/order"

    assert response.status_code == 200
    assert response.json() == mock_success_response


# Error response for cancellation failure
@patch("app.api.bitmex.main.requests.delete")
def test_cancel_orders_failure(mock_delete):
    mock_error_response = {
        "error": "Invalid ID"
    }

    # Set up the mock to return an error response
    mock_delete.return_value.status_code = 400
    mock_delete.return_value.json.return_value = mock_error_response

    # Call the endpoint with mocked cancel request data
    response = client.request("DELETE", "/bitmex/orders", json={
        "orderID": "a"
    })

    # Assert the mock API was called correctly
    mock_delete.assert_called_once()
    assert response.status_code == 400
    assert response.json() == {"detail": mock_error_response}


# Cancel all orders without any filter
@patch("app.api.bitmex.main.requests.delete")
def test_cancel_orders_all_without_filter_success(mock_delete):
    mock_success_response = {
        "status": "success",
    }

    # Set up the mock to return a successful response
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = mock_success_response

    # Call the endpoint without request data to cancel all orders that the authenticated user has
    response = client.request("DELETE", "/bitmex/orders", json={
        "all": "true"
    })

    # Assert that the mock API was called once
    mock_delete.assert_called_once()

    # Get the actual call arguments
    args, kwargs = mock_delete.call_args

    # Check that the called URL is correct
    assert args[0] == BITMEX_BASE_URL + "/order/all"

    assert response.status_code == 200
    assert response.json() == mock_success_response


# Cancel all orders without any filter, and add a memo (text)
@patch("app.api.bitmex.main.requests.delete")
def test_cancel_orders_all_without_filter_success_added_description(mock_delete):
    mock_success_response = {
        "status": "success",
    }

    # Set up the mock to return a successful response
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = mock_success_response

    # Call the endpoint without request data to cancel all orders that the authenticated user has
    response = client.request("DELETE", "/bitmex/orders", json={
        "all": "true",
        "text": "description"
    })

    # Assert that the mock API was called once
    mock_delete.assert_called_once()

    # Get the actual call arguments
    args, kwargs = mock_delete.call_args

    # Check that the called URL is correct
    assert args[0] == BITMEX_BASE_URL + "/order/all"

    assert response.status_code == 200
    assert response.json() == mock_success_response


# If 'all' paramter is not specified, at least one filter must be added
def test_cancel_orders_all_without_filter_failure():
    # Call the endpoint without request data to cancel all orders that the authenticated user has
    response = client.request("DELETE", "/bitmex/orders", json={
        "text": "description"
    })
    assert response.status_code == 400
    error_message = response.json().get("detail", "")
    assert error_message == """At least one parameter (targetAccountIds, filter, or symbol) must be provided.
                    If you want to cancel all orders without a filter, please set the parameter ‘all’ to ‘true’."""


# Cancel all orders from the filtered results
@patch("app.api.bitmex.main.requests.delete")
def test_cancel_orders_all_with_filter_success(mock_delete):
    mock_success_response = {
        "status": "success",
    }

    # Set up the mock to return a successful response
    mock_delete.return_value.status_code = 200
    mock_delete.return_value.json.return_value = mock_success_response

    # Call the endpoint with mocked 'cancel all' request data
    response = client.request("DELETE", "/bitmex/orders", json={
        "symbol": "ETCUSD",
        "filter": {
            "side": "Buy"
        }
    })

    # Assert that the mock API was called once
    mock_delete.assert_called_once()

    # Get the actual call arguments
    args, kwargs = mock_delete.call_args

    # Check that the called URL is correct
    assert args[0] == BITMEX_BASE_URL + "/order/all"

    assert response.status_code == 200
    assert response.json() == mock_success_response