from datetime import date, datetime
from typing import Any

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, intpk


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str]
    permissions: Mapped[dict[str, Any]]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024))
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)

    role: Mapped[Role] = relationship("Role", lazy="selectin")


class Author(Base):
    __tablename__ = "author"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    biography: Mapped[str | None] = mapped_column(nullable=True)
    date_of_birth: Mapped[date | None] = mapped_column(nullable=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[intpk]
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    published_year: Mapped[int | None]
    isbn: Mapped[str | None]
    description: Mapped[str | None]
    available_count: Mapped[int] = mapped_column(default=0)

    author: Mapped["Author"] = relationship("Author", back_populates="books")


class Borrow(Base):

    __tablename__ = "borrowed_book"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    borrow_date: Mapped[date]
    return_date: Mapped[date | None]

    # user: Mapped["User"] = relationship("User", back_populates="borrowed_books")
    book: Mapped["Book"] = relationship("Book")
