from fastapi import FastAPI
from app.routes.trade import router as trade_router

app = FastAPI(title="Trade Execution Service", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Trade Execution Service is up and running"}

app.include_router(trade_router, prefix="/api", tags=["Trade"])
