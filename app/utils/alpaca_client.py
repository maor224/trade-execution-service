from alpaca_trade_api.rest import REST
from app.config.settings import settings

def get_alpaca_client():
    return REST(
        key_id=settings.ALPACA_API_KEY,
        secret_key=settings.ALPACA_SECRET_KEY,
        base_url=settings.ALPACA_BASE_URL,
    )
