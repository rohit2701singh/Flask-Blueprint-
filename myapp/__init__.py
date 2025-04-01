# Creates the Flask app instance, Loads configurations
# Initializes extensions like SQLAlchemy & Flask-Login
# Registers Blueprints (for modular routing)
# Always be mindful of where and how you're importing modules, otherwise you will caught in circular import and app will crash

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from myapp.config import Config


db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)    # initialise extension here
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from myapp.users.routes import users    # importing bluprint instance 'users'
    from myapp.posts.routes import posts
    from myapp.main.routes import main

    app.register_blueprint(users)   # registering routes of bluprint instances
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app