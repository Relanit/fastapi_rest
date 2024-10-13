from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey

from src.auth.models import intpk, User
from src.database import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[intpk]
    name: Mapped[str]
    biography: Mapped[str | None] = mapped_column(nullable=True)
    date_of_birth: Mapped[datetime | None] = mapped_column(nullable=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[intpk]
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    published_year: Mapped[int | None]
    isbn: Mapped[str | None]
    description: Mapped[str | None]
    available: Mapped[bool] = mapped_column(default=True)

    author: Mapped["Author"] = relationship("Author", back_populates="books")


class Borrow(Base):

    __tablename__ = "borrowed_book"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    borrow_date: Mapped[str]
    return_date: Mapped[datetime | None]

    # user: Mapped["User"] = relationship("User", back_populates="borrowed_books")
    book: Mapped["Book"] = relationship("Book")
