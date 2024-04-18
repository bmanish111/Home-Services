# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.contrib.auth import get_user_model

User = get_user_model()


class MyForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        required=True,
        validators=[
            RegexValidator(
                regex="^[A-Za-z]+(?:\s[A-Za-z]\.?|(?:\s[A-Za-z]+)+)?$",
                message="First name should contain only alphabetic characters.",
                code="invalid_name",
            ),
        ],
    )

    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    contact = forms.CharField(
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                regex="^\+?[0-9]+([-.\s]?[0-9]+)*$",
                message="Phone number should contain only numeric value.",
                code="invalid_name",
            ),
        ],
    )

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")
        if User.objects.filter(phone=contact).exists():
            raise ValidationError("This contact number is already in use.")
        return contact

    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

    def clean_password(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
