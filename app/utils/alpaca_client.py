from app.config.settings import get_settings
from alpaca_trade_api import REST

def get_alpaca_client():
    settings = get_settings()
    return REST(
        key_id=settings.ALPACA_API_KEY,
        secret_key=settings.ALPACA_SECRET_KEY,
        base_url=settings.ALPACA_BASE_URL,
    )
