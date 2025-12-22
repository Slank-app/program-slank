from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    goals = db.relationship("Goal", backref="user", lazy=True)
    progress = db.relationship("ProgressLog", backref="user", lazy=True)
    skill_profile = db.relationship(
        "SkillProfile", backref="user", uselist=False)
    assessments = db.relationship("Assessment", backref="user", lazy=True)


class Goal(db.Model):
    __tablename__ = "goals"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    target_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(100), default="active", nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    routines = db.relationship("Routine", backref="goal", lazy=True)


class Assessment(db.Model):
    __tablename__ = "assessments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    type = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    raw_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )


class SkillProfile(db.Model):
    __tablename__ = "skillprofiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )
    cognitive_score = db.Column(db.Integer, default=0)
    consistency_score = db.Column(db.String(50), default=0, nullable=False)
    learning_speed = db.Column(db.Integer, default=0)
    weakness_tags = db.Column(db.Text, nullable=False)


class Routine(db.Model):
    __tablename__ = "routines"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    goal_id = db.Column(
        db.Integer,
        db.ForeignKey("goals.id"),
        nullable=False
    )
    daily_minutes = db.Column(db.Integer, nullable=False)
    difficulty_level = db.Column(db.String(100), nullable=False)
    structure = db.Column(db.String(200), nullable=False)
    tasks = db.relationship("Task", backref="routine", lazy=True)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    routine_id = db.Column(
        db.Integer,
        db.ForeignKey("routines.id"),
        nullable=False
    )
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String, nullable=False)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    progresses = db.relationship(
        "ProgressLog",
        backref="task",
        lazy=True
    )


class ProgressLog(db.Model):
    __tablename__ = "progress_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id"),
        nullable=False
    )
    performance_score = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )
    feedback = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
