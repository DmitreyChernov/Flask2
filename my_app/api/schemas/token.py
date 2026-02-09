from marshmallow import Schema, fields

class TokenOut(Schema):
    access_token = fields.Str()
    token_type = fields.Str(dump_default="bearer")