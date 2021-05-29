from flask import Flask
from models import db, User

# init SQLAlchemy so we can use it later in our models


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.static_folder = 'static'
    return app
