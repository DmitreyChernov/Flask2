from flask import abort, jsonify, request
from marshmallow import ValidationError
from api import app, db
from api.models.user import UserModel
from api.schemas.user import user_schema, UserSchema


# url: /users/<int:user_id> - GET
@app.get("/users/<int:user_id>")
@app.output(UserSchema)
@app.doc(summary="Get user by id", description="Get user by id", tags=["users"])
def get_user_by_id(user_id: int):
    user = db.get_or_404(UserModel, user_id, description="Пользователь не найден")
    return user, 200


# url: /users - GET
@app.route("/users")
@app.output(UserSchema(many=True))
@app.doc(summary="Get all users", description="Get all users", tags=["users"])
def get_users():
    users = db.session.scalars(db.select(UserModel)).all()
    return users, 200


# url:  /users - POST
@app.route("/users", methods=["POST"])
@app.input(UserSchema, arg_name="user")
@app.output(UserSchema, status_code=201)
@app.doc(summary="Create new user and save to db", description="Create new user and save to db", tags=["users"])
def create_user(user):
    json_data = request.get_json()
    #if not json_data:
     #   return jsonify({"error": "No input data"}), 400
    try:
        user.save()
        #user = user_schema.load(json_data)
    except ValidationError as err:
        abort(400, f"Validation error: {err.messages_dict}")
    return user