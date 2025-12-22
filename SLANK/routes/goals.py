from flask import Blueprint, jsonify, request
from db.models import db, Goal
from utils.auth import get_current_user_id


goals_bp = Blueprint("goals", __name__)


@goals_bp.route("/goals", methods=["POST"])
def create_goal():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400
    if "title" not in data:
        return jsonify({"error": "title is required"}), 400
    goal = Goal(
        user_id=get_current_user_id(),
        title=data["title"],
        description=data.get("description", ""),
        status="active"
    )
    db.session.add(goal)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"id": goal.id, "title": goal.title}), 201
# POST is done


@goals_bp.route("/goals", methods=["GET"])
def list_goals():
    goals = Goal.query.filter_by(user_id=get_current_user_id()).all()
    return jsonify([
        {
            "id": g.id,
            "title": g.title,
            "description": g.description,
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
        "title": goal.title,
        "description": goal.description,
        "status": goal.status
    }), 200
# GET_GOAL is done


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
    if "title" in data:
        goal.title = data["title"]
    if "description" in data:
        goal.description = data["description"]
    if "status" in data:
        goal.status = data["status"]
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"updated_id": goal_id}), 200
# UPDATER is done


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
# DELETE is done
