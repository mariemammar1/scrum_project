from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from models import db, User

admin_bp = Blueprint("admin", __name__)

def is_admin():
    return get_jwt().get("role") == "Admin"


@admin_bp.route("/users", methods=["POST"])
@jwt_required()
def create_user():
    if not is_admin():
        return {"message": "Forbidden"}, 403

    data = request.json
    user = User(username=data["username"], role=data.get("role", "User"))
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()
    return {"message": "User created"}