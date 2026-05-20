from modals.store import (USERS, SELLERS, PRODUCTS,
                           ORDERS, PROMO_CODES,
                           CATEGORIES, counter)
from datetime import datetime

class AdminController:

    # ── Users ─────────────────────────────────
    @staticmethod
    def all_users():
        return list(USERS.values())

    @staticmethod
    def delete_user(uid: int):
        USERS.pop(int(uid), None)

    # ── Sellers ───────────────────────────────
    @staticmethod
    def all_sellers():
        return list(SELLERS.values())

    @staticmethod
    def approve_seller(uid: int):
        if uid in SELLERS:
            SELLERS[uid]["is_approved"] = True

    @staticmethod
    def reject_seller(uid: int):
        if uid in SELLERS:
            SELLERS[uid]["is_approved"] = False

    # ── Products ──────────────────────────────
    @staticmethod
    def all_products():
        return list(PRODUCTS.values())

    @staticmethod
    def approve_product(pid: int):
        if pid in PRODUCTS:
            PRODUCTS[pid]["is_approved"] = True

    @staticmethod
    def delete_product(pid: int):
        PRODUCTS.pop(int(pid), None)

    # ── Finances ──────────────────────────────
    @staticmethod
    def finances():
        total_revenue = sum(o["total"] for o in ORDERS.values())
        total_orders  = len(ORDERS)
        return {
            "total_revenue": total_revenue,
            "total_orders":  total_orders,
            "orders": list(ORDERS.values())
        }

    # ── Promos ────────────────────────────────
    @staticmethod
    def all_promos():
        return PROMO_CODES

    @staticmethod
    def add_promo(code: str, discount: int):
        PROMO_CODES[code.upper()] = int(discount)

    @staticmethod
    def delete_promo(code: str):
        PROMO_CODES.pop(code.upper(), None)

    # ── Categories ────────────────────────────
    @staticmethod
    def all_categories():
        return CATEGORIES

    @staticmethod
    def add_category(name: str):
        if name not in CATEGORIES:
            CATEGORIES.append(name)

    @staticmethod
    def delete_category(name: str):
        if name in CATEGORIES:
            CATEGORIES.remove(name)

    # ── Dashboard Stats ───────────────────────
    @staticmethod
    def stats():
        return {
            "users":    len(USERS),
            "sellers":  len(SELLERS),
            "products": len(PRODUCTS),
            "orders":   len(ORDERS),
            "revenue":  sum(o["total"] for o in ORDERS.values())
        }

admin_ctrl = AdminController()
