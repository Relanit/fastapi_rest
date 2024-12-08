import unittest
from datetime import date, timedelta
from pydantic import ValidationError

from borrowings.schemas import BorrowBase


class TestBorrowBase(unittest.TestCase):
    def test_valid_borrow_base(self):
        borrow = BorrowBase(
            user_id=1,
            book_id=2,
            borrow_date=date.today(),
            return_deadline=date.today() + timedelta(days=10),
        )
        self.assertEqual(borrow.user_id, 1)
        self.assertEqual(borrow.book_id, 2)
        self.assertEqual(borrow.borrow_date, date.today())
        self.assertEqual(borrow.return_deadline, date.today() + timedelta(days=10))

    def test_default_borrow_date_and_return_deadline(self):
        borrow = BorrowBase(user_id=1, book_id=2)
        self.assertEqual(borrow.borrow_date, date.today())
        self.assertEqual(borrow.return_deadline, date.today() + timedelta(days=30))

    def test_negative_book_id(self):
        with self.assertRaises(ValidationError) as context:
            BorrowBase(
                user_id=1,
                book_id=-2,
                borrow_date=date.today(),
                return_deadline=date.today() + timedelta(days=10),
            )
        self.assertIn("Book id must be a non-negative number", str(context.exception))

    def test_future_borrow_date(self):
        with self.assertRaises(ValidationError) as context:
            BorrowBase(
                user_id=1,
                book_id=2,
                borrow_date=date.today() + timedelta(days=1),
                return_deadline=date.today() + timedelta(days=10),
            )
        self.assertIn("Borrowing date must not be in the future", str(context.exception))

    def test_past_return_deadline(self):
        with self.assertRaises(ValidationError) as context:
            BorrowBase(
                user_id=1,
                book_id=2,
                borrow_date=date.today(),
                return_deadline=date.today(),
            )
        self.assertIn("Return deadline must be in the future", str(context.exception))

    def test_future_return_deadline(self):
        future_deadline = date.today() + timedelta(days=15)
        borrow = BorrowBase(user_id=1, book_id=2, return_deadline=future_deadline)
        self.assertEqual(borrow.return_deadline, future_deadline)

    def test_invalid_date_types(self):
        with self.assertRaises(ValidationError) as context:
            BorrowBase(
                user_id=1,
                book_id=2,
                borrow_date="invalid_date",
                return_deadline="invalid_date",
            )
        self.assertIn("Input should be a valid date or datetime", str(context.exception))


if __name__ == "__main__":
    unittest.main()
