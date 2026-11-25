from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from accounts.models import Profile

User = get_user_model()


class TestProfileModel(TestCase):
    """
    Test profile model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09302263666",
            password="user-password-123"
        )
        
        self.profile = self.user.profile
        
        self.profile.first_name = "mohammadreza"
        self.profile.last_name = "ahmadi"
        
        self.profile.save(update_fields=["first_name", "last_name"])
    
    def test_profile_model_entry(self):
        """
        Test profile model data insertion/types/field attributes
        """
        data = self.profile
        self.assertTrue(isinstance(data, Profile))
        
        data_str = f"{data.first_name}-{data.last_name}"
        self.assertEqual(str(data), data_str)

        