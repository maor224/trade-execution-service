import traceback

from fastapi import APIRouter, Depends

from app.utils.alpaca_client import get_alpaca_client

router = APIRouter()


@router.get("/")
def get_positions(alpaca_client=Depends(get_alpaca_client)):
    try:
        positions = alpaca_client.get_all_positions()
        return positions
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}
