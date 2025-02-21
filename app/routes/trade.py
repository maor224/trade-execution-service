import traceback

from fastapi import APIRouter, Depends

from app.models.trade_request import TradeRequest
from app.utils.alpaca_client import get_alpaca_client

router = APIRouter()


@router.post("/trade")
def execute_trade(trade: TradeRequest, alpaca_client=Depends(get_alpaca_client)):
    try:
        order = alpaca_client.submit_order(
            symbol=trade.symbol,
            qty=trade.qty,
            side=trade.side.value,
            type="market",
            time_in_force="gtc",
        )
        return {"message": "Order placed successfully", "order": order._raw}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}
