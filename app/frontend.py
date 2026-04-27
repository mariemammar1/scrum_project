from flask import Blueprint, render_template, request, redirect
from models import db, User, Article, StockOperation
from werkzeug.security import generate_password_hash

frontend_bp = Blueprint("frontend", __name__)


# ---------------- LOGIN PAGE ----------------
@frontend_bp.route("/login")
def login_page():
    return render_template("login.html")


# ---------------- REGISTER PAGE ----------------
@frontend_bp.route("/register")
def register_page():
    return render_template("register.html")


@frontend_bp.route("/register", methods=["POST"])
def register_user():
    data = request.form

    user = User(
        username=data["username"],
        role="User"
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return redirect("/login")


# ---------------- DASHBOARD (ONLY ONE) ----------------
@frontend_bp.route("/dashboard")
def dashboard_page():
    total_articles = Article.query.count()
    total_stock = sum([a.stock for a in Article.query.all()])

    entries = StockOperation.query.filter_by(type="ENTRY").count()
    exits = StockOperation.query.filter_by(type="EXIT").count()

    return render_template(
        "dashboard.html",
        total_articles=total_articles,
        total_stock=total_stock,
        entries=entries,
        exits=exits
    )


# ---------------- INVENTORY ----------------
@frontend_bp.route("/inventory")
def inventory_page():
    articles = Article.query.all()
    return render_template("inventory.html", articles=articles)


# ➕ CREATE ARTICLE (NEW)
@frontend_bp.route("/article/create", methods=["POST"])
def create_article():
    data = request.form

    article = Article(
        title=data["title"],
        content=data["content"],
        price=float(data["price"]),
        stock=int(data["stock"]),
        category_id=1,
        subcategory_id=1
    )

    db.session.add(article)
    db.session.commit()

    return redirect("/inventory")


# 📥 STOCK ENTRY (NEW)
@frontend_bp.route("/stock/entry", methods=["POST"])
def stock_entry():
    data = request.form
    article = Article.query.get(data["article_id"])

    article.stock += int(data["quantity"])

    op = StockOperation(type="ENTRY", quantity=data["quantity"], article_id=article.id)

    db.session.add(op)
    db.session.commit()

    return redirect("/inventory")


# 📤 STOCK EXIT (NEW)
@frontend_bp.route("/stock/exit", methods=["POST"])
def stock_exit():
    data = request.form
    article = Article.query.get(data["article_id"])

    qty = int(data["quantity"])

    if article.stock >= qty:
        article.stock -= qty

        op = StockOperation(type="EXIT", quantity=qty, article_id=article.id)
        db.session.add(op)
        db.session.commit()

    return redirect("/inventory")