from flask import Blueprint, jsonify, request
from db.models import db, ProgressLog
from utils.auth import get_current_user_id
from routes.user import profile
from routes.routines import daily_minutes, difficulty_level

progresses_bp = Blueprint("progresslogs", __name__)


@progresses_bp.route("/progress", methods=["POST"])
def create_progress():
    data = request.get_json()

    if not data or "task_id" not in data:
        return jsonify({"error": "task_id required"}), 400

    progress = ProgressLog(
        user_id=get_current_user_id(),
        task_id=data["task_id"],
        performance_score=data.get("performance_score", 0),
        feedback=data.get("feedback", ""))

    db.session.add(progress)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "id": progress.id,
        "task_id": progress.task_id}), 201


def adjust_consistency():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400
    if "daily_minutes" in data:

    if "consistency_score" in data:
        if "consistency_score"[0] < "preferred_difficulty_ratio":
            ""


@progresses_bp.route("/progress", methods=["GET"])
def list_progress():
    progresses = ProgressLog.query.filter_by(
        user_id=get_current_user_id()
    ).all()

    return jsonify([{
        "id": p.id,
        "task_id": p.task_id,
        "performance_score": p.performance_score,
        "feedback": p.feedback,
        "timestamp": p.timestamp
    } for p in progresses]), 200


@progresses_bp.route("/progress/task/<int:task_id>", methods=["GET"])
def get_progress_by_task(task_id):
    progresses = ProgressLog.query.filter_by(
        task_id=task_id,
        user_id=get_current_user_id()
    ).all()

    return jsonify([{
        "id": p.id,
        "performance_score": p.performance_score,
        "feedback": p.feedback,
        "timestamp": p.timestamp
    } for p in progresses]), 200


@progresses_bp.route("/progress/<int:progress_id>", methods=["GET"])
def get_progress_by_progress(progress_id):
    progresses = ProgressLog.query.filter_by(
        id=progress_id,
        user_id=get_current_user_id()
    ).all()

    return jsonify([{
        "id": p.id,
        "performance_score": p.performance_score,
        "feedback": p.feedback,
        "timestamp": p.timestamp
    } for p in progresses]), 200


@progresses_bp.route("/progress/<int:progress_id>", methods=["PATCH"])
def update_progress(progress_id):
    progress = ProgressLog.query.filter_by(
        id=progress_id,
        user_id=get_current_user_id()
    ).first_or_404()

    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400

    if "performance_score" in data:
        progress.performance_score = data["performance_score"]
    if "feedback" in data:
        progress.feedback = data["feedback"]

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"updated_id": progress_id}), 200


@progresses_bp.route("/progress/<int:progress_id>", methods=["DELETE"])
def delete_progress(progress_id):
    progress = ProgressLog.query.filter_by(
        id=progress_id,
        user_id=get_current_user_id()
    ).first_or_404()

    db.session.delete(progress)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"deleted_id": progress_id}), 200
