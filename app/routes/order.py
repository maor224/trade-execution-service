import traceback

from alpaca.trading.requests import LimitOrderRequest, MarketOrderRequest
from fastapi import APIRouter, Depends

from app.utils.alpaca_client import get_alpaca_client

router = APIRouter()


@router.get("/")
def get_orders(alpaca_client=Depends(get_alpaca_client)):
    try:
        orders = alpaca_client.get_orders()
        return orders
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


@router.post("/market")
def market_order(
    market_order_request: MarketOrderRequest, alpaca_client=Depends(get_alpaca_client)
):
    try:
        order = alpaca_client.submit_order(order_data=market_order_request)
        return {"message": "Order placed successfully", "order": order}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}


@router.post("/limit")
def limit_order(
    limit_order_request: LimitOrderRequest, alpaca_client=Depends(get_alpaca_client)
):
    try:
        order = alpaca_client.submit_order(order_data=limit_order_request)
        return {"message": "Order placed successfully", "order": order}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}
