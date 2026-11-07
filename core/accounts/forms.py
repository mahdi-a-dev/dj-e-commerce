from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model



class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["phone_number"]


class LoginForm(AuthenticationForm):
    username = PhoneNumberField(
        label="Phone number",
        widget=forms.TextInput
    )
    
    error_messages = {
        "invalid_login": "Phone number or password is invalid."
    }
    
    