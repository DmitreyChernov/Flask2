from flask import jsonify, request
from api import app, db
from api.models.author import AuthorModel
from api.models.quote import QuoteModel
from api.handlers.author import get_or_create_author
import random
from typing import Any


def check_rating(rating_value: Any, is_new: bool) -> int | None:
    try:
        rating = int(rating_value)
        if 1 <= rating <= 5:
            return rating
    except:
        return None


@app.route("/quotes")
def get_quotes():
    quotes = QuoteModel.query.all()
    return jsonify([q.to_dict() for q in quotes])


@app.route("/quotes/<int:id>")
def get_quote(id):
    quote = QuoteModel.query.get_or_404(id)
    return jsonify(quote.to_dict())


@app.route("/quotes/count")
def quotes_count():
    count = QuoteModel.query.count()
    return jsonify({"count": count})


@app.route("/quotes/random")
def random_quote():
    quotes = QuoteModel.query.all()
    if not quotes:
        return jsonify({"error": "Нет цитат"}), 404
    return jsonify(random.choice(quotes).to_dict())


@app.route("/quotes", methods=["POST"])
def create_quote():
    data = request.get_json()
    if not data or "author" not in data or "text" not in data:
        return jsonify({"error": "Требуются поля 'author' и 'text'"}), 400

    author_name = str(data["author"]).strip()
    text = str(data["text"]).strip()
    if not author_name or not text:
        return jsonify({"error": "Поля 'author' и 'text' не должны быть пустыми"}), 400

    rating = check_rating(data.get("rating"), is_new=True) or 1

    author = get_or_create_author(author_name)
    new_quote = QuoteModel(author=author, text=text, rating=rating)
    db.session.add(new_quote)

    try:
        db.session.commit()
        return jsonify(new_quote.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Ошибка при создании цитаты: {e}")
        return jsonify({"error": "Ошибка при сохранении в БД"}), 500
    

@app.route("/quotes/<int:id>", methods=["PUT"])
def edit_quote(id):
    quote = QuoteModel.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return jsonify({"error": "Отсутствуют данные"}), 400

    updated = False

    if "author" in data:
        author_name = str(data["author"]).strip()
        if not author_name:
            return jsonify({"error": "Имя автора не может быть пустым"}), 400
        quote.author = get_or_create_author(author_name)
        updated = True

    if "text" in data:
        text = str(data["text"]).strip()
        if not text:
            return jsonify({"error": "Текст цитаты не может быть пустым"}), 400
        quote.text = text
        updated = True

    if "rating" in data:
        validated = check_rating(data["rating"], is_new=False)
        if validated is not None:
            quote.rating = validated
            updated = True
        else:
            return jsonify({"error": "Рейтинг должен быть целым числом от 1 до 5"}), 400

    if not updated:
        return jsonify({"error": "Нет валидных полей для обновления"}), 400

    try:
        db.session.commit()
        return jsonify(quote.to_dict())
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Ошибка при обновлении цитаты {id}: {e}")
        return jsonify({"error": "Ошибка при обновлении в БД"}), 500


@app.route("/quotes/<int:id>", methods=["DELETE"])
def del_quote(id):
    quote = QuoteModel.query.get_or_404(id)
    db.session.delete(quote)
    try:
        db.session.commit()
        return jsonify({"message": "Цитата удалена"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка при удалении"}), 500
    

@app.route("/quotes/filters")
def filter_quotes():
    query = QuoteModel.query
    filters_applied = {}

    if "id" in request.args:
        try:
            id_val = int(request.args["id"])
            query = query.filter(QuoteModel.id == id_val)
            filters_applied["id"] = id_val
        except ValueError:
            return jsonify({"error": "Параметр 'id' должен быть целым числом"}), 400

    if "author" in request.args:
        author_name = request.args["author"].strip()
        if author_name:
            query = query.join(QuoteModel.author).filter(AuthorModel.name == author_name)
            filters_applied["author"] = author_name
        else:
            return jsonify({"error": "Параметр 'author' не может быть пустым"}), 400

    if "text" in request.args:
        text = request.args["text"].strip()
        if text:
            query = query.filter(QuoteModel.text == text)
            filters_applied["text"] = text

    if "rating" in request.args:
        try:
            rating = int(request.args["rating"])
            if 1 <= rating <= 5:
                query = query.filter(QuoteModel.rating == rating)
                filters_applied["rating"] = rating
            else:
                return jsonify({"error": "Рейтинг должен быть от 1 до 5"}), 400
        except ValueError:
            return jsonify({"error": "Параметр 'rating' должен быть целым числом"}), 400

    results = query.all()
    if not results:
        return jsonify({
            "message": "Цитаты по заданным критериям не найдены",
            "filters_applied": filters_applied
        }), 200

    return jsonify([q.to_dict() for q in results]), 200