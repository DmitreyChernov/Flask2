from flask import render_template
from werkzeug.exceptions import HTTPException
from api import app

@app.get("/")
@app.doc(hide=True)
def index():
    return render_template("index.html")

@app.errorhandler(HTTPException)
def handle_exception(e):
    return {"error": e.description}, e.code

@app.errorhandler(404)
def not_found(e):
    return {"error": "Ресурс не найден"}, 404

@app.errorhandler(500)
def internal_error(e):
    return {"error": "Внутренняя ошибка сервера"}, 500