from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from api.config import DevConfig

app = Flask(__name__)
app.json.ensure_ascii = False
app.config.from_object(DevConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from api.models import author, quote
db.configure_mappers()
from api.handlers import author, quote