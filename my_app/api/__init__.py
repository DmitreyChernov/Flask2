# api/__init__.py
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from api.config import DevConfig


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config.from_object(DevConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    return app


app = create_app()
auth = HTTPBasicAuth(app)

from api.models import author, quote, user
db.configure_mappers()

from api.handlers import author, quote, user
from api.models.user import UserModel


@auth.verify_password
def verify_password(username, password):
    if not username or not password:
        return False
    user = db.session.execute(
        db.select(UserModel).filter_by(username=username)
    ).scalar_one_or_none()
    if user and user.verify_password(password):
        g.user = user
        return True
    return False