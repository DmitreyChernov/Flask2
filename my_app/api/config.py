from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.resolve()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfig(Config):
    DB_NAME = "quotes.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / DB_NAME}"
    SQLALCHEMY_ECHO = False