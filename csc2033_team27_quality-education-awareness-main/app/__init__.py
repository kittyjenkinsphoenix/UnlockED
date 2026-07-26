import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from config import DevelopmentConfig, ProductionConfig

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()

# login manager settings
login_manager.login_view = "main.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database for Flask-Login."""
    from .models import User

    return db.session.get(User, int(user_id))


# limiting function
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])


def create_app(test_config=None):
    """Create and configure the Flask application instance."""
    app = Flask(__name__)

    flask_env = os.environ.get("FLASK_ENV", "development")

    if flask_env == "production":
        config_class = ProductionConfig
    else:
        config_class = DevelopmentConfig

    app.config.from_object(config_class)

    config_class.init_app(app)

    if test_config:
        app.config.update(test_config)

    # initilsise extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    # secure logging setup
    if not app.debug:  # prod. environment
        if not os.path.exists("logs"):
            os.mkdir("logs")  # create directory

        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=1 * 1024 * 1024, backupCount=5
        )  # 1 mb, 5 backup logs

        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]")
        )  # formatting
        file_handler.setLevel(logging.INFO)  # ignores debug
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("App started")

    from .routes import main

    app.register_blueprint(main)

    def seed_database():
        """Insert the default demo users when the database is empty."""
        from .models import User

        users = [
            {
                "username": "user1@email.com",
                "name": "User",
                "password": "Userpass!23",
                "role": "user",
                "bio": "I'm a basic user",
            },
            {
                "username": "admin1@email.com",
                "name": "Admin",
                "password": "Adminpass!23",
                "role": "admin",
                "bio": "I'm an administrator",
            },
        ]

        for data in users:
            user = User(username=data["username"], name=data["name"], role=data["role"])
            user.set_password(data["password"])
            user.set_bio(data["bio"])
            db.session.add(user)

        db.session.commit()

    with app.app_context():
        from .models import User

        db.create_all()

        if not User.query.first():  # only seed db if no users exist
            seed_database()  # populate table with startup data

    return app
