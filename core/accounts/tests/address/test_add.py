from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Address
from common.tests.accress_mixin import (
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMixin
)

User = get_user_model()


class AddAddressTests(
    TestCase,
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMixin
    ):
    """
    Test AddAddress view.
    """
    url_name = "accounts:add"
    valid_data = {
        "title": "home address",
        "province": "Tehran",
        "city": "Tehran",
        "postal_code": "3325214502",
        "full_address": "user address"
    }
    
    expected_get_status = 200
    expected_post_status = 302
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            phone_number="09122589632",
            password="regular-password-123"
        )
        
        
    def test_user_can_add_address(self):
        """
        Test user can add address.
        """
        self.client.force_login(self.user)
        
        response = self.client.post(
            self.get_url(),
            self.valid_data
        )
            
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Address.objects.filter(
                user=self.user,
                title=self.valid_data["title"]
            ).exists()
        )