import hashlib
from datetime import datetime

# ═══════════════════════════════════════════
#  OOP — Password Manager
# ═══════════════════════════════════════════
class PasswordManager:
    @staticmethod
    def hash(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify(stored: str, provided: str) -> bool:
        return stored == hashlib.sha256(provided.encode()).hexdigest()

pm = PasswordManager()

# ═══════════════════════════════════════════
#  OOP — ID Counter
# ═══════════════════════════════════════════
class IDCounter:
    def __init__(self):
        self._counters = {
            "user": 3, "product": 4,
            "order": 2, "review": 1,
            "notif": 3, "chat": 1, "promo": 2
        }

    def next(self, k: str) -> int:
        self._counters[k] += 1
        return self._counters[k]

counter = IDCounter()

# ═══════════════════════════════════════════
#  DATA STORE
# ═══════════════════════════════════════════

USERS = {
    1: {
        "id": 1, "name": "Admin User",
        "email": "admin@pasalify.com",
        "password": pm.hash("admin123"),
        "role": "admin", "phone": "",
        "address": "", "created_at": "2026-01-01"
    },
    2: {
        "id": 2, "name": "Demo Seller",
        "email": "seller@pasalify.com",
        "password": pm.hash("seller123"),
        "role": "seller", "phone": "",
        "address": "", "created_at": "2026-01-01"
    },
    3: {
        "id": 3, "name": "Demo Customer",
        "email": "customer@pasalify.com",
        "password": pm.hash("customer123"),
        "role": "customer", "phone": "",
        "address": "", "created_at": "2026-01-01"
    },
}

SELLERS = {
    2: {
        "id": 2, "user_id": 2,
        "store_name": "Demo Store", "slug": "demo-store",
        "description": "Best products in Nepal!",
        "theme_color": "#6c5ce7",
        "is_approved": True, "commission_rate": 10,
        "total_sales": 5000, "created_at": "2026-01-01"
    },
}

PRODUCTS = {
    1: {
        "id": 1, "seller_id": 2,
        "name": "Wireless Headphones", "price": 2500.0,
        "category": "Electronics",
        "description": "High-quality wireless headphones.",
        "stock": 20, "rating": 4.5,
        "reviews_count": 8, "is_approved": True,
        "created_at": "2026-01-10"
    },
    2: {
        "id": 2, "seller_id": 2,
        "name": "Cotton T-Shirt", "price": 800.0,
        "category": "Clothing",
        "description": "Comfortable 100% cotton t-shirt.",
        "stock": 50, "rating": 4.0,
        "reviews_count": 12, "is_approved": True,
        "created_at": "2026-01-12"
    },
    3: {
        "id": 3, "seller_id": 2,
        "name": "Python Programming Book", "price": 1200.0,
        "category": "Books",
        "description": "Complete Python guide.",
        "stock": 15, "rating": 4.8,
        "reviews_count": 20, "is_approved": True,
        "created_at": "2026-01-14"
    },
    4: {
        "id": 4, "seller_id": 2,
        "name": "Stainless Steel Bottle", "price": 600.0,
        "category": "Home & Kitchen",
        "description": "Eco-friendly insulated bottle.",
        "stock": 30, "rating": 4.3,
        "reviews_count": 6, "is_approved": True,
        "created_at": "2026-01-15"
    },
}

CARTS     = {}   # { user_id: { product_id: qty } }
WISHLISTS = {}   # { user_id: [product_id, ...] }

ORDERS = {
    1: {
        "id": 1, "user_id": 3,
        "address": "Lalitpur, Nepal",
        "payment_method": "COD",
        "status": "Delivered", "total": 3300.0,
        "items": [
            {"product_id": 1, "name": "Wireless Headphones",
             "price": 2500.0, "quantity": 1},
            {"product_id": 4, "name": "Stainless Steel Bottle",
             "price": 600.0, "quantity": 1},
        ],
        "created_at": "2026-01-20"
    },
    2: {
        "id": 2, "user_id": 3,
        "address": "Lalitpur, Nepal",
        "payment_method": "eSewa",
        "status": "Processing", "total": 800.0,
        "items": [
            {"product_id": 2, "name": "Cotton T-Shirt",
             "price": 800.0, "quantity": 1},
        ],
        "created_at": "2026-01-22"
    },
}

REVIEWS = {}   # { product_id: [ {review dict} ] }

NOTIFICATIONS = {
    3: [
        {"id": 1, "message": "Your order #1 has been delivered!", "read": False, "date": "2026-01-21"},
        {"id": 2, "message": "New product added to your wishlist category.", "read": False, "date": "2026-01-22"},
        {"id": 3, "message": "Promo code SAVE10 is expiring soon!", "read": True,  "date": "2026-01-23"},
    ]
}

CHATS = {}   # { chat_id: { seller_id, customer_id, messages: [] } }

CATEGORIES = [
    "Electronics", "Clothing", "Books",
    "Home & Kitchen", "Sports", "Beauty"
]

PROMO_CODES = {
    "SAVE10":  10,
    "SAVE20":  20,
    "WELCOME": 15,
    "NEPAL25": 25
}
