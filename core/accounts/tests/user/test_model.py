from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

User = get_user_model()


class TestUserModel(TestCase):
    """
    Test custome user model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09302263666",
            password="user-password-123"
        )
    
    def test_user_model_entry(self):
        """
        Test user model data insertion/types/field attributes.
        """
        data = self.user
        self.assertTrue(isinstance(data, User))
        self.assertEqual(str(data), data.phone_number)
    
    def test_unique_phone_number(self):
        """
        Test phone_number filed must be unique.
        """
        with self.assertRaises(IntegrityError), transaction.atomic():
            User.objects.create(
                phone_number=self.user.phone_number,
                password="new-password-123"
            )
    
    def test_create_superuser(self):
        """
        Test create_superuser method.
        """
        superuser = User.objects.create_superuser(
            phone_number="09333695821",
            password="user-password-456"
        )
        
        self.assertTrue(
            User.objects.filter(
                phone_number=superuser.phone_number,
                is_superuser=True
            ).exists())
        