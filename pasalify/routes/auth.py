from flask import (Blueprint, render_template, redirect,
                   url_for, session, flash, request)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from controllers.auth_controllers import auth_ctrl
from modals.store import SELLERS

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# ── Forms ─────────────────────────────────────────────────
class LoginForm(FlaskForm):
    email    = StringField("Email",    validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit   = SubmitField("Login")

class RegisterForm(FlaskForm):
    name     = StringField("Full Name", validators=[DataRequired(), Length(2, 80)])
    email    = StringField("Email",     validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 50)])
    confirm  = PasswordField("Confirm",
                             validators=[DataRequired(), EqualTo("password")])
    role     = SelectField("Register As",
                           choices=[("customer", "Customer"),
                                    ("seller",   "Seller")])
    submit   = SubmitField("Register")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField("New Password",
                                 validators=[DataRequired(), Length(6, 50)])
    confirm      = PasswordField("Confirm",
                                 validators=[DataRequired(),
                                             EqualTo("new_password")])
    submit       = SubmitField("Change Password")

class ForgotForm(FlaskForm):
    email  = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Send Reset Link")

# ── Routes ────────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = auth_ctrl.verify(form.email.data, form.password.data)
        if user:
            session["user_id"] = user["id"]
            session["name"]    = user["name"]
            session["role"]    = user["role"]
            session.permanent  = True
            flash(f"Welcome back, {user['name']}!", "success")
            if user["role"] == "admin":
                return redirect(url_for("admin.dashboard"))
            if user["role"] == "seller":
                if user["id"] not in SELLERS:
                    return redirect(url_for("seller.setup"))
                return redirect(url_for("seller.dashboard"))
            return redirect(url_for("customer.home"))
        flash("Invalid email or password.", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if auth_ctrl.email_exists(form.email.data):
            flash("Email already registered.", "warning")
        else:
            user = auth_ctrl.register(
                form.name.data, form.email.data,
                form.password.data, form.role.data
            )
            flash("Registered successfully! Please login.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotForm()
    if form.validate_on_submit():
        flash("If that email exists, a reset link has been sent.", "info")
    return render_template("auth/forgot_password.html", form=form)

@auth_bp.route("/change-password", methods=["GET", "POST"])
def change_password():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        ok = auth_ctrl.change_password(
            session["user_id"],
            form.old_password.data,
            form.new_password.data
        )
        if ok:
            flash("Password changed successfully!", "success")
            return redirect(url_for("auth.login"))
        flash("Old password is incorrect.", "danger")
    return render_template("auth/change_password.html", form=form)

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
