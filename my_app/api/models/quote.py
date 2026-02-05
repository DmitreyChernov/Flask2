
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api import db
from api.models.author import AuthorModel


class QuoteModel(db.Model):
    __tablename__ = 'quotes'
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["AuthorModel"] = relationship(back_populates="quotes")
    text: Mapped[str] = mapped_column(String(255))
    rating: Mapped[int] = mapped_column(nullable=False, default=1)

    def __init__(self, author: AuthorModel, text: str, rating: int = 1):
        self.author = author
        self.text = text
        self.rating = rating

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author.name,
            "text": self.text,
            "rating": self.rating
        }