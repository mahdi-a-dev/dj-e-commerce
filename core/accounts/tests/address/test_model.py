from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Address

User = get_user_model()


class TestAddressModel(TestCase):
    """
    Test address model.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09302263666",
            password="user-password-123"
        )

        self.address = Address.objects.create(
            user=self.user,
            title="home address",
            province="Tehran",
            city="Tehran",
            postal_code="3325214502",
            full_address="user address"
        )
    
    def test_address_model_entry(self):
        """
        Test address model data insertion/types/field attributes
        """
        data = self.address
        self.assertTrue(isinstance(data, Address))

        self.assertEqual(str(data), data.title)
    
        