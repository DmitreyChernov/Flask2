from api import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class AuthorModel(db.Model):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    surname: Mapped[str] = mapped_column(String(32), nullable=False, server_default="Иванов", index=True)
    quotes: Mapped[list["QuoteModel"]] = relationship("QuoteModel", back_populates="author", lazy="dynamic", cascade="all, delete-orphan")