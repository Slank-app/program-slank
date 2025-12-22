from flask import Blueprint, request, jsonify
from db.models import db, Task

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    required = ["routine_id", "title", "type"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": "missing data"}), 400

    task = Task(
        user_id=data["user_id"],
        routine_id=data["routine_id"],
        title=data["title"],
        type=data["type"],
        duration=data.get("duration", 0),
        completed=False
    )
    db.session.add(task)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"id": task.id}), 201


@tasks_bp.route("/tasks/routines/<int:routine_id>", methods=["GET"])
def get_tasks(routine_id):
    tasks = Task.query.filter_by(routine_id=routine_id).all()
    return jsonify([{
        "id": task.id,
        "title": task.title,
        "type": task.type,
        "duration": task.duration,
        "completed": task.completed
    }for task in tasks]), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "no data provided"}), 400

    required = ["title", "type", "duration", "completed"]
    for f in required:
        if f in data:
            setattr(task, f, data[f])
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"updated_id": task_id}), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"deleted_id": task_id}), 200
