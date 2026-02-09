from flask import jsonify
from api import app, db #,admin@required
from api.models.author import AuthorModel
from api.schemas.author import authors_schema


def get_or_create_author(name: str) -> AuthorModel:
    name = name.strip()
    author = db.session.execute(
        db.select(AuthorModel).where(AuthorModel.name == name)
    ).scalar_one_or_none()
    if author is None:
        author = AuthorModel(name=name)
        db.session.add(author)
        db.session.flush()
    return author


@app.get("/authors")
# @admin_required
def get_authors():
    authors = db.session.scalars(db.select(AuthorModel)).all()
    return jsonify(authors_schema.dump(authors)), 200