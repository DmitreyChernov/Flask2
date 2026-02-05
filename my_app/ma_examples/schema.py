from marshmallow import Schema, fields

class AuthorSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True, error_messages={"required": "field_name is required"})
    email = fields.Email(required=True, error_messages={"required": "field_name is required"})
    surname = fields.String()