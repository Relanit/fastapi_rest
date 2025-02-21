import unittest
from datetime import date
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
                price=100.0
            )
        self.assertIn("Название актива должно содержать хотя бы 1 символ", str(context.exception))

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
                price=100.0
            )
        self.assertIn("Год листинга не может быть в будущем", str(context.exception))

    def test_invalid_available_count(self):
        with self.assertRaises(ValidationError) as context:
            AssetBase(
                company_id=1,
                name="Valid Asset Name",
                listed_year=2020,
                ticker="ASSET1",
                description="A valid description.",
                available_count=-1,
                price=100.0
            )
        self.assertIn("Количество доступных единиц должно быть неотрицательным", str(context.exception))

    def test_invalid_price(self):
        with self.assertRaises(ValidationError) as context:
            AssetBase(
                company_id=1,
                name="Valid Asset Name",
                listed_year=2020,
                ticker="ASSET1",
                description="A valid description.",
                available_count=10,
                price=0
            )
        self.assertIn("Цена должна быть положительной", str(context.exception))

    def test_valid_asset(self):
        asset = AssetBase(
            company_id=1,
            name="Valid Asset Name",
            listed_year=2020,
            ticker="ASSET1",
            description="A valid description.",
            available_count=10,
            price=100.0
        )
        self.assertEqual(asset.available_count, 10)
        self.assertEqual(asset.price, 100.0)


if __name__ == '__main__':
    unittest.main()
