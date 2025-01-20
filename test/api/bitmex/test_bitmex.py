from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


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
    assert response.status_code == 400
    assert response.json() == {"detail": mock_error_response}