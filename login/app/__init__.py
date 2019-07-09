from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


Login_manager = LoginManager()
Login_manager.login_view = 'main.login'

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    config_name.init_app(app)
    Login_manager.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app