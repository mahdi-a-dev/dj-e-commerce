from django.test import TestCase
from accounts.forms import LoginForm
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginTests(TestCase):
    """
    Test user login
    """
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("accounts:login")
        
        cls.user = User.objects.create_user(
            phone_number="09102263465",
            password="password-123"
        )
        
        cls.valid_data = {
            "username": "09102263465",
            "password": "password-123"
        }
        
    
    def test_user_can_login(self):
        """
        test valid user login successfully.
        """
        response = self.client.post(
            self.url,
            data=self.valid_data
        )
        
        self.assertEqual(response.status_code, 302)
        
        self.assertEqual(
            self.client.session["_auth_user_id"],
            str(self.user.pk)
        )
    
    def test_data_is_valid(self):
        """
        Test from is valid or invalid.
        """
        valid_form = LoginForm(
            data=self.valid_data
        )
        
        # invalid email
        invalid_form = LoginForm(
            data={
                "username": "invalid-phone",
                "password": "password1-123"
            }
        )
        
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())