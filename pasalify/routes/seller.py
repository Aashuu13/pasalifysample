from flask import (Blueprint, render_template, redirect,
                   url_for, session, flash, request)
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, FloatField,
                     IntegerField, SelectField, SubmitField)
from wtforms.validators import DataRequired, NumberRange
from controllers.seller_controllers import seller_ctrl
from modals.store import CATEGORIES
from utils.auth import seller_only

seller_bp = Blueprint("seller", __name__, url_prefix="/seller")

class SetupForm(FlaskForm):
    store_name  = StringField("Store Name",  validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit      = SubmitField("Create Store")

class ProductForm(FlaskForm):
    name        = StringField("Product Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    price       = FloatField("Price",   validators=[DataRequired(),
                                                    NumberRange(min=1)])
    stock       = IntegerField("Stock", validators=[DataRequired(),
                                                    NumberRange(min=0)])
    category    = SelectField("Category", choices=[])
    submit      = SubmitField("Save Product")

class CustomizeForm(FlaskForm):
    theme_color = StringField("Theme Color", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit      = SubmitField("Save")

@seller_bp.route("/setup", methods=["GET", "POST"])
@seller_only
def setup():
    form = SetupForm()
    if form.validate_on_submit():
        seller_ctrl.create_store(
            session["user_id"],
            form.store_name.data,
            form.description.data
        )
        flash("Store created! Awaiting admin approval.", "success")
        return redirect(url_for("seller.dashboard"))
    return render_template("seller/setup.html", form=form)

@seller_bp.route("/dashboard")
@seller_only
def dashboard():
    store    = seller_ctrl.get_store(session["user_id"])
    products = seller_ctrl.get_products(session["user_id"])
    orders   = seller_ctrl.get_orders(session["user_id"])
    return render_template("seller/dashboard.html",
                           store=store,
                           products=products,
                           orders=orders)

@seller_bp.route("/store-profile")
@seller_only
def store_profile():
    store = seller_ctrl.get_store(session["user_id"])
    return render_template("seller/store_profile.html", store=store)

@seller_bp.route("/customize", methods=["GET", "POST"])
@seller_only
def store_customize():
    form  = CustomizeForm()
    store = seller_ctrl.get_store(session["user_id"])
    if form.validate_on_submit():
        seller_ctrl.update_store(session["user_id"], {
            "theme_color": form.theme_color.data,
            "description": form.description.data
        })
        flash("Store customized!", "success")
        return redirect(url_for("seller.store_customize"))
    return render_template("seller/store_customize.html",
                           form=form, store=store)

@seller_bp.route("/products")
@seller_only
def products():
    prods = seller_ctrl.get_products(session["user_id"])
    return render_template("seller/products.html", products=prods)

@seller_bp.route("/products/add", methods=["GET", "POST"])
@seller_bp.route("/products/edit/<int:pid>", methods=["GET", "POST"])
@seller_only
def product_form(pid=None):
    form = ProductForm()
    form.category.choices = [(c, c) for c in CATEGORIES]
    if form.validate_on_submit():
        if pid:
            seller_ctrl.update_product(pid, {
                "name": form.name.data,
                "description": form.description.data,
                "price": form.price.data,
                "stock": form.stock.data,
                "category": form.category.data
            })
            flash("Product updated!", "success")
        else:
            seller_ctrl.add_product(
                session["user_id"],
                form.name.data, form.price.data,
                form.category.data,
                form.description.data,
                form.stock.data
            )
            flash("Product added!", "success")
        return redirect(url_for("seller.products"))
    return render_template("seller/product_form.html",
                           form=form, pid=pid)

@seller_bp.route("/products/delete/<int:pid>", methods=["POST"])
@seller_only
def delete_product(pid):
    seller_ctrl.delete_product(pid)
    flash("Product deleted.", "info")
    return redirect(url_for("seller.products"))

@seller_bp.route("/categories")
@seller_only
def categories():
    return render_template("seller/categories.html",
                           categories=CATEGORIES)

@seller_bp.route("/inventory")
@seller_only
def inventory():
    prods = seller_ctrl.get_products(session["user_id"])
    return render_template("seller/inventory.html", products=prods)

@seller_bp.route("/orders")
@seller_only
def orders():
    my_orders = seller_ctrl.get_orders(session["user_id"])
    return render_template("seller/orders.html", orders=my_orders)

@seller_bp.route("/orders/status/<int:oid>", methods=["POST"])
@seller_only
def update_status(oid):
    status = request.form.get("status")
    seller_ctrl.update_order_status(oid, status)
    flash("Order status updated.", "success")
    return redirect(url_for("seller.orders"))

@seller_bp.route("/reviews")
@seller_only
def reviews():
    revs = seller_ctrl.get_reviews(session["user_id"])
    return render_template("seller/reviews.html", reviews=revs)

@seller_bp.route("/chats")
@seller_only
def chats():
    my_chats = seller_ctrl.get_chats(session["user_id"])
    return render_template("seller/chats.html", chats=my_chats)

@seller_bp.route("/chats/<int:cid>")
@seller_only
def chat_detail(cid):
    from modals.store import CHATS
    chat = CHATS.get(cid, {})
    return render_template("seller/chat_detail.html", chat=chat)
