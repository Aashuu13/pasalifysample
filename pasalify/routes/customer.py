from flask import (Blueprint, render_template, redirect,
                   url_for, session, flash, request)
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from controllers.customer_controllers import cust_ctrl
from modals.store import CATEGORIES, USERS
from utils.auth import customer_only

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")

class CheckoutForm(FlaskForm):
    address        = StringField("Address",  validators=[DataRequired()])
    payment_method = SelectField("Payment",
                                 choices=[("COD","Cash on Delivery"),
                                          ("eSewa","eSewa"),
                                          ("Khalti","Khalti")])
    promo_code     = StringField("Promo Code")
    submit         = SubmitField("Place Order")

class SupportForm(FlaskForm):
    subject = StringField("Subject",  validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit  = SubmitField("Send")

@customer_bp.route("/home")
@customer_only
def home():
    products = cust_ctrl.all_products()
    return render_template("customer/home.html", products=products)

@customer_bp.route("/products")
@customer_only
def products():
    search   = request.args.get("search", "")
    category = request.args.get("category", "")
    prods    = cust_ctrl.all_products(search, category)
    return render_template("customer/products.html",
                           products=prods,
                           categories=CATEGORIES,
                           search=search,
                           selected_cat=category)

@customer_bp.route("/product/<int:pid>")
@customer_only
def product_detail(pid):
    product = cust_ctrl.get_product(pid)
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for("customer.products"))
    return render_template("customer/product_detail.html",
                           product=product)

@customer_bp.route("/cart")
@customer_only
def cart():
    items, total = cust_ctrl.get_cart(session["user_id"])
    return render_template("customer/cart.html",
                           items=items, total=total)

@customer_bp.route("/cart/add/<int:pid>", methods=["POST"])
@customer_only
def add_to_cart(pid):
    cust_ctrl.add_to_cart(session["user_id"], pid)
    flash("Added to cart!", "success")
    return redirect(url_for("customer.cart"))

@customer_bp.route("/cart/remove/<int:pid>", methods=["POST"])
@customer_only
def remove_from_cart(pid):
    cust_ctrl.remove_from_cart(session["user_id"], pid)
    return redirect(url_for("customer.cart"))

@customer_bp.route("/wishlist")
@customer_only
def wishlist():
    items = cust_ctrl.get_wishlist(session["user_id"])
    return render_template("customer/wishlist.html", items=items)

@customer_bp.route("/wishlist/toggle/<int:pid>", methods=["POST"])
@customer_only
def toggle_wishlist(pid):
    cust_ctrl.toggle_wishlist(session["user_id"], pid)
    return redirect(url_for("customer.wishlist"))

@customer_bp.route("/checkout", methods=["GET", "POST"])
@customer_only
def checkout():
    form  = CheckoutForm()
    items, total = cust_ctrl.get_cart(session["user_id"])
    if not items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("customer.cart"))
    if form.validate_on_submit():
        order = cust_ctrl.place_order(
            session["user_id"],
            form.address.data,
            form.payment_method.data,
            form.promo_code.data.upper()
        )
        flash("Order placed successfully!", "success")
        return redirect(url_for("customer.order_detail",
                                oid=order["id"]))
    return render_template("customer/checkout.html",
                           form=form, items=items, total=total)

@customer_bp.route("/orders")
@customer_only
def orders():
    my_orders = cust_ctrl.get_orders(session["user_id"])
    return render_template("customer/orders.html",
                           orders=my_orders)

@customer_bp.route("/orders/<int:oid>")
@customer_only
def order_detail(oid):
    order = cust_ctrl.get_order(oid)
    return render_template("customer/order_detail.html",
                           order=order)

@customer_bp.route("/payment-history")
@customer_only
def payment_history():
    my_orders = cust_ctrl.get_orders(session["user_id"])
    paid = [o for o in my_orders
            if o["payment_method"] != "COD"]
    return render_template("customer/payment_history.html",
                           orders=paid)

@customer_bp.route("/profile")
@customer_only
def profile():
    user = USERS.get(session["user_id"])
    return render_template("customer/profile.html", user=user)

@customer_bp.route("/notifications")
@customer_only
def notifications():
    notifs = cust_ctrl.get_notifications(session["user_id"])
    return render_template("customer/notifications.html",
                           notifications=notifs)

@customer_bp.route("/support", methods=["GET", "POST"])
@customer_only
def support():
    form = SupportForm()
    if form.validate_on_submit():
        flash("Support ticket submitted!", "success")
        return redirect(url_for("customer.support"))
    return render_template("customer/support.html", form=form)
