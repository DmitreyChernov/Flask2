from api import ma
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema
from marshmallow import ValidationError, validates
from marshmallow.validate import Range


class QuoteInputSchema(ma.Schema):
    author = ma.String(required=True)
    text = ma.String(required=True)
    rating = ma.Integer(
        validate=Range(min=1, max=5)
    )

class QuoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuoteModel
        load_instance = True
        include_fk = False
    author = ma.Nested(lambda: AuthorSchema(only=("name", "surname")))
    rating = ma.Integer(validate=Range(min=1, max=5))

class UpdateQuoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuoteModel
        load_instance = False
        include_fk = False
    
    author = ma.Nested(lambda: AuthorSchema(only=("name", "surname")))
    text = ma.Str()
    rating = ma.Integer(validate=Range(min=1, max=5))


class CountSchema(ma.Schema):
    count = ma.Integer(required=True)


class FilterSchema(ma.Schema):
    id = ma.Integer()
    author = ma.String()
    text = ma.String()
    rating = ma.Integer(validate=Range(min=1, max=5))


quote_input_schema = QuoteInputSchema()
filter_schema = FilterSchema()
count_schema = CountSchema()
quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)