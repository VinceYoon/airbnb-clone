import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string


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
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            self.send_email(secret)
            self.save()
        return

    def send_email(self, secret):
        email_template = render_to_string(
            "emails/verify_email.html", {"secret": secret}
        )
        send_mail(
            "Verify Airbnb Account",
            strip_tags(email_template),
            settings.EMAIL_FROM,
            [self.email],
            fail_silently=False,
            html_message=email_template,
        )
        return
