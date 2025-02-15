import os
import pytest
from app.config.settings import Settings
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def mock_env_vars():
    os.environ["ALPACA_API_KEY"] = "test_api_key"
    os.environ["ALPACA_SECRET_KEY"] = "test_secret_key"
    os.environ["ALPACA_BASE_URL"] = "https://paper-api.alpaca.markets"

def test_settings():
    settings = Settings()
    assert settings.ALPACA_API_KEY == "test_api_key"
    assert settings.ALPACA_SECRET_KEY == "test_secret_key"
    assert settings.ALPACA_BASE_URL == "https://paper-api.alpaca.markets"

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Trade Execution Service is up and running"}

def test_trade_endpoint():
    payload = {
        "symbol": "AAPL",
        "qty": 1,
        "side": "buy"
    }
    response = client.post("/trade", json=payload)
    assert response.status_code == 200 or response.status_code == 400
    if response.status_code == 200:
        assert "order" in response.json()
    elif response.status_code == 400:
        assert "error" in response.json()
