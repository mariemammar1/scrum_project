from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models import db, Article

inventory_bp = Blueprint("inventory", __name__)

# US38 - Global inventory
@inventory_bp.route("/inventory", methods=["GET"])
@jwt_required()
def global_inventory():
    articles = Article.query.all()

    return [{
        "id": a.id,
        "title": a.title,
        "stock": a.stock,
        "price": a.price
    } for a in articles]





# US39 - Manage inventory line (manual update)
@inventory_bp.route("/inventory/<int:id>", methods=["PUT"])
@jwt_required()
def update_inventory(id):
    article = Article.query.get_or_404(id)
    article.stock = request.json["stock"]

    db.session.commit()
    return {"message": "Stock updated"}
@inventory_bp.route("/inventory/low", methods=["GET"])
@jwt_required()
def low_stock():
    threshold = request.args.get("threshold", 5)

    articles = Article.query.filter(Article.stock <= threshold).all()

    return [{
        "id": a.id,
        "title": a.title,
        "stock": a.stock
    } for a in articles]