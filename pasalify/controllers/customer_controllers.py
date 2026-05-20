from modals.store import (PRODUCTS, CARTS, WISHLISTS,
                           ORDERS, NOTIFICATIONS,
                           PROMO_CODES, REVIEWS, counter)
from datetime import datetime

class CustomerController:

    # ── Products ──────────────────────────────
    @staticmethod
    def all_products(search="", category=""):
        prods = [p for p in PRODUCTS.values() if p["is_approved"]]
        if search:
            prods = [p for p in prods
                     if search.lower() in p["name"].lower()]
        if category:
            prods = [p for p in prods
                     if p["category"] == category]
        return prods

    @staticmethod
    def get_product(pid: int):
        return PRODUCTS.get(int(pid))

    # ── Cart ──────────────────────────────────
    @staticmethod
    def get_cart(uid: int):
        cart = CARTS.get(uid, {})
        items = []
        total = 0.0
        for pid, qty in cart.items():
            p = PRODUCTS.get(pid)
            if p:
                subtotal = p["price"] * qty
                total += subtotal
                items.append({**p, "qty": qty, "subtotal": subtotal})
        return items, round(total, 2)

    @staticmethod
    def add_to_cart(uid: int, pid: int, qty: int = 1):
        CARTS.setdefault(uid, {})
        CARTS[uid][pid] = CARTS[uid].get(pid, 0) + qty

    @staticmethod
    def remove_from_cart(uid: int, pid: int):
        CARTS.get(uid, {}).pop(pid, None)

    @staticmethod
    def clear_cart(uid: int):
        CARTS[uid] = {}

    # ── Wishlist ──────────────────────────────
    @staticmethod
    def get_wishlist(uid: int):
        ids = WISHLISTS.get(uid, [])
        return [PRODUCTS[i] for i in ids if i in PRODUCTS]

    @staticmethod
    def toggle_wishlist(uid: int, pid: int):
        WISHLISTS.setdefault(uid, [])
        if pid in WISHLISTS[uid]:
            WISHLISTS[uid].remove(pid)
        else:
            WISHLISTS[uid].append(pid)

    # ── Orders ────────────────────────────────
    @staticmethod
    def place_order(uid: int, address: str,
                    payment: str, promo: str):
        items, total = CustomerController.get_cart(uid)
        discount = 0
        if promo in PROMO_CODES:
            discount = round(total * PROMO_CODES[promo] / 100, 2)
        final = round(total - discount, 2)
        oid = counter.next("order")
        ORDERS[oid] = {
            "id": oid, "user_id": uid,
            "address": address, "payment_method": payment,
            "status": "Processing", "total": final,
            "discount": discount,
            "items": [
                {"product_id": i["id"], "name": i["name"],
                 "price": i["price"], "quantity": i["qty"]}
                for i in items
            ],
            "created_at": datetime.now().strftime("%Y-%m-%d")
        }
        CustomerController.clear_cart(uid)
        return ORDERS[oid]

    @staticmethod
    def get_orders(uid: int):
        return [o for o in ORDERS.values() if o["user_id"] == uid]

    @staticmethod
    def get_order(oid: int):
        return ORDERS.get(int(oid))

    # ── Notifications ─────────────────────────
    @staticmethod
    def get_notifications(uid: int):
        return NOTIFICATIONS.get(uid, [])

    @staticmethod
    def mark_read(uid: int, nid: int):
        for n in NOTIFICATIONS.get(uid, []):
            if n["id"] == nid:
                n["read"] = True

cust_ctrl = CustomerController()
