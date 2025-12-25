from flask import Blueprint, jsonify, request
from models_new import db, Goal
from auth import get_current_user_id


goals_bp = Blueprint("goals", __name__)


@goals_bp.route("/goals", methods=["POST"])
def create_goal():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400
    if "target" not in data:
        return jsonify({"error": "target is required"}), 400
    goal = Goal(
        user_id=get_current_user_id(),
        target=data["target"],
        target_count=data.get("target_count", 1),
        daily_time=data["daily_time"],
        status="active",
    )
    db.session.add(goal)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"id": goal.id, "target": goal.target}), 201


@goals_bp.route("/goals", methods=["GET"])
def list_goals():
    goals = Goal.query.filter_by(user_id=get_current_user_id()).all()
    return jsonify([
        {
            "id": g.id,
            "target": g.target,
            "target_count": g.target_count,
            "daily_time": g.daily_time,
            "status": g.status
        }
        for g in goals
    ])


@goals_bp.route("/goals/<int:goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.filter_by(
        id=goal_id, user_id=get_current_user_id()).first_or_404()
    return jsonify({
        "id": goal.id,
        "target": goal.target,
        "target_count": goal.target_count,
        "daily_time": goal.daily_time,
        "status": goal.status
    }), 200


@goals_bp.route("/goals/<int:goal_id>", methods=["PATCH"])
def update_goal(goal_id):
    goal = Goal.query.filter_by(
        id=goal_id,
        user_id=get_current_user_id()
    ).first_or_404()
    data = request.get_json()

    if not data:
        return jsonify({"error": "no data provided"}), 400
    if "status" in data and data["status"] not in {"active", "paused", "done"}:
        return jsonify({"error": "invalid status"}), 400
    goal.target = data["target"]
    goal.target_count = data["target_count"]
    goal.daily_time = data["daily_time"],
    goal.status = data["status"]
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"updated_id": goal_id}), 200


@goals_bp.route("/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.filter_by(
        id=goal_id,
        user_id=get_current_user_id()
    ).first_or_404()
    db.session.delete(goal)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"deleted_id": goal_id}), 200
