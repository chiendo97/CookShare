# app/__init__.py

# import
import os

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, IMAGES

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

# login_manager initialization
login_manager = LoginManager()

# config image store
foods_img = UploadSet('foods', IMAGES)
steps_img = UploadSet('steps', IMAGES)
users_img = UploadSet('users', IMAGES)

ROOT_DIR = os.path.dirname(os.path.abspath('asdf'))

def create_app(config_name):

    # init app
    if os.getenv('FLASK_CONFIG') == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI="mysql://CookShare:Tchien123@CookShare.mysql.pythonanywhere-services.com/CookShare$CookShare2"
        )
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')

    # config photo
    app.config['UPLOADS_DEFAULT_DEST'] = os.path.dirname(os.path.abspath('asdf')) + '/static/img/'
    app.config['UPLOADED_foods_DEST'] = os.path.dirname(os.path.abspath('asdf')) + '/static/img/foods'
    app_config['UPLOADED_steps_DEST'] = os.path.dirname(os.path.abspath('asdf')) + '/static/img/steps'
    app_config['UPLOADED_users_DEST'] = os.path.dirname(os.path.abspath('asdf')) + '/static/img/users'
    configure_uploads(app, foods_img)
    configure_uploads(app, steps_img)
    configure_uploads(app, users_img)

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
    app.register_blueprint(admin_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app