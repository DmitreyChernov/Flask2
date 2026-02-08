from flask import request
from api import ma
from api.models.user import UserModel
from marshmallow import validate, fields, post_load


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        exclude = ("password_hash",)
        dump_only = ("id",)
        
    username = ma.auto_field(required=True, validate=validate.Length(min=4))
    password = fields.String(required=True, validate=validate.Length(min=5, max=15))

    @post_load
    def make_user(self, data, **kwargs):
        if request.method == "POST":
            return UserModel(**data)
        return data


user_schema = UserSchema()