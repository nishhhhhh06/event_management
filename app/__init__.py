from flask import Flask, session
from app.extensions import db, login_manager, migrate, bcrypt, mail
from flask_login import logout_user
from app.routes.auth_routes import auth_bp
from app.routes.event_routes import events_bp
from app.routes.user_routes import user_bp
from app.routes.main_routes import main_bp
from app.models import User
from datetime import timedelta


def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.before_request
    def check_session_timeout():
        # Logout user if session expires
        session.modified = True
        if not session.get("_user_id"):
            logout_user()

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(events_bp, url_prefix="/events")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(main_bp)

    # Flask-Mail Configuration (Replace with your email details)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your email'  # Change this
    app.config['MAIL_PASSWORD'] = 'app password'  # create app password for your account and enter here
    app.config['MAIL_DEFAULT_SENDER'] = 'your email'  # Change this

    mail.init_app(app)

    return app
