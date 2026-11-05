from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Address

User = get_user_model()


class TestAddressModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09302263666",
            password="user-password-123"
        )

        self.address = Address.objects.create(
            user=self.user,
            title="home address",
            province="qazvin",
            city="abyek",
            postal_code="3325214502",
            address="user address"
        )
    
    def test_address_model_entry(self):
        """
        Test address model data insertion/types/field attributes
        """
        data = self.address
        self.assertTrue(isinstance(data, Address))
        
        data_str = f"{data.user.phone_number} - {data.title}"
        self.assertEqual(str(data), data_str)
    
        