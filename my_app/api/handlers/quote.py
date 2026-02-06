# my_app/api/handlers/quote.py

from flask import jsonify, request
from api import app, db
from api.models.quote import QuoteModel
from api.models.author import AuthorModel
from api.schemas.quote import quote_schema, quotes_schema
from api.handlers.author import get_or_create_author
import random


@app.route("/quotes")
def get_quotes():
    quotes = db.session.scalars(db.select(QuoteModel)).all()
    return jsonify(quotes_schema.dump(quotes)), 200


@app.route("/quotes/<int:id>")
def get_quote(id):
    quote = db.session.get(QuoteModel, id)
    if not quote:
        return jsonify({"error": "Цитата не найдена"}), 404
    return jsonify(quote_schema.dump(quote)), 200


@app.route("/quotes/count")
def quotes_count():
    count = db.session.scalar(db.select(db.func.count(QuoteModel.id)))
    return jsonify({"count": count}), 200


@app.route("/quotes/random")
def random_quote():
    quotes = db.session.scalars(db.select(QuoteModel)).all()
    if not quotes:
        return jsonify({"error": "Нет цитат"}), 404
    return jsonify(quote_schema.dump(random.choice(quotes))), 200


@app.route("/quotes", methods=["POST"])
def create_quote():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Отсутствуют данные"}), 400

    # Валидация текста и автора вручную (пока автор — строка)
    author_name = json_data.get("author")
    text = json_data.get("text")

    if not author_name or not text:
        return jsonify({"error": "Требуются поля 'author' и 'text'"}), 400

    author_name = str(author_name).strip()
    text = str(text).strip()

    if not author_name or not text:
        return jsonify({"error": "Поля 'author' и 'text' не должны быть пустыми"}), 400

    # Валидация rating через схему (остальные поля)
    try:
        validated = quote_schema.load(
            {"text": text, "rating": json_data.get("rating", 1)},
            partial=("author", "id")  # пропускаем author и id
        )
    except Exception as err:
        return jsonify({"error": str(err)}), 400

    author = get_or_create_author(author_name)
    new_quote = QuoteModel(
        author=author,
        text=validated.text,
        rating=validated.rating
    )

    db.session.add(new_quote)
    try:
        db.session.commit()
        return jsonify(quote_schema.dump(new_quote)), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Ошибка при создании цитаты: {e}")
        return jsonify({"error": "Ошибка при сохранении в БД"}), 500


@app.route("/quotes/<int:id>", methods=["PUT"])
def edit_quote(id):
    quote = db.session.get(QuoteModel, id)
    if not quote:
        return jsonify({"error": "Цитата не найдена"}), 404

    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Отсутствуют данные"}), 400

    updates = {}
    updated = False

    if "author" in json_data:
        author_name = str(json_data["author"]).strip()
        if not author_name:
            return jsonify({"error": "Имя автора не может быть пустым"}), 400
        quote.author = get_or_create_author(author_name)
        updated = True

    if "text" in json_data:
        text = str(json_data["text"]).strip()
        if not text:
            return jsonify({"error": "Текст не может быть пустым"}), 400
        updates["text"] = text

    if "rating" in json_data:
        updates["rating"] = json_data["rating"]

    if updates:
        try:
            validated = quote_schema.load(updates, partial=True)
            for key, value in updates.items():
                setattr(quote, key, getattr(validated, key))
            updated = True
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    if not updated:
        return jsonify({"error": "Нет валидных полей для обновления"}), 400

    try:
        db.session.commit()
        return jsonify(quote_schema.dump(quote)), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Ошибка при обновлении цитаты {id}: {e}")
        return jsonify({"error": "Ошибка при обновлении в БД"}), 500


@app.route("/quotes/<int:id>", methods=["DELETE"])
def del_quote(id):
    quote = db.session.get(QuoteModel, id)
    if not quote:
        return jsonify({"error": "Цитата не найдена"}), 404

    db.session.delete(quote)
    try:
        db.session.commit()
        return jsonify({"message": "Цитата удалена"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Ошибка при удалении"}), 500


@app.route("/quotes/filters")
def filter_quotes():
    query = db.select(QuoteModel)
    filters_applied = {}

    if "id" in request.args:
        try:
            id_val = int(request.args["id"])
            query = query.where(QuoteModel.id == id_val)
            filters_applied["id"] = id_val
        except ValueError:
            return jsonify({"error": "Параметр 'id' должен быть целым числом"}), 400

    if "author" in request.args:
        author_name = request.args["author"].strip()
        if author_name:
            query = query.join(QuoteModel.author).where(AuthorModel.name == author_name)
            filters_applied["author"] = author_name
        else:
            return jsonify({"error": "Параметр 'author' не может быть пустым"}), 400

    if "text" in request.args:
        text = request.args["text"].strip()
        if text:
            query = query.where(QuoteModel.text == text)
            filters_applied["text"] = text

    if "rating" in request.args:
        try:
            rating = int(request.args["rating"])
            if 1 <= rating <= 5:
                query = query.where(QuoteModel.rating == rating)
                filters_applied["rating"] = rating
            else:
                return jsonify({"error": "Рейтинг должен быть от 1 до 5"}), 400
        except ValueError:
            return jsonify({"error": "Параметр 'rating' должен быть целым числом"}), 400

    results = db.session.scalars(query).all()
    if not results:
        return jsonify({
            "message": "Цитаты по заданным критериям не найдены",
            "filters_applied": filters_applied
        }), 200

    return jsonify(quotes_schema.dump(results)), 200


@app.route("/author/<int:id>/quotes")
def get_author_quotes(id):
    au = db.session.get(AuthorModel, id)
    if not au:
        return jsonify({"error": "Автор не найден"}), 404
    quotes = au.quotes.all()
    return jsonify(quotes_schema.dump(quotes)), 200