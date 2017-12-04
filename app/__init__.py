# app/__init__.py

# import
import os

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# login_manager initialization
login_manager = LoginManager()

def create_app(config_name):

    # init app
    if os.getenv('FLASK_CONFIG') == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            # SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
            SQLALCHEMY_DATABASE_URI="mysql://CookShare:Tchien123@CookShare.mysql.pythonanywhere-services.com/CookShare$CookShare2"
            # mysql://CookShare:Tchien123@CookShare.mysql.pythonanywhere-services.com/CookShare$CookShare2
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')

    # bootstrap
    Bootstrap(app)

    # init db
    db.init_app(app)

    # init login_manager
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    # init migrate
    migrate = Migrate(app, db)

    from app import models

    # blueprint
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app