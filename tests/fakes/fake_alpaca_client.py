from typing import Dict, List


class FakeAlpacaClient:
    def __init__(self):
        self.orders: List[Dict] = []
        self.positions: List[Dict] = []

    def submit_order(self, order_data):
        order = {
            "id": f"order_{len(self.orders) + 1}",
            "status": "accepted",
            **order_data.dict(),
        }
        self.orders.append(order)
        return order

    def get_orders(self):
        return self.orders

    def get_all_positions(self):
        return self.positions
