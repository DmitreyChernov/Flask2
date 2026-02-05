from api import ma 
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema


class QuoteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = QuoteModel
        # load_instance = True

    id = ma.auto_field()
    text = ma.auto_field()
    author = ma.Nested(AuthorSchema(only=("id")))


quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)