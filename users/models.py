from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User Model"""

    GENDER_CHOICE = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    LANGUAGE_CHOICE = (
        ("en", "English"),
        ("kr", "Korean"),
    )

    CURRENCY_CHOICE = (
        ("usd", "USD"),
        ("cad", "CAD"),
        ("krw", "KRW"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=6, blank=True)
    bio = models.TextField(blank=True)
    dob = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICE, max_length=2, blank=True, default="en"
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICE, max_length=3, blank=True, default="cad"
    )
    superhost = models.BooleanField(default=False)
