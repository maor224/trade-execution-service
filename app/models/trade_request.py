from pydantic import BaseModel, Field

from app.models.enums import TradeSide


class TradeRequest(BaseModel):
    symbol: str = Field(..., example="AAPL")
    qty: int = Field(..., gt=0, example=10)
    side: TradeSide = Field(..., example="buy")
