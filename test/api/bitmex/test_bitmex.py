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