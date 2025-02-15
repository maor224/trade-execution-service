from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from app.config.settings import get_settings
from app.main import app
from app.utils.alpaca_client import get_alpaca_client
from tests.mock_settings import MockSettings

@pytest.fixture(scope="module")
def mock_alpaca_client():
    mock_client = MagicMock()
    mock_client.submit_order.return_value = MagicMock(_raw={"id": "test_order_id"})
    return mock_client

@pytest.fixture(scope="module", autouse=True)
def override_settings_dependency(mock_alpaca_client):
    def mock_get_settings():
        return MockSettings(
            ALPACA_API_KEY="test_api_key",
            ALPACA_SECRET_KEY="test_secret_key",
            ALPACA_BASE_URL="https://paper-api.alpaca.markets",
        )

    app.dependency_overrides[get_settings] = mock_get_settings

    def mock_get_alpaca_client():
        return mock_alpaca_client

    app.dependency_overrides[get_alpaca_client] = mock_get_alpaca_client
    yield
    app.dependency_overrides.clear()


client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Trade Execution Service is up and running"}

def test_trade_endpoint(mock_alpaca_client):
    payload = {
        "symbol": "AAPL",
        "qty": 1,
        "side": "buy"
    }

    response = client.post("/api/trade", json=payload)

    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert "order" in response.json()
    elif response.status_code == 400:
        assert "error" in response.json()

    mock_alpaca_client.submit_order.assert_called_once_with(
        symbol="AAPL", qty=1, side="buy", type="market", time_in_force="gtc"
    )
