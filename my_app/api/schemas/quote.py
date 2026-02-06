from api import ma
from api.models.quote import QuoteModel
from api.schemas.author import AuthorSchema

class QuoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = QuoteModel
        load_instance = True
        include_fk = False

    author = ma.Nested(lambda: AuthorSchema(only=("name", "surname")))
    rating = ma.auto_field(validate=lambda x: (isinstance(x, int) and 1 <= x <= 5) or 
                           exec('raise ValidationError("Рейтинг от 1 до 5")'))

quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)