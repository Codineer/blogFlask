from flask import Flask
from .models import db
from os import path
from flask_login import LoginManager


DB_NAME = "flask_blog_db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://root:utkarsh@localhost:3306/{DB_NAME}"  
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User,Post,Comment,Like

    create_db(app)

    login_manager= LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    with app.app_context():
        db.create_all()
        print("Created database!")
