from fastapi import FastAPI
from alpaca_trade_api.rest import REST, TimeFrame
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# Initialize Alpaca API client
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ALPACA_BASE_URL = os.getenv("ALPACA_BASE_URL")

alpaca_client = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_BASE_URL)

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Trade Execution Service is up and running"}

@app.post("/trade")
def execute_trade(symbol: str, qty: int, side: str):
    """
    Execute a trade: Buy or Sell
    """
    try:
        order = alpaca_client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type="market",
            time_in_force="gtc"
        )
        return {"message": "Order placed successfully", "order": order._raw}
    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}
