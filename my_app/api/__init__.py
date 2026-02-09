from functools import wraps
from flask import Flask, abort, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
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
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth("Bearer")
multi_auth = MultiAuth(basic_auth, token_auth)

from api.models import author, quote, user
db.configure_mappers()

from api.handlers import author, quote, user, token
from api.models.user import UserModel


@basic_auth.verify_password
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


@token_auth.verify_token
def verify_token(token):
    from api.models.user import UserModel
    user = UserModel.verify_auth_token(token)
    return user

"""
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not getattr(g, 'user', None) or g.user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated
"""