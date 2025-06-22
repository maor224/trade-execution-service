from typing import Dict, List


class FakeAlpacaClient:
    def __init__(self):
        self.orders: List[Dict] = []

    def submit_order(self, order_data):
        order = {
            "id": f"order_{len(self.orders) + 1}",
            "status": "accepted",
            **order_data.dict(),
        }
        self.orders.append(order)
        return order
