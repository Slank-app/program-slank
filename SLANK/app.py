from flask import Flask
from db.models import db
from routes.goals import goals_bp
from routes.assessments import assessments_bp
from routes.tasks import tasks_bp
from routes.routines import routines_bp
from routes.progresslogs import progresses_bp
from routes.user import users_bp
from routes.login import auth_bp


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    db.init_app(app)
    app.register_blueprint(goals_bp)
    app.register_blueprint(assessments_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(routines_bp)
    app.register_blueprint(progresses_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    with app.app_context():
        db.create_all()

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
