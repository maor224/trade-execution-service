from alpaca_trade_api import REST

from app.config.settings import get_settings


def get_alpaca_client():
    settings = get_settings()
    return REST(
        key_id=settings.ALPACA_API_KEY,
        secret_key=settings.ALPACA_SECRET_KEY,
        base_url=settings.ALPACA_BASE_URL,
    )
