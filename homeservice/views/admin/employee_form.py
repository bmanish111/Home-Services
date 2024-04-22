# forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.contrib.auth import get_user_model
from django.utils.html import escape, mark_safe

User = get_user_model()


class MyForm(forms.Form):
    fullname = forms.CharField(
        max_length=50,
        required=True,
        validators=[
            RegexValidator(
                regex="^[A-Za-z]+(?:\s[A-Za-z]\.?|(?:\s[A-Za-z]+)+)?$",
                message="Full name should contain only alphabetic characters.",
                code="invalid_name",
            ),
        ],
    )

    def clean_fullname(self):
        fullname = self.cleaned_data.get("fullname")
        # Split the full name into words
        words = fullname.split()

        # Check if there are exactly two words
        if len(words) < 2:
            raise forms.ValidationError("Full name must contain atleast two words.")

    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    phone = forms.CharField(
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

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("This phone number is already in use.")
        return phone

    address = forms.CharField(max_length=100, required=True)
    gender = forms.ChoiceField(
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    )

    experience = forms.CharField(required=True)

    def clean_experience(self):
        experience = self.cleaned_data.get("experience")

        if not experience.isdigit():
            raise forms.ValidationError("This field must contain only numbers.")

        return experience

    bio = forms.CharField(widget=forms.Textarea)

    def clean_bio(self):
        bio = self.cleaned_data["bio"]

        # Escape HTML characters to prevent XSS
        escaped_bio = escape(bio)

        # Check if the escaped bio is equal to the original bio
        # If not, it means HTML tags were present in the original input
        if escaped_bio != bio:
            raise ValidationError(
                "Invalid input. Please enter plain text without HTML tags."
            )

        return mark_safe(escaped_bio)

    previous_work = forms.CharField(widget=forms.Textarea)

    def clean_previous_work(self):
        previous_work = self.cleaned_data["previous_work"]

        # Escape HTML characters to prevent XSS
        escaped_previous_work = escape(previous_work)

        # Check if the escaped previous_work is equal to the original previous_work
        # If not, it means HTML tags were present in the original input
        if escaped_previous_work != previous_work:
            raise ValidationError(
                "Invalid input. Please enter plain text without HTML tags."
            )

        return mark_safe(escaped_previous_work)

    previous_experience = forms.CharField(widget=forms.Textarea)

    def clean_previous_experience(self):
        previous_experience = self.cleaned_data["previous_experience"]

        # Escape HTML characters to prevent XSS
        escaped_previous_experience = escape(previous_experience)

        # Check if the escaped previous_experience is equal to the original previous_experience
        # If not, it means HTML tags were present in the original input
        if escaped_previous_experience != previous_experience:
            raise ValidationError(
                "Invalid input. Please enter plain text without HTML tags."
            )

        return mark_safe(escaped_previous_experience)

    profile_pic = forms.FileField()

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get("profile_pic")

        if not profile_pic:
            raise forms.ValidationError("File is required.")

        return profile_pic

    picture_of_id = forms.FileField()

    def clean_picture_of_id(self):
        picture_of_id = self.cleaned_data.get("picture_of_id")

        if not picture_of_id:
            raise forms.ValidationError("File is required.")

        return picture_of_id
