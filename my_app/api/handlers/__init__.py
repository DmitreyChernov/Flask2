from flask import jsonify, render_template
from api import app
from werkzeug.exceptions import HTTPException

@app.route("/")
def index():
    return render_template("index.html")


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"error": e.description}), e.code