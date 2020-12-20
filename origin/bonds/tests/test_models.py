from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from bonds import models

class CustomValidatorsTestCase(TestCase):
    def test_positive_validator__valid(self):
        models.validate_positive(10)

    def test_positive_validator__invalid_negative(self):
        with self.assertRaises(ValidationError):
            models.validate_positive(-1)

    def test_positive_validator__invalid_zero(self):
        with self.assertRaises(ValidationError):
            models.validate_positive(0)

    def test_currrency_code__valid(self):
        models.validate_currency_code("EUR")

    def test_currrency_code__invalid(self):
        with self.assertRaises(ValidationError):
            models.validate_currency_code("ER")

    def test_isin_length__valid(self):
        models.validate_isin_length("123456781234")

    def test_isin_length__invalid(self):
        with self.assertRaises(ValidationError):
            models.validate_isin_length("123")

    def test_lei_length__valid(self):
        models.validate_lei_length("12345678901234567890")

    def test_lei_length__invalid(self):
        with self.assertRaises(ValidationError):
            models.validate_lei_length("123")


class BondModelTestCase(TestCase):
    def test_bond_model_str(self):
        bond = models.Bond(
            user = User.objects.create_user(username="test"),
            isin = "123456781234",
            size = 100,
            currency = "EUR",
            maturity = "2020-12-25",
            lei = "12312312312312312312",
            legal_name = "test legal name"
        )
        assert str(bond) == "isin: 123456781234, user: 1"

    def test_bond_model__valid(self):
        bond = models.Bond(
            user = User.objects.create_user(username="test"),
            isin = "123456781234",
            size = 100,
            maturity = "2020-12-25",
            currency = "EUR",
            lei = "12312312312312312312",
            legal_name = "test legal name"
        )
        bond.save()

    def test_bond_model__invalid_lei(self):
        bond = models.Bond(
            user = User.objects.create_user(username="test"),
            isin = "123456781234",
            size = 100,
            maturity = "2020-12-25",
            currency = "EUR",
            lei = "1231231231231231231a",
            legal_name = "test legal name"
        )
        with self.assertRaises(ValidationError) as e:
            bond.full_clean()

    def test_bond_model__invalid_isin(self):
        bond = models.Bond(
            user = User.objects.create_user(username="test"),
            isin = "1234567812a4",
            size = 100,
            maturity = "2020-12-25",
            currency = "EUR",
            lei = "12312312312312312312",
            legal_name = "test legal name"
        )
        with self.assertRaises(ValidationError) as e:
            bond.full_clean()