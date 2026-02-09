from flask import abort, current_app
from passlib.apps import custom_app_context as pwd_context
import sqlalchemy.orm as so
from api import db
from config import Config
import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
#from itsdangerous import URLSafeSerializer, BadSignature
from time import time
import jwt



class UserModel(db.Model):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128))

    def __init__(self, username, password):
        self.username = username
        self.hash_password(password)

    def hash_password(self, password):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            abort(400, f"Database integrity error: {str(e.orig)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(503, f"Database error: {str(e)}")
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(503, f"Database error: {str(e)}")
    

    def generate_auth_token(self):
        token = jwt.encode(
            {"id": self.id, "exp": int(time() + 60)},
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return token

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, key=Config.SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            print(e)
            return None  # invalid token
        user = db.get_or_404(UserModel, data['id'], description=f"User with id={data['id']} not found")
        return user