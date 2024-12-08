import unittest
from datetime import date
from pydantic import ValidationError

from books.schemas import BookBase


class TestBookBase(unittest.TestCase):

    def test_invalid_title_length(self):
        with self.assertRaises(ValidationError) as context:
            BookBase(
                author_id=1,
                title="",
                published_year=2020,
                isbn="1234567890123",
                description="A valid description.",
                available_count=10
            )
        self.assertIn("Book title must be at least 1 character long.", str(context.exception))

    def test_future_published_year(self):
        current_year = date.today().year
        with self.assertRaises(ValidationError) as context:
            BookBase(
                author_id=1,
                title="Valid Book Title",
                published_year=current_year + 1,
                isbn="1234567890123",
                description="A valid description.",
                available_count=10
            )
        self.assertIn("Published year cannot be in the future.", str(context.exception))

    def test_invalid_available_count(self):
        with self.assertRaises(ValidationError) as context:
            BookBase(
                author_id=1,
                title="Valid Book Title",
                published_year=2020,
                isbn="1234567890123",
                description="A valid description.",
                available_count=-1
            )
        self.assertIn("Available count must be a non-negative number.", str(context.exception))

    def test_valid_available_count(self):
        book = BookBase(
            author_id=1,
            title="Valid Book Title",
            published_year=2020,
            isbn="1234567890123",
            description="A valid description.",
            available_count=10
        )
        self.assertEqual(book.available_count, 10)


if __name__ == '__main__':
    unittest.main()
