from flask import Blueprint, request, jsonify
from db.models import db, Routine
from utils.auth import get_current_user_id
routines_bp = Blueprint("routines", __name__)


@routines_bp.route("/routines", methods=["POST"])
def create_routine():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400
    routine = Routine(
        user_id=get_current_user_id(),
        goal_id=data["goal_id"],
        daily_minutes=data["daily_minutes"],
        difficulty_level=data["difficulty_level"],
        structure=data["structure"]
    )
    db.session.add(routine)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "id": routine.id,
        "difficulty_level": routine.difficulty_level
    }), 201


@routines_bp.route("/routines", methods=["GET"])
def list_routines():
    routines = Routine.query.filter_by(user_id=get_current_user_id()).all()
    return jsonify([{
        "id": r.id,
        "daily_minutes": r.daily_minutes,
        "difficulty_level": r.difficulty_level,
        "structure": r.structure
    }for r in routines])


@routines_bp.route("/routines/<int:routine_id>", methods=["GET"])
def get_routine(routine_id):
    routine = Routine.query.filter_by(
        id=routine_id,
        user_id=get_current_user_id()
    ).first_or_404()
    return jsonify({
        "id": routine.id,
        "daily_minutes": routine.daily_minutes,
        "difficulty_level": routine.difficulty_level,
        "structure": routine.structure
    }), 200


@routines_bp.route("/routines/<int:routine_id>", methods=["PATCH"])
def update_routine(routine_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400
    routine = Routine.query.filter_by(
        id=routine_id,
        goal_id=data["goal_id"],
        user_id=get_current_user_id()
    ).first_or_404()

    if "daily_minutes" in data:
        routine.daily_minutes = data["daily_minutes"]
    if "difficulty_level" in data:
        routine.difficulty_level = data["difficulty_level"]
    if "structure" in data:
        routine.structure = data["structure"]
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"updated_id": routine_id}), 200


@routines_bp.route("/routines/<int:routine_id>", methods=["DELETE"])
def delete_routine(routine_id):
    routine = Routine.query.filter_by(
        id=routine_id,
        user_id=get_current_user_id()
    ).first_or_404()
    db.session.delete(routine)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"deleted_id": routine_id}), 200
