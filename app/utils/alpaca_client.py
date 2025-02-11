from alpaca_trade_api.rest import REST
from app.config.settings import settings

alpaca_client = REST(
    settings.ALPACA_API_KEY,
    settings.ALPACA_SECRET_KEY,
    base_url=settings.ALPACA_BASE_URL
)
