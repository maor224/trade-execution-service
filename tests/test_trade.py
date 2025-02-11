from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Trade Execution Service is up and running"}

def test_execute_trade():
    trade_data = {"symbol": "AAPL", "qty": 1, "side": "buy"}
    response = client.post("/api/trade", json=trade_data)
    assert response.status_code == 200
    assert "order" in response.json()
