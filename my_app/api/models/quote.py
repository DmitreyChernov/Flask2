from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api import db


class QuoteModel(db.Model):
    __tablename__ = 'quotes'
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["AuthorModel"] = relationship(back_populates="quotes")
    text: Mapped[str] = mapped_column(String(255))
    rating: Mapped[int] = mapped_column(nullable=False, default=1)

    def __repr__(self):
        return f"<Quote {self.id}: {self.text[:30]}...>"