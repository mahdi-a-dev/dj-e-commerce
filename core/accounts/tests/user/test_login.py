from django.test import TestCase
from accounts.forms import LoginForm
from django.contrib.auth import get_user_model
from accounts.tests.mixins.user_mixin import UserAuthenticationTestMixin

User = get_user_model()


class LoginTests(UserAuthenticationTestMixin, TestCase):
    """
    Test user login
    """
    url_name = "accounts:login"
    form = LoginForm
    username_field = "username"
    
    valid_data = {
        "username": "09102263465",
        "password": "password-123"
    }
    invalid_data = {
        "username": "00910226346",
        "password1": "password-123"
    }
    
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09102263465",
            password="password-123"
        )
    
        self.assertTrue(User.objects.filter(
            phone_number=self.user.phone_number
        ).exists())