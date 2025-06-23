import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.utils.alpaca_client import get_alpaca_client
from tests.fakes.fake_alpaca_client import FakeAlpacaClient


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


def test_get_positions():
    response = client.get("/positions")

    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list)
