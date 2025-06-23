from fastapi import FastAPI

from app.routes.order import router as order_router
from app.routes.position import router as position_router

app = FastAPI(title="Trade Execution Service", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "Trade Execution Service is up and running"}


app.include_router(order_router, prefix="/orders", tags=["Order"])
app.include_router(position_router, prefix="/positions", tags=["Position"])
