from flask import (Blueprint, render_template, redirect,
                   url_for, session, flash, request)
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from controllers.admin_controllers import admin_ctrl
from utils.auth import admin_only

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

class PromoForm(FlaskForm):
    code     = StringField("Promo Code",    validators=[DataRequired()])
    discount = IntegerField("Discount (%)", validators=[DataRequired(),
                                                        NumberRange(1, 100)])
    submit   = SubmitField("Add Promo")

class CategoryForm(FlaskForm):
    name   = StringField("Category Name", validators=[DataRequired()])
    submit = SubmitField("Add Category")

@admin_bp.route("/dashboard")
@admin_only
def dashboard():
    stats = admin_ctrl.stats()
    return render_template("admin/dashboard.html", stats=stats)

@admin_bp.route("/sellers")
@admin_only
def sellers():
    all_sellers = admin_ctrl.all_sellers()
    return render_template("admin/sellers.html",
                           sellers=all_sellers)

@admin_bp.route("/sellers/approve/<int:uid>", methods=["POST"])
@admin_only
def approve_seller(uid):
    admin_ctrl.approve_seller(uid)
    flash("Seller approved.", "success")
    return redirect(url_for("admin.sellers"))

@admin_bp.route("/sellers/reject/<int:uid>", methods=["POST"])
@admin_only
def reject_seller(uid):
    admin_ctrl.reject_seller(uid)
    flash("Seller rejected.", "warning")
    return redirect(url_for("admin.sellers"))

@admin_bp.route("/products")
@admin_only
def products():
    prods = admin_ctrl.all_products()
    return render_template("admin/products.html", products=prods)

@admin_bp.route("/products/approve/<int:pid>", methods=["POST"])
@admin_only
def approve_product(pid):
    admin_ctrl.approve_product(pid)
    flash("Product approved.", "success")
    return redirect(url_for("admin.products"))

@admin_bp.route("/products/delete/<int:pid>", methods=["POST"])
@admin_only
def delete_product(pid):
    admin_ctrl.delete_product(pid)
    flash("Product deleted.", "info")
    return redirect(url_for("admin.products"))

@admin_bp.route("/users")
@admin_only
def users():
    all_users = admin_ctrl.all_users()
    return render_template("admin/users.html", users=all_users)

@admin_bp.route("/users/delete/<int:uid>", methods=["POST"])
@admin_only
def delete_user(uid):
    admin_ctrl.delete_user(uid)
    flash("User deleted.", "info")
    return redirect(url_for("admin.users"))

@admin_bp.route("/finances")
@admin_only
def finances():
    data = admin_ctrl.finances()
    return render_template("admin/finances.html", data=data)

@admin_bp.route("/promos", methods=["GET", "POST"])
@admin_only
def promos():
    form  = PromoForm()
    if form.validate_on_submit():
        admin_ctrl.add_promo(form.code.data, form.discount.data)
        flash("Promo added!", "success")
        return redirect(url_for("admin.promos"))
    all_promos = admin_ctrl.all_promos()
    return render_template("admin/promos.html",
                           form=form, promos=all_promos)

@admin_bp.route("/promos/delete/<code>", methods=["POST"])
@admin_only
def delete_promo(code):
    admin_ctrl.delete_promo(code)
    return redirect(url_for("admin.promos"))

@admin_bp.route("/categories", methods=["GET", "POST"])
@admin_only
def categories():
    form = CategoryForm()
    if form.validate_on_submit():
        admin_ctrl.add_category(form.name.data)
        flash("Category added!", "success")
        return redirect(url_for("admin.categories"))
    cats = admin_ctrl.all_categories()
    return render_template("admin/categories.html",
                           form=form, categories=cats)

@admin_bp.route("/categories/delete/<name>", methods=["POST"])
@admin_only
def delete_category(name):
    admin_ctrl.delete_category(name)
    return redirect(url_for("admin.categories"))

@admin_bp.route("/system")
@admin_only
def system():
    return render_template("admin/system.html")
