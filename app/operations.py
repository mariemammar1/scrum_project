from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from models import db, StockOperation, Article

operations_bp = Blueprint("operations", __name__)


# ENTRY
@operations_bp.route("/stock/entry", methods=["POST"])
@jwt_required()
def stock_entry():
    data = request.json
    article = Article.query.get_or_404(data["article_id"])

    article.stock += data["quantity"]

    op = StockOperation(
        type="ENTRY",
        quantity=data["quantity"],
        article_id=article.id
    )

    db.session.add(op)
    db.session.commit()

    return {"message": "Stock entry created"}


# EXIT
@operations_bp.route("/stock/exit", methods=["POST"])
@jwt_required()
def stock_exit():
    data = request.json
    article = Article.query.get_or_404(data["article_id"])

    if article.stock < data["quantity"]:
        return {"message": "Not enough stock"}, 400

    article.stock -= data["quantity"]

    op = StockOperation(
        type="EXIT",
        quantity=data["quantity"],
        article_id=article.id
    )

    db.session.add(op)
    db.session.commit()

    return {"message": "Stock exit created"}


# LIST
@operations_bp.route("/stock", methods=["GET"])
@jwt_required()
def list_operations():
    ops = StockOperation.query.all()

    return [{
        "id": o.id,
        "type": o.type,
        "quantity": o.quantity,
        "article_id": o.article_id,
        "date": str(o.date)
    } for o in ops]


# EDIT
@operations_bp.route("/stock/<int:id>", methods=["PUT"])
@jwt_required()
def edit_operation(id):
    op = StockOperation.query.get_or_404(id)
    op.quantity = request.json["quantity"]

    db.session.commit()
    return {"message": "Operation updated"}


# FILTER
@operations_bp.route("/stock/filter", methods=["GET"])
@jwt_required()
def filter_operations():
    query = StockOperation.query

    if request.args.get("type"):
        query = query.filter_by(type=request.args.get("type"))

    return [{
        "id": o.id,
        "type": o.type,
        "quantity": o.quantity
    } for o in query.all()]