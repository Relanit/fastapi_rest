import unittest
from datetime import date, timedelta
from pydantic import ValidationError
from transactions.schemas import TransactionBase


class TestTransactionBase(unittest.TestCase):
    def test_valid_transaction_base(self):
        transaction = TransactionBase(
            user_id=1,
            asset_id=2,
            purchase_date=date.today(),
            target_sell_date=date.today() + timedelta(days=10),
            amount=100,
        )
        self.assertEqual(transaction.user_id, 1)
        self.assertEqual(transaction.asset_id, 2)
        self.assertEqual(transaction.purchase_date, date.today())
        self.assertEqual(transaction.target_sell_date, date.today() + timedelta(days=10))

    def test_default_purchase_date_and_target_sell_date(self):
        transaction = TransactionBase(user_id=1, asset_id=2, amount=100)
        self.assertEqual(transaction.purchase_date, date.today())
        self.assertEqual(transaction.target_sell_date, date.today() + timedelta(days=30))

    def test_negative_asset_id(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(
                user_id=1,
                asset_id=-2,
                purchase_date=date.today(),
                target_sell_date=date.today() + timedelta(days=10),
                amount=100
            )
        self.assertIn("ID актива должен быть неотрицательным", str(context.exception))

    def test_future_purchase_date(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(
                user_id=1,
                asset_id=2,
                purchase_date=date.today() + timedelta(days=1),
                target_sell_date=date.today() + timedelta(days=10),
                amount=100
            )
        self.assertIn("Дата покупки не может быть в будущем", str(context.exception))

    def test_past_target_sell_date(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(
                user_id=1,
                asset_id=2,
                purchase_date=date.today(),
                target_sell_date=date.today(),
                amount=100
            )
        self.assertIn("Целевая дата продажи должна быть в будущем", str(context.exception))

    def test_future_target_sell_date(self):
        future_deadline = date.today() + timedelta(days=15)
        transaction = TransactionBase(
            user_id=1,
            asset_id=2,
            target_sell_date=future_deadline,
            amount=100
        )
        self.assertEqual(transaction.target_sell_date, future_deadline)

    def test_invalid_date_types(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(
                user_id=1,
                asset_id=2,
                purchase_date="invalid_date",
                target_sell_date="invalid_date",
                amount=100
            )
        self.assertIn("invalid", str(context.exception).lower())


if __name__ == "__main__":
    unittest.main()
