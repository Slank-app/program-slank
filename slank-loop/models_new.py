from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    goals = db.relationship("Goal", backref="user", lazy=True)
    session = db.relationship("Session", backref="user", lazy=True)


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target = db.Column(db.String(100), nullable=False)
    target_count = db.Column(db.Integer, nullable=False)
    daily_time = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String, nullable=False)
    progress = db.relationship("Session", backref="goal", lazy=True)


class Session(db.Model):
    __tablename__ = "sessions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"), nullable=False)
    items_correct = db.Column(db.Integer, nullable=False)
    items_seen = db.Column(db.Integer, nullable=False)
    total_time = db.Column(db.Float, nullable=False, default=0.0)
    expected_time = db.Column(db.Float, nullable=False, default=0.0)
    last_session_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    current_batch_size = db.Column(db.Integer, nullable=False, default=7)
