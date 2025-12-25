from flask import Blueprint, request, jsonify
from models_new import db, Session
from auth import get_current_user_id, get_current_goal_id
from engine.session import end_learning_session

session_bp = Blueprint("session_end", __name__)


@session_bp.route("/session-end", methods=["POST"])
def create_progress():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data"}), 400
    if "items_correct" not in data or "items_seen" not in data:
        return jsonify({"error": "missing credentials"}), 400
    progress = Session(
        user_id=get_current_user_id(),
        goal_id=get_current_goal_id(),
        items_correct=data["items_correct"],
        items_seen=data["items_seen"],
        total_time=data["total_time"],
        expected_time=data["expected_time"],
        current_batch_size=data["current_batch_size"]
    )
    db.session.add(progress)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "id": progress.id,
        "current_batch_size": progress.current_batch_size
    }), 201


@session_bp.route("/session-end/<int:progress_id>", methods=["PATCH"])
def end_session(progress_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "missing data"}), 400
    if data["items_seen"] <= 0:
        return jsonify({"error": "items_seen must be greater than 0"}), 400

    required = ["items_correct", "items_seen", "total_time"]
    for f in required:
        if f not in data:
            return jsonify({"error": "no data provided"}), 400
    progress = Session.query.filter_by(
        id=progress_id,
        user_id=get_current_user_id(),
        goal_id=get_current_goal_id()
    ).first_or_404()
    next_batch_size = end_learning_session(
        items_correct=data["items_correct"],
        items_seen=data["items_seen"],
        total_time=data["total_time"],
        current_batch_size=progress.current_batch_size,
        expected_time=progress.expected_time
    )
    progress.items_correct = data["items_correct"]
    progress.items_seen = data["items_seen"]
    progress.total_time = data["total_time"]
    progress.current_batch_size = next_batch_size
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "next_batch_size": next_batch_size,
        "accuracy": data["items_correct"] / data["items_seen"]
    }), 200
