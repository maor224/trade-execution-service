import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.utils.alpaca_client import get_alpaca_client
from tests.fake_alpaca_client import FakeAlpacaClient


@pytest.fixture(scope="module")
def fake_alpaca_client():
    return FakeAlpacaClient()


@pytest.fixture(scope="module", autouse=True)
def override_dependency(fake_alpaca_client):
    def get_fake_alpaca_client():
        return fake_alpaca_client

    app.dependency_overrides[get_alpaca_client] = get_fake_alpaca_client
    yield
    app.dependency_overrides.clear()


client = TestClient(app)


def test_get_orders(fake_alpaca_client):
    fake_alpaca_client.orders.append(
        {
            "symbol": "AAPL",
            "qty": 1,
            "side": "buy",
            "time_in_force": "day",
            "order_type": "market",
        }
    )
    fake_alpaca_client.orders.append(
        {
            "symbol": "TSLA",
            "qty": 2,
            "side": "sell",
            "time_in_force": "gtc",
            "limit_price": 700,
            "order_type": "limit",
        }
    )

    response = client.get("/orders")

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 2

    assert response_data[0]["symbol"] == "AAPL"
    assert response_data[0]["qty"] == 1
    assert response_data[0]["side"] == "buy"
    assert response_data[0]["time_in_force"] == "day"
    assert response_data[0]["order_type"] == "market"

    assert response_data[1]["symbol"] == "TSLA"
    assert response_data[1]["qty"] == 2
    assert response_data[1]["side"] == "sell"
    assert response_data[1]["time_in_force"] == "gtc"
    assert response_data[1]["limit_price"] == 700
    assert response_data[1]["order_type"] == "limit"


def test_market_order(fake_alpaca_client):
    payload = {
        "symbol": "AAPL",
        "qty": 1,
        "side": "buy",
        "time_in_force": "day",
    }

    response = client.post("/orders/market", json=payload)

    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert response_data["message"] == "Order placed successfully"
    assert "order" in response_data

    assert len(fake_alpaca_client.orders) == 1
    order = fake_alpaca_client.orders[0]
    assert order["symbol"] == "AAPL"
    assert order["qty"] == 1
    assert order["side"] == "buy"
    assert order["time_in_force"] == "day"


def test_limit_order(fake_alpaca_client):
    payload = {
        "symbol": "AAPL",
        "qty": 1,
        "side": "buy",
        "limit_price": 150,
        "time_in_force": "gtc",
    }

    response = client.post("/orders/limit", json=payload)

    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert response_data["message"] == "Order placed successfully"
    assert "order" in response_data

    assert len(fake_alpaca_client.orders) == 2
    order = fake_alpaca_client.orders[1]
    assert order["symbol"] == "AAPL"
    assert order["qty"] == 1
    assert order["side"] == "buy"
    assert order["limit_price"] == 150
    assert order["time_in_force"] == "gtc"
