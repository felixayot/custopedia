from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail



db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "users.sign_in"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)


    from app.main.routes import main
    from app.users.routes import users
    from app.tickets.routes import tickets
    from app.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(tickets)
    app.register_blueprint(errors)

    return app
