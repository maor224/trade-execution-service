from alpaca.trading.client import TradingClient

from app.config.settings import get_settings


def get_alpaca_client():
    settings = get_settings()
    return TradingClient(
        api_key=settings.ALPACA_API_KEY,
        secret_key=settings.ALPACA_SECRET_KEY,
        paper=True,
    )
