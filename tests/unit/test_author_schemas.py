import unittest
from datetime import date, timedelta
from pydantic import ValidationError

from authors.schemas import AuthorBase, AuthorCreate, AuthorPatchUpdate


class TestAuthorSchemas(unittest.TestCase):

    def test_author_base_valid(self):
        data = {
            "name": "  john doe  ",
            "biography": "A famous author.",
            "date_of_birth": "1980-01-01"
        }
        author = AuthorBase(**data)
        self.assertEqual(author.name, "John Doe")  # Проверяем форматирование имени
        self.assertEqual(author.biography, "A famous author.")
        self.assertEqual(author.date_of_birth, date(1980, 1, 1))

    def test_author_base_invalid_name(self):
        data = {"name": "A", "date_of_birth": "1980-01-01"}
        with self.assertRaises(ValidationError) as context:
            AuthorBase(**data)
        self.assertIn("Author name must be between 2 and 100 characters long.", str(context.exception))

    def test_author_base_invalid_date_of_birth_format(self):
        data = {"name": "John Doe", "date_of_birth": "01-01-1980"}
        with self.assertRaises(ValidationError) as context:
            AuthorBase(**data)
        self.assertIn("Invalid date format. Use 'YYYY-MM-DD'.", str(context.exception))

    def test_author_base_invalid_date_of_birth_future(self):
        future_date = (date.today() + timedelta(days=1)).isoformat()
        data = {"name": "John Doe", "date_of_birth": future_date}
        with self.assertRaises(ValidationError) as context:
            AuthorBase(**data)
        self.assertIn("Date of birth cannot be in the future.", str(context.exception))

    def test_author_create_valid(self):
        data = {"name": "John Doe", "date_of_birth": "1980-01-01"}
        author = AuthorCreate(**data)
        self.assertEqual(author.name, "John Doe")
        self.assertEqual(author.date_of_birth, date(1980, 1, 1))

    def test_author_patch_update_partial(self):
        data = {"name": None, "date_of_birth": "2000-03-10"}

        with self.assertRaises(ValidationError):
            AuthorPatchUpdate(**data)


if __name__ == "__main__":
    unittest.main()
