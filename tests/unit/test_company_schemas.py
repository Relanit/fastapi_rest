import unittest
from datetime import date, timedelta
from pydantic import ValidationError
from companies.schemas import CompanyBase, CompanyCreate, CompanyPatchUpdate


class TestCompanySchemas(unittest.TestCase):
    def test_company_base_valid(self):
        data = {
            "name": "  john doe  ",
            "profile": "A leading company.",
            "foundation_date": "1980-01-01"
        }
        company = CompanyBase(**data)
        self.assertEqual(company.name, "John Doe")  # Проверяем форматирование имени
        self.assertEqual(company.profile, "A leading company.")
        self.assertEqual(company.foundation_date, date(1980, 1, 1))

    def test_company_base_invalid_name(self):
        data = {"name": "A", "foundation_date": "1980-01-01"}
        with self.assertRaises(ValidationError) as context:
            CompanyBase(**data)
        self.assertIn("Название компании должно содержать от 2 до 100 символов", str(context.exception))

    def test_company_base_invalid_foundation_date_format(self):
        data = {"name": "John Doe", "foundation_date": "01-01-1980"}
        with self.assertRaises(ValidationError) as context:
            CompanyBase(**data)
        self.assertIn("Неверный формат даты. Используйте 'YYYY-MM-DD'", str(context.exception))

    def test_company_base_invalid_foundation_date_future(self):
        future_date = (date.today() + timedelta(days=1)).isoformat()
        data = {"name": "John Doe", "foundation_date": future_date}
        with self.assertRaises(ValidationError) as context:
            CompanyBase(**data)
        self.assertIn("Дата основания не может быть в будущем", str(context.exception))

    def test_company_create_valid(self):
        data = {"name": "John Doe", "foundation_date": "1980-01-01"}
        company = CompanyCreate(**data)
        self.assertEqual(company.name, "John Doe")
        self.assertEqual(company.foundation_date, date(1980, 1, 1))

    def test_company_patch_update_partial(self):
        data = {"name": None, "foundation_date": "2000-03-10"}
        with self.assertRaises(ValidationError):
            CompanyPatchUpdate(**data)


if __name__ == "__main__":
    unittest.main()
