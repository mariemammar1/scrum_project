from flask import Flask
from flask import redirect
from config import Config
from models import db
from flask_jwt_extended import JWTManager

from auth import auth_bp
from admin import admin_bp
from category import category_bp
from article import article_bp
from secondary import secondary_bp
from operations import operations_bp
from exports import export_bp
from inventory import inventory_bp
from statistics import statistics_bp
from frontend import frontend_bp


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
JWTManager(app)

# Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(category_bp, url_prefix="/api")
app.register_blueprint(article_bp, url_prefix="/api")
app.register_blueprint(secondary_bp, url_prefix="/api")
app.register_blueprint(operations_bp, url_prefix="/api")
app.register_blueprint(export_bp, url_prefix="/api")
app.register_blueprint(inventory_bp, url_prefix="/api")
app.register_blueprint(statistics_bp, url_prefix="/api")
app.register_blueprint(frontend_bp)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)