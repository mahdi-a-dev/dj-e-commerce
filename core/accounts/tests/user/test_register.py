from django.test import TestCase
from accounts.forms import RegisterForm
from accounts.tests.mixins.user_mixin import UserAuthenticationTestMixin


class TestRegister(UserAuthenticationTestMixin, TestCase):
    """
    Test user registration
    """
    url_name = "accounts:register"
    form = RegisterForm
    username_field = "phone_number"
    
    valid_data = {
        "phone_number": "09102263465",
        "password1": "password-123",
        "password2": "password-123"
    }
    invalid_data = {
        "phone_number": "00910226346",
        "password1": "password-123",
        "password2": "password-123"
    }
    
    def test_duplicate_phone_number_is_rejected(self):
        """
        Test duplicate phone_number is rejected.
        """
        self.client.post(
            self.get_url(),
            data=self.valid_data
        )
        
        # user with the same phone_number
        form = self.form(
            data=self.valid_data
        )
        
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)