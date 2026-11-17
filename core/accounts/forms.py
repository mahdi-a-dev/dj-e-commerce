from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model
from accounts.models import Profile, Address


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["phone_number"]


class LoginForm(AuthenticationForm):
    username = PhoneNumberField(
        widget=forms.TextInput
    )
    


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["title", "province", "city", "postal_code", "full_address"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name"]
