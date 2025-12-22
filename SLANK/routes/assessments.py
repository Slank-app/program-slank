from flask import Blueprint, jsonify, request
from db.models import db, Assessment
from utils.auth import get_current_user_id

assessments_bp = Blueprint("assessments", __name__)


@assessments_bp.route("/assessments", methods=["POST"])
def create_assessment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "no any data provided"}), 400
    if not data or "type" not in data:
        return jsonify({"error": "type is required"}), 400
    if "raw_data" not in data:
        return jsonify({"error": "raw data is required"}), 400
    assessment = Assessment(
        user_id=get_current_user_id(),
        type=data["type"],
        score=data.get("score", 0),
        raw_data=data["raw_data"],
    )
    db.session.add(assessment)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({
        "id": assessment.id,
        "type": assessment.type
    }), 201


@assessments_bp.route("/assessments", methods=["GET"])
def list_assessments():
    assessments = Assessment.query.filter_by(
        user_id=get_current_user_id()).all()
    return jsonify([{
        "id": a.id,
        "type": a.type,
        "score": a.score,
        "raw_data": a.raw_data,
    }
        for a in assessments
    ])


@assessments_bp.route("/assessments/<int:assessment_id>", methods=["GET"])
def get_assessment(assessment_id):
    assessment = Assessment.query.filter_by(
        id=assessment_id,
        user_id=get_current_user_id()
    ).first_or_404()
    return jsonify({
        "id": assessment.id,
        "type": assessment.type,
        "score": assessment.score,
        "raw_data": assessment.raw_data
    }), 200


@assessments_bp.route("/assessments/<int:assessment_id>", methods=["PATCH"])
def update_assessment(assessment_id):
    assessment = Assessment.query.filter_by(
        id=assessment_id,
        user_id=get_current_user_id()
    ).first_or_404()
    data = request.get_json()

    if not data:
        return jsonify({"error": "no data provided"}), 400

    if "type" in data:
        assessment.type = data["type"]
    if "raw_data" in data:
        assessment.raw_data = data["raw_data"]
    if "score" in data:
        assessment.score = data["score"]
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"updated_id": assessment_id}), 200


@assessments_bp.route("/assessments/<int:assessment_id>", methods=["DELETE"])
def delete_assessment(assessment_id):
    assessment = Assessment.query.filter_by(
        id=assessment_id,
        user_id=get_current_user_id()
    ).first_or_404()
    db.session.delete(assessment)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    return jsonify({"deleted_id": assessment.id}), 204
