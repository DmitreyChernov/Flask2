from flask import abort, jsonify, request
from marshmallow import ValidationError
from api import app, db
from api.models.user import UserModel
from api.schemas.user import user_schema, UserSchema


# url: /users/<int:user_id> - GET
@app.get("/users/<int:user_id>")
def get_user_by_id(user_id: int):
    user = db.get_or_404(UserModel, user_id, description=_("User with id=%(user_id)s not found", user_id=user_id))
    return user, 200


# url: /users - GET
@app.get("/users")
def get_users():
    users = db.session.scalars(db.select(UserModel)).all()
    return users, 200


# url:  /users - POST
@app.post("/users")
def create_user(user):
    user.save()  
    return user