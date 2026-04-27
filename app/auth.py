from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token)

    return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return {"message": "Logged out"}