import unittest
from datetime import date
from decimal import Decimal

from pydantic import ValidationError
from assets.schemas import AssetBase


class TestAssetBase(unittest.TestCase):
    def test_invalid_name_length(self):
        with self.assertRaises(ValidationError) as context:
            AssetBase(
                company_id=1,
                name="",
                listed_year=2020,
                ticker="ASSET1",
                description="A valid description.",
                available_count=10,
                price=Decimal("100.00"),
            )
        self.assertIn("type=string_too_short", str(context.exception))

    def test_future_listed_year(self):
        current_year = date.today().year
        with self.assertRaises(ValidationError) as context:
            AssetBase(
                company_id=1,
                name="Valid Asset Name",
                listed_year=current_year + 1,
                ticker="ASSET1",
                description="A valid description.",
                available_count=10,
                price=Decimal("100.00"),
            )
        self.assertIn("type=less_than_equal", str(context.exception))

    def test_invalid_available_count(self):
        with self.assertRaises(ValidationError) as context:
            AssetBase(
                company_id=1,
                name="Valid Asset Name",
                listed_year=2020,
                ticker="ASSET1",
                description="A valid description.",
                available_count=-1,
                price=Decimal("100.00"),
            )
        self.assertIn("type=greater_than_equal", str(context.exception))

    def test_invalid_price(self):
        with self.assertRaises(ValidationError) as context:
            AssetBase(
                company_id=1,
                name="Valid Asset Name",
                listed_year=2020,
                ticker="ASSET1",
                description="A valid description.",
                available_count=10,
                price=Decimal("0"),
            )
        self.assertIn("type=greater_than", str(context.exception))

    def test_valid_asset(self):
        asset = AssetBase(
            company_id=1,
            name="Valid Asset Name",
            listed_year=2020,
            ticker="ASSET1",
            description="A valid description.",
            available_count=10,
            price=Decimal("100.00"),
        )
        self.assertEqual(asset.available_count, 10)
        self.assertEqual(asset.price, Decimal("100.00"))


if __name__ == "__main__":
    unittest.main()
