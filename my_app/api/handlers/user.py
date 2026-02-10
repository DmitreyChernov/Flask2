from flask import abort
from api import app, db
from api.models.user import UserModel
from api.schemas.user import UserSchema, user_input_schema, user_schema


# ! Отлажено
@app.get("/users/<int:user_id>")
@app.output(UserSchema)
@app.doc(summary="Получить пользователя по ID", tags=["Users"])
def get_user_by_id(user_id: int):
    user = db.session.get(UserModel, user_id)
    if not user:
        abort(404, description="Пользователь не найден")
    return user


# ! Отлажено
@app.get("/users")
@app.output(UserSchema(many=True))
@app.doc(summary="Получить всех пользователей", tags=["Users"])
def get_users():
    users = db.session.scalars(db.select(UserModel)).all()
    return users


# ! Отлажено
@app.post("/users")
@app.input(user_input_schema, arg_name='data')
@app.output(user_schema, status_code=201)
@app.doc(summary="Создать нового пользователя", tags=["Users"])
def create_user(data):
    existing_user = db.session.scalar(
        db.select(UserModel).where(UserModel.username == data["username"])
    )
    if existing_user:
        abort(400, description="Пользователь с таким именем уже существует")
    user = UserModel(username=data["username"])
    user.hash_password(data["password"])
    
    try:
        user.save()
        return user
    except Exception as e:
        abort(500, description=f"Ошибка при создании пользователя: {str(e)}")