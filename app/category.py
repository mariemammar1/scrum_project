from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models import db, Category, SubCategory

category_bp = Blueprint("category", __name__)

# ➕ Create Category (US7)
@category_bp.route("/categories", methods=["POST"])
@jwt_required()
def create_category():
    cat = Category(name=request.json["name"])
    db.session.add(cat)
    db.session.commit()
    return {"message": "Category created"}


# ✏️ Edit Category (US8)
@category_bp.route("/categories/<int:id>", methods=["PUT"])
@jwt_required()
def edit_category(id):
    cat = Category.query.get_or_404(id)
    cat.name = request.json["name"]
    db.session.commit()
    return {"message": "Category updated"}


# 🗑 Delete Category (US9)
@category_bp.route("/categories/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_category(id):
    cat = Category.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    return {"message": "Category deleted"}


# 📋 List Categories (US10)
@category_bp.route("/categories", methods=["GET"])
@jwt_required()
def list_categories():
    cats = Category.query.all()
    return [{"id": c.id, "name": c.name} for c in cats]


# 📂 Create SubCategory (US11)
@category_bp.route("/subcategories", methods=["POST"])
@jwt_required()
def create_subcategory():
    sub = SubCategory(
        name=request.json["name"],
        category_id=request.json["category_id"]
    )
    db.session.add(sub)
    db.session.commit()
    return {"message": "Subcategory created"}