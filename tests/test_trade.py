import os
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.trade_request import TradeRequest
from app.models.enums import TradeSide
from app.utils.alpaca_client import get_alpaca_client

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def mock_env_vars():
    os.environ["ALPACA_API_KEY"] = "test_api_key"
    os.environ["ALPACA_SECRET_KEY"] = "test_secret_key"
    os.environ["ALPACA_BASE_URL"] = "https://paper-api.alpaca.markets"
    yield
    del os.environ["ALPACA_API_KEY"]
    del os.environ["ALPACA_SECRET_KEY"]
    del os.environ["ALPACA_BASE_URL"]

@pytest.fixture(scope="module")
def mock_alpaca_client():
    mock_client = MagicMock()
    mock_client.submit_order.return_value = MagicMock(_raw={"id": "test_order_id"})
    return mock_client

@pytest.fixture(scope="module", autouse=True)
def override_dependencies(mock_alpaca_client):
    app.dependency_overrides[get_alpaca_client] = lambda: mock_alpaca_client
    yield
    app.dependency_overrides.clear()

def test_trade_endpoint(mock_alpaca_client):
    trade_request = TradeRequest(symbol="AAPL", qty=1, side=TradeSide.BUY)

    response = client.post("/api/trade", json=trade_request.model_dump())
    assert response.status_code == 200
    assert response.json()["order"] == {"id": "test_order_id"}

    mock_alpaca_client.submit_order.assert_called_once_with(
        symbol="AAPL", qty=1, side="buy", type="market", time_in_force="gtc"
    )
