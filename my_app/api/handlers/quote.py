from flask import abort, jsonify, request
from api import app, db
from api.models.quote import QuoteModel
from api.models.author import AuthorModel
from api.handlers.author import get_or_create_author
from api.schemas.quote import QuoteSchema, quote_input_schema, filter_schema, count_schema, quotes_schema, UpdateQuoteSchema
import random
import marshmallow as ma
from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError


# ! Отлажено
@app.get("/quotes")
@app.output(QuoteSchema(many=True))
@app.doc(summary="Получить все цитаты", tags=["Quotes and Authors"])
def get_quotes():
    quotes = db.session.scalars(db.select(QuoteModel)).all()
    return quotes


# ! Отлажено
@app.get("/quotes/<int:id>")
@app.output(QuoteSchema)
@app.doc(summary="Получить цитату по ID", tags=["Quotes and Authors"])
def get_quote(id: int):
    quote = db.session.get(QuoteModel, id)
    if not quote:
        abort(404, description="Цитата не найдена")
    return quote


# ! Отлажено
@app.get("/quotes/count")
@app.output(count_schema)
@app.doc(summary="Получить количество цитат", tags=["Quotes and Authors"])
def quotes_count():
    count = db.session.scalar(db.select(db.func.count(QuoteModel.id)))
    return {"count": count}


# ! Отлажено
@app.get("/quotes/random")
@app.output(QuoteSchema)
@app.doc(summary="Получить случайную цитату", tags=["Quotes and Authors"])
def random_quote():
    quotes = db.session.scalars(db.select(QuoteModel)).all()
    if not quotes:
        abort(404, description="Нет цитат")
    return random.choice(quotes)


# ! Отлажено
@app.post("/quotes")
@app.input(quote_input_schema, arg_name='data')
@app.output(QuoteSchema, status_code=201)
@app.doc(
    summary="Создать новую цитату",
    description="Создаёт новую цитату с указанным автором, текстом и рейтингом",
    tags=["Quotes and Authors"]
)
def create_quote(data):
    author_name = data["author"].strip()
    text = data["text"].strip()
    
    if not author_name:
        abort(400, description="Имя автора не может быть пустым")
    if not text:
        abort(400, description="Текст не может быть пустым")
    
    author = get_or_create_author(author_name)
 
    rating = data.get("rating", 1)
    
    new_quote = QuoteModel(
        author=author,
        text=text,
        rating=rating
    )
    
    db.session.add(new_quote)
    try:
        db.session.commit()
        return new_quote
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Ошибка при создании цитаты: {e}")
        abort(500, description="Ошибка при сохранении в БД")


# ! Отлажено
@app.delete("/quotes/<int:id>")
@app.output({}, status_code=204)
@app.doc(summary="Удалить цитату", tags=["Quotes and Authors"])
def del_quote(id: int):
    quote = db.session.get(QuoteModel, id)
    if not quote:
        abort(404, description="Цитата не найдена")
    
    db.session.delete(quote)
    try:
        db.session.commit()
        return {}
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Ошибка при удалении цитаты {id}: {e}")
        abort(500, description="Ошибка при удалении")


# ! Отлажено
@app.get("/quotes/filters")
@app.input(filter_schema, location='query')
@app.output(QuoteSchema(many=True))
@app.doc(
    summary="Фильтрация цитат",
    description="Фильтрация цитат по параметрам: id, author, text, rating",
    tags=["Quotes and Authors"]
)
def filter_quotes(query_data):
    query = db.select(QuoteModel)
    filters_applied = {}

    if "id" in query_data:
        id_val = query_data["id"]
        query = query.where(QuoteModel.id == id_val)
        filters_applied["id"] = id_val

    if "author" in query_data:
        author_name = query_data["author"].strip()
        if author_name:
            query = query.join(QuoteModel.author).where(AuthorModel.name == author_name)
            filters_applied["author"] = author_name
        else:
            abort(400, description="Параметр 'author' не может быть пустым")

    if "text" in query_data:
        text = query_data["text"].strip()
        if text:
            query = query.where(QuoteModel.text == text)
            filters_applied["text"] = text

    if "rating" in query_data:
        rating = query_data["rating"]
        if 1 <= rating <= 5:
            query = query.where(QuoteModel.rating == rating)
            filters_applied["rating"] = rating
        else:
            abort(400, description="Рейтинг должен быть от 1 до 5")

    results = db.session.scalars(query).all()
    return results