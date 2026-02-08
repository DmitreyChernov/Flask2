from flask import abort, jsonify, request
from marshmallow import ValidationError
from api import app, db
from api.models.user import UserModel
from api.schemas.user import user_schema, UserSchema


# url: /users/<int:user_id> - GET
@app.get("/users/<int:user_id>")
def get_user_by_id(user_id: int):
    user = db.get_or_404(UserModel, user_id, description="Пользователь не найден")
    return jsonify(user_schema.dump(user)), 200


# url: /users - GET
@app.route("/users")
def get_users():
    users = db.session.scalars(db.select(UserModel)).all()
    return jsonify(user_schema.dump(users, many=True)), 200


# url:  /users - POST
@app.route("/users", methods=["POST"])
def create_user():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data"}), 400
    try:
        user = user_schema.load(json_data)
    except Exception as err:
        return jsonify({"error": str(err)}), 400
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201