from api import ma
from api.models.author import AuthorModel

class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthorModel
        load_instance = True
        include_fk = False

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)