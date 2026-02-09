from flask import current_app
from passlib.apps import custom_app_context as pwd_context
import sqlalchemy.orm as so
import sqlalchemy as sa
from api import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import jwt
from time import time


class UserModel(db.Model):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(32), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="user")

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
            from flask import abort
            abort(400, f"Database integrity error: {str(e.orig)}")
        except SQLAlchemyError as e:
            db.session.rollback()
            from flask import abort
            abort(503, f"Database error: {str(e)}")

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            from flask import abort
            abort(503, f"Database error: {str(e)}")

    def generate_auth_token(self):
        return jwt.encode(
            {"id": self.id, "exp": int(time() + 600)},
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(
                token,
                key=current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )
        except Exception:
            return None
        return db.session.get(UserModel, data['id'])