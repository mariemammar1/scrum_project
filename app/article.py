from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models import db, Article

article_bp = Blueprint("article", __name__)


# ➕ Create Article (US14)
@article_bp.route("/articles", methods=["POST"])
@jwt_required()
def create_article():
    data = request.json

    art = Article(
        title=data["title"],
        content=data["content"],
        price=data["price"],
        stock=data["stock"],
        category_id=data["category_id"],
        subcategory_id=data["subcategory_id"]
    )

    db.session.add(art)
    db.session.commit()
    return {"message": "Article created"}


# ✏️ Edit Article (US15)
@article_bp.route("/articles/<int:id>", methods=["PUT"])
@jwt_required()
def edit_article(id):
    art = Article.query.get_or_404(id)
    data = request.json

    art.title = data["title"]
    art.content = data["content"]
    art.price = data["price"]
    art.stock = data["stock"]

    db.session.commit()
    return {"message": "Article updated"}


# 🗑 Delete Article (US16)
@article_bp.route("/articles/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_article(id):
    art = Article.query.get_or_404(id)
    db.session.delete(art)
    db.session.commit()
    return {"message": "Article deleted"}


# 📋 List + Filters (US17)
@article_bp.route("/articles", methods=["GET"])
@jwt_required()
def list_articles():
    query = Article.query

    if request.args.get("category_id"):
        query = query.filter_by(category_id=request.args.get("category_id"))

    if request.args.get("subcategory_id"):
        query = query.filter_by(subcategory_id=request.args.get("subcategory_id"))

    return [{
        "id": a.id,
        "title": a.title,
        "price": a.price,
        "stock": a.stock
    } for a in query.all()]