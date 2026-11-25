from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Profile
from accounts.tests.mixins.accress_mixin import AccessTestMixin

User = get_user_model()


class EditProfileTests(AccessTestMixin, TestCase):
    """
    Test EditProfile view.
    """
    
    url_name = "accounts:edit-profile"
    valid_data = {
        "first_name": "mohammadreza",
        "last_name": "admadi",
    }
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            phone_number="09122589632",
            password="regular-password-123"
        )
        
        cls.profile = cls.user.profile
        
    def test_users_can_edit_profile(self):
        """
        Test users can edit their profile.
        """
        self.client.force_login(self.user)
        
        response = self.client.post(
            self.get_url(),
            self.valid_data
        )
            
        self.assertEqual(response.status_code, 302)
        
        self.profile.refresh_from_db()
        
        self.assertEqual(
            self.profile.first_name,
            self.valid_data["first_name"]
        )
        
        self.assertEqual(
            self.profile.last_name,
            self.valid_data["last_name"]
        )