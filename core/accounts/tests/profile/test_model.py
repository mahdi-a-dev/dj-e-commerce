from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from accounts.models import Profile

User = get_user_model()


class TestProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09302263666",
            password="user-password-123"
        )

        self.profile = Profile.objects.create(
            user=self.user,
            first_name="mohammadreza",
            last_name="ahmadi",
            email="user@gmail.com"
        )
    
    def test_profile_model_entry(self):
        """
        Test profile model data insertion/types/field attributes
        """
        data = self.profile
        self.assertTrue(isinstance(data, Profile))
        
        data_str = f"{data.user.phone_number} - {data.first_name} {data.last_name}"
        self.assertEqual(str(data), data_str)
    
    def test_unique_email(self):
        """
        Test email filed must be unique
        """
        user = User.objects.create_user(
            phone_number="09102541425",
            password="new-password-123"
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Profile.objects.create(
                    user=user,
                    first_name="reza",
                    last_name="ahmadi",
                    email=self.profile.email
                )
        