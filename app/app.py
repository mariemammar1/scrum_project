from flask import Flask
from flask import redirect
from config import Config
from models import db
from flask_jwt_extended import JWTManager

from auth import auth_bp



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
JWTManager(app)

# Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)