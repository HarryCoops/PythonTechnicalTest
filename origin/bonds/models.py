from django.db import models
from django.contrib.auth.models import User  
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from bonds.settings import CURRENCY_CODES

def validate_positive(value):
    if value <= 0:
        raise ValidationError(f"{value} is not a positive integer")

def validate_currency_code(value):
    if value not in CURRENCY_CODES:
        raise ValidationError(f"{value} currency code does not exist")

def validate_isin_length(value):
    if len(value) != 12:
        raise ValidationError(f"{value} has invalid length for ISIN")

def validate_lei_length(value):
    if len(value) != 20:
        raise ValidationError(f"{value} has invalid length for lei")


class Bond(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isin = models.CharField(max_length=12, validators=[
        RegexValidator(
            regex=r"^[A-Z0-9]*$",
            message="ISIN must be an uppercase alphanumeric string",
            code="invalid_isin"
        ),
        validate_isin_length
    ])
    size = models.IntegerField(validators=[validate_positive])
    currency = models.CharField(max_length=3, validators=[validate_currency_code])
    maturity = models.DateField()
    lei = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex=r"^[A-Z0-9]*$",
            message="LEI must be an uppercase alphanumeric string",
            code="invalid_lei"
        ),
        validate_lei_length
    ])
    legal_name = models.CharField(max_length=100)
    created = models.DateField(auto_now=True)

    class Meta:
        unique_together = ("user", "isin")
        indexes = [
            models.Index(fields=["user", "isin"])
        ]
    def __str__(self):
        return f"isin: {self.isin}, user: {self.user.id}"
    