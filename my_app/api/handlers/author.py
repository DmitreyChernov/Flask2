from functools import wraps
from flask import abort, g
from api import app, db, token_auth
from api.models.author import AuthorModel
from api.schemas.author import AuthorSchema
import logging


def get_or_create_author(name: str) -> AuthorModel:
    name = name.strip()
    author = db.session.scalar(
        db.select(AuthorModel).where(AuthorModel.name == name)
    )
    if author is None:
        author = AuthorModel(name=name)
        db.session.add(author)
        db.session.flush()
    return author


# ! Отлажено
@app.get("/authors")
@app.output(AuthorSchema(many=True))
@app.doc(summary="Получить всех авторов", tags=["Quotes and Authors"])
def get_authors():
    authors = db.session.scalars(db.select(AuthorModel)).all()
    return authors


# ! Отлажено
@app.get("/authors/<int:id>")
@app.output(AuthorSchema)
@app.doc(summary="Получить автора по ID", tags=["Quotes and Authors"])
def get_author(id: int):
    author = db.session.get(AuthorModel, id)
    if not author:
        abort(404, description="Автор не найден")
    return author


@app.post("/authors")
@app.input(AuthorSchema, arg_name="author")
@app.output(AuthorSchema, status_code=201)
@app.doc(
    summary="Create new author",
    description="Create new author (admin only)",
    responses={403: "Forbidden", 503: "Database error"},
    tags=["Authors"]
)
@app.auth_required(token_auth)
def create_author(author):
    try:
        db.session.add(author)
        db.session.commit()
        logging.info(f"✓ Author created successfully")
    except Exception as e:
        logging.error(f"✗ Database error: {e}")
        abort(503, description=f"Database error: {str(e)}")
    return author