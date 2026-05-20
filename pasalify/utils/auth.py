from functools import wraps
from flask import session, redirect, url_for, flash

# ═══════════════════════════════════════════
#  OOP — Role Guard Decorator Factory
# ═══════════════════════════════════════════
class RoleGuard:
    @staticmethod
    def require(*roles):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                if "user_id" not in session:
                    flash("Please login first.", "warning")
                    return redirect(url_for("auth.login"))
                if session.get("role") not in roles:
                    flash("Access denied.", "danger")
                    return redirect(url_for("index"))
                return f(*args, **kwargs)
            return wrapper
        return decorator

guard = RoleGuard()
login_required  = guard.require("customer", "seller", "admin")
customer_only   = guard.require("customer")
seller_only     = guard.require("seller")
admin_only      = guard.require("admin")
