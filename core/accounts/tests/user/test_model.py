from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

User = get_user_model()


class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09302263666",
            password="user-password-123"
        )
    
    def test_user_model_entry(self):
        """
        Test user model data insertion/types/field attributes
        """
        data = self.user
        self.assertTrue(isinstance(data, User))
        self.assertEqual(str(data), data.phone_number)
    
    def test_unique_phone_number(self):
        """
        Test phone_number filed must be unique
        """
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create(
                    phone_number=self.user.phone_number,
                    password="new-password-123"
                )
        