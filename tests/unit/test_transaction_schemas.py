import unittest
from datetime import date, timedelta
from decimal import Decimal

from pydantic import ValidationError
from transactions.schemas import TransactionBase


class TestTransactionBase(unittest.TestCase):
    def test_valid_transaction_base(self):
        transaction = TransactionBase(
            user_id=1,
            asset_id=2,
            purchase_date=date.today(),
            target_sell_date=date.today() + timedelta(days=10),
            amount=Decimal("100.00"),
        )
        self.assertEqual(transaction.user_id, 1)
        self.assertEqual(transaction.asset_id, 2)
        self.assertEqual(transaction.purchase_date, date.today())
        self.assertEqual(transaction.target_sell_date, date.today() + timedelta(days=10))

    def test_default_purchase_date_and_target_sell_date(self):
        transaction = TransactionBase(user_id=1, asset_id=2, amount=Decimal("100.00"))
        self.assertEqual(transaction.purchase_date, date.today())
        self.assertEqual(transaction.target_sell_date, date.today() + timedelta(days=30))

    def test_negative_asset_id(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(
                user_id=1,
                asset_id=-2,
                purchase_date=date.today(),
                target_sell_date=date.today() + timedelta(days=10),
                amount=Decimal("100.00"),
            )
        self.assertIn("type=greater_than_equal", str(context.exception))

    def test_future_purchase_date(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(
                user_id=1,
                asset_id=2,
                purchase_date=date.today() + timedelta(days=1),
                target_sell_date=date.today() + timedelta(days=10),
                amount=Decimal("100.00"),
            )
        self.assertIn("type=less_than_equal", str(context.exception))

    def test_past_target_sell_date(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(
                user_id=1,
                asset_id=2,
                purchase_date=date.today(),
                target_sell_date=date.today(),
                amount=Decimal("100.00"),
            )
        self.assertIn("type=greater_than", str(context.exception))

    def test_future_target_sell_date(self):
        future_deadline = date.today() + timedelta(days=15)
        transaction = TransactionBase(
            user_id=1,
            asset_id=2,
            target_sell_date=future_deadline,
            amount=Decimal("100.00"),
        )
        self.assertEqual(transaction.target_sell_date, future_deadline)

    def test_invalid_date_types(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(
                user_id=1,
                asset_id=2,
                purchase_date="invalid_date",
                target_sell_date="invalid_date",
                amount=Decimal("100.00"),
            )
        self.assertIn("invalid", str(context.exception).lower())


if __name__ == "__main__":
    unittest.main()
