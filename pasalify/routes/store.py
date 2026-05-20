from flask import Blueprint, render_template, redirect, url_for, flash
from modals.store import SELLERS, PRODUCTS, CHATS

store_bp = Blueprint("store", __name__, url_prefix="/store")

@store_bp.route("/<slug>")
def public(slug):
    store = next((s for s in SELLERS.values()
                  if s["slug"] == slug), None)
    if not store:
        flash("Store not found.", "danger")
        return redirect(url_for("auth.login"))
    prods = [p for p in PRODUCTS.values()
             if p["seller_id"] == store["user_id"]
             and p["is_approved"]]
    return render_template("store/public.html",
                           store=store, products=prods)

@store_bp.route("/<slug>/chat")
def chat(slug):
    store = next((s for s in SELLERS.values()
                  if s["slug"] == slug), None)
    return render_template("store/chat.html", store=store)
