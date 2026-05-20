import sys
import os

# This fixes ModuleNotFoundError for controllers, models, utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.auth     import auth_bp
from routes.customer import customer_bp
from routes.seller   import seller_bp
from routes.admin    import admin_bp

def register_all(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(seller_bp)
    app.register_blueprint(admin_bp)