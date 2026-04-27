from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# USER
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="User")
    is_deleted = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# CATEGORY
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


# ARTICLE
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)

    price = db.Column(db.Float)
    stock = db.Column(db.Integer, index=True)  # ✅ index

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), index=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'))


# SPRINT 2B
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(50))
    salary = db.Column(db.Float)


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact = db.Column(db.String(100))


# ✅ SPRINT 3
class StockOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  # ENTRY / EXIT
    quantity = db.Column(db.Integer)

    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    date = db.Column(db.DateTime, default=db.func.now())