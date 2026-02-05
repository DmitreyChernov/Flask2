from flask import jsonify
from api import app, db
from api.models.author import AuthorModel
from api.schemas.author import author_schema, authors_schema



def get_or_create_author(name: str) -> AuthorModel:
    name = name.strip()
    author = db.session.execute(
        db.select(AuthorModel).where(AuthorModel.name == name)
    ).scalar_one_or_none()
    if author is None:
        author = AuthorModel(name=name)
        db.session.add(author)
    return author


@app.route("/author/<int:id>/quotes")
def get_author_quotes(id):
    au = AuthorModel.query.get_or_404(id)
    quotes = au.quotes.all()
    return jsonify([q.to_dict() for q in quotes])


@app.get("/authors")
def get_authors():
    authors = db.session.scalars(db.select(AuthorModel)).all()
    return jsonify(author_schema.dump(authors)), 200

