from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthenticationTestMixin:
    """
    """
    
    url_name = None
    form = None
    username_field = None
    
    valid_data = {}
    invalid_data = {}
    
    def get_url(self):
        return reverse(
            self.url_name
        )
    
    def test_successful(self):
        """
        test valid user register/login successfully.
        """
        self.client.post(
            self.get_url(),
            data=self.valid_data
        )
        
        self.assertTrue(
            User.objects.filter(
                phone_number=self.valid_data[self.username_field]
            ).exists())
    
    def test_registeration_data_is_valid(self):
        """
        Test from is valid or invalid.
        """
        valid_form = self.form(
            data=self.valid_data
        )
        
        # invalid email
        invalid_form = self.form(
            data=self.invalid_data
        )
        
        self.assertTrue(valid_form.is_valid())
        self.assertFalse(invalid_form.is_valid())
