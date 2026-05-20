from modals.store import (PRODUCTS, SELLERS, ORDERS,
                           REVIEWS, CHATS, USERS,
                           CATEGORIES, counter)
from datetime import datetime

class SellerController:

    @staticmethod
    def get_store(uid: int):
        return SELLERS.get(int(uid))

    @staticmethod
    def create_store(uid: int, store_name: str, desc: str):
        SELLERS[uid] = {
            "id": uid, "user_id": uid,
            "store_name": store_name,
            "slug": store_name.lower().replace(" ", "-"),
            "description": desc,
            "theme_color": "#6c5ce7",
            "is_approved": False,
            "commission_rate": 10,
            "total_sales": 0,
            "created_at": datetime.now().strftime("%Y-%m-%d")
        }

    @staticmethod
    def update_store(uid: int, data: dict):
        if uid in SELLERS:
            SELLERS[uid].update(data)

    @staticmethod
    def get_products(uid: int):
        return [p for p in PRODUCTS.values()
                if p["seller_id"] == int(uid)]

    @staticmethod
    def add_product(uid: int, name, price,
                    category, description, stock):
        pid = counter.next("product")
        PRODUCTS[pid] = {
            "id": pid, "seller_id": int(uid),
            "name": name, "price": float(price),
            "category": category,
            "description": description,
            "stock": int(stock), "rating": 0.0,
            "reviews_count": 0, "is_approved": True,
            "created_at": datetime.now().strftime("%Y-%m-%d")
        }
        return PRODUCTS[pid]

    @staticmethod
    def update_product(pid: int, data: dict):
        if pid in PRODUCTS:
            PRODUCTS[pid].update(data)

    @staticmethod
    def delete_product(pid: int):
        PRODUCTS.pop(pid, None)

    @staticmethod
    def get_orders(uid: int):
        return [
            o for o in ORDERS.values()
            if any(i.get("seller_id") == int(uid)
                   for i in o["items"])
        ]

    @staticmethod
    def update_order_status(oid: int, status: str):
        if oid in ORDERS:
            ORDERS[oid]["status"] = status

    @staticmethod
    def get_reviews(uid: int):
        seller_pids = {p["id"] for p in PRODUCTS.values()
                       if p["seller_id"] == int(uid)}
        result = []
        for pid, revs in REVIEWS.items():
            if pid in seller_pids:
                result.extend(revs)
        return result

    @staticmethod
    def get_chats(uid: int):
        return [c for c in CHATS.values()
                if c["seller_id"] == int(uid)]

seller_ctrl = SellerController()
