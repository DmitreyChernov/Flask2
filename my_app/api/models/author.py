from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api import db
# from api.models.quote import QuoteModel





class AuthorModel(db.Model):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)
    surname: Mapped[str] = mapped_column(String(32), nullable=True, index=True)
    quotes: Mapped[list["QuoteModel"]] = relationship(back_populates="author", lazy="dynamic", cascade="all, delete-orphan")

    def to_dict(self):
        return {"name": self.name, "surname": self.surname}