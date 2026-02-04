from flask import jsonify
from api import app
from werkzeug.exceptions import HTTPException


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"error": e.description}), e.code