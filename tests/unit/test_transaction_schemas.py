import unittest
from decimal import Decimal

from pydantic import ValidationError
from transactions.schemas import TransactionBase


class TestTransactionBase(unittest.TestCase):
    def test_valid_transaction_base(self):
        transaction = TransactionBase(asset_id=2, amount=Decimal("100.00"))
        self.assertEqual(transaction.asset_id, 2)

    def test_negative_asset_id(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(asset_id=-2, amount=Decimal("100.00"))
        self.assertIn("type=greater_than_equal", str(context.exception))

    def test_negative_amount(self):
        with self.assertRaises(ValidationError) as context:
            TransactionBase(asset_id=2, amount=Decimal("-100.00"))
        self.assertIn("type=greater_than", str(context.exception))


if __name__ == "__main__":
    unittest.main()
