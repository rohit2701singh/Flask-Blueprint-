# THIS PAGE IS APPLICATION FACTORY

# Creates the Flask app instance, Loads configurations
# Initializes extensions like SQLAlchemy & Flask-Login
# Registers Blueprints (for modular routing)
# Always be mindful of where and how you're importing modules, otherwise you will caught in circular import and app will crash

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from myapp.config import Config
from flask_ckeditor import CKEditor
from flask_admin import Admin

db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

ckeditor = CKEditor()

admin = Admin(name='App Admin Page') # /admin in URL
    

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)    # initialise extension here
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    from myapp.models import User, Post # import here to avoid circular import
    from myapp.admin_views.views import UserView, PostView, MyAdminIndexView

    admin.init_app(app, index_view=MyAdminIndexView())
    admin.add_view(UserView(User, db.session))
    admin.add_view(PostView(Post, db.session))

    from myapp.users.routes import users    # importing bluprint instance 'users'
    from myapp.posts.routes import posts
    from myapp.main.routes import main

    app.register_blueprint(users)   # registering bluprints 
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app