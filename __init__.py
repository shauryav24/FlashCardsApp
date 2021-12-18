from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app =Flask(__name__)
    
    app.config['SECRET_KEY'] = "tismysecretkey"

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./aria.sqlite3'

    db.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint)

    return app