import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, redirect, url_for, session, render_template
from flask_wtf.csrf import CSRFProtect
from config import Config
from routes import register_all

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)
register_all(app)

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    role = session.get("role")
    if role == "admin":
        return redirect(url_for("admin.dashboard"))
    if role == "seller":
        return redirect(url_for("seller.dashboard"))
    return redirect(url_for("customer.home"))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
