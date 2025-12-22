from werkzeug.security import check_password_hash
from flask import Blueprint, request, jsonify
from db.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "missing credentials"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"error": "invalid credentials"}), 401

    if not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "invalid credentials"}), 401

    return jsonify({
        "message": "login successful",
        "user_id": user.id
    }), 200
