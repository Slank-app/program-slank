from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from models_new import db, User

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    required = ["email", "password", "age", "country"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": "missing data"}), 400

    user = User(
        email=data["email"],
        password=generate_password_hash(data["password"]),
        age=data["age"],
        country=data["country"]
    )
    db.session.add(user)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"error": "email already exists"}), 409

    return jsonify({
        "id": user.id,
        "email": user.email,
    }), 201


@users_bp.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id,
        "email": u.email
    }for u in users
    ])


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    return jsonify({
        "email": user.email
    }), 200
