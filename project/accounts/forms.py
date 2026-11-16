# forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class SignupForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=150,  # email is stored in User.username (150 char limit)
        error_messages={
            "required": "Email is required.",
            "invalid": "Enter a valid email address.",
        },
    )

    password1 = forms.CharField(
        required=True,
        strip=False,
        widget=forms.PasswordInput(),
        validators=[validate_password],
        error_messages={
            "required": "Password is required.",
        },
    )

    password2 = forms.CharField(
        required=True,
        strip=False,
        widget=forms.PasswordInput(),
        error_messages={
            "required": "Please confirm your password.",
        },
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords don't match.")

        return cleaned

    