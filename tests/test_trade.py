import os
import pytest
from app.main import app
from fastapi.testclient import TestClient

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

def test_root_endpoint(mock_env_vars):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Trade Execution Service is up and running"}

def test_trade_endpoint(mock_env_vars):
    payload = {
        "symbol": "AAPL",
        "qty": 1,
        "side": "buy"
    }
    response = client.post("/trade", json=payload)
    assert response.status_code in [200, 400, 404]
    if response.status_code == 200:
        assert "order" in response.json()
    elif response.status_code == 400:
        assert "error" in response.json()
    elif response.status_code == 404:
        assert "detail" in response.json()
