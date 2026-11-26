from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Address
from common.tests.accress_mixin import (
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMisin
)

User = get_user_model()


class EditAddressTests(
    TestCase,
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMisin
    ):
    """
    Test EditAddress view.
    """
    url_name = "accounts:edit"
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
           
        # The address we use for edit
        cls.address = Address.objects.create(
            user=cls.user,
            title="home",
            province="Qazvin",
            city="Qazvin",
            postal_code="3345454502",
            full_address="user address"
        )

    def get_url_kwargs(self):
        return {"pk": self.address.pk}
        
    def test_user_can_edit_address(self):
        """
        Test users can edit thier addresses.
        """
        self.client.force_login(self.user)
        
        response = self.client.post(
            self.get_url(),
            self.valid_data
        )
            
        self.assertEqual(response.status_code, 302)

        self.address.refresh_from_db()
        
        self.assertEqual(
            self.address.title,
            self.valid_data["title"]
        )
        
        self.assertEqual(
            self.address.full_address,
            self.valid_data["full_address"]
        )