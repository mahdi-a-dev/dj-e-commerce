from django.test import TestCase
from accounts.forms import RegisterForm
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class TestRegister(TestCase):
    """
    Test user registration
    """
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("accounts:register")
   
        cls.valid_data = {
            "phone_number": "09102263465",
            "password1": "password-123",
            "password2": "password-123"
        }   
    
    def test_user_can_regiser(self):
        """
        test valid user register successfully.
        """
        self.client.post(
            self.url,
            data=self.valid_data
        )
        
        self.assertTrue(
            User.objects.filter(
                phone_number=self.valid_data["phone_number"]
            ).exists())
    
    def test_data_is_valid(self):
        """
        Test from is valid or invalid.
        """
        valid_form = RegisterForm(
            data=self.valid_data
        )
        
        # invalid email
        invalid_form = RegisterForm(
            data={
                "phone_number": "invalid-phone",
                "password1": "password-123",
                "password2": "password-123"
            }
        )
        
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())
    
    def test_duplicate_phone_number_is_rejected(self):
        """
        Test duplicate phone_number is rejected.
        """
        self.client.post(
            self.url,
            data=self.valid_data
        )
        
        # user with the same phone_number
        form = RegisterForm(
            data=self.valid_data
        )
        
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)