from marshmallow import EXCLUDE, INCLUDE, RAISE
from author import Author
from schema import AuthorSchema


json_data = """
{
    "id": 12,
    "name": "Ivan",
    "email": "ivan@mail.ru"
}
"""

schema = AuthorSchema()
json_data_as_dict = schema.loads(json_data)
print(json_data_as_dict)
