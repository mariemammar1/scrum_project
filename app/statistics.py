from flask import Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from models import db, Article, Category, StockOperation

statistics_bp = Blueprint("statistics", __name__)


# US41 - Stats by category
@statistics_bp.route("/stats/category", methods=["GET"])
@jwt_required()
def stats_category():
    result = db.session.query(
        Category.name,
        func.count(Article.id)
    ).join(Article, Article.category_id == Category.id)\
     .group_by(Category.name).all()

    return [{"category": r[0], "count": r[1]} for r in result]


# US42 - Entry/Exit stats
@statistics_bp.route("/stats/operations", methods=["GET"])
@jwt_required()
def stats_operations():
    result = db.session.query(
        StockOperation.type,
        func.sum(StockOperation.quantity)
    ).group_by(StockOperation.type).all()

    return [{"type": r[0], "total": r[1]} for r in result]


# US44 - Dashboard KPIs
@statistics_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    total_articles = Article.query.count()
    total_stock = db.session.query(func.sum(Article.stock)).scalar() or 0

    total_entries = db.session.query(func.sum(StockOperation.quantity))\
        .filter_by(type="ENTRY").scalar() or 0

    total_exits = db.session.query(func.sum(StockOperation.quantity))\
        .filter_by(type="EXIT").scalar() or 0

    return {
        "total_articles": total_articles,
        "total_stock": total_stock,
        "entries": total_entries,
        "exits": total_exits
    }