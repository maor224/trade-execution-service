from fastapi import APIRouter
from app.models.trade_request import TradeRequest
from app.utils.alpaca_client import alpaca_client
import traceback

router = APIRouter()

@router.post("/trade")
def execute_trade(trade: TradeRequest):
    """
    Execute a trade: Buy or Sell
    """
    try:
        order = alpaca_client.submit_order(
            symbol=trade.symbol,
            qty=trade.qty,
            side=trade.side.value,
            type="market",
            time_in_force="gtc"
        )
        return {"message": "Order placed successfully", "order": order._raw}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}
