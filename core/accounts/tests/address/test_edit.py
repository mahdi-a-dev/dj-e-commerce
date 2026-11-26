from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Address
from common.tests.accress_mixin import (
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMixin
)

User = get_user_model()


class EditAddressTests(
    TestCase,
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMixin
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

        # other user
        user = User.objects.create_user(
            phone_number="09102233696",
            password="password-123"
        )
        
        # other address
        cls.other_address = Address.objects.create(
            user=user,
            title="word address",
            province="Qazvin",
            city="Qazvin",
            postal_code="3516454502",
            full_address="address"   
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
    
    def test_user_cannot_edit_other_users_address(self):
        """
        Test user cannot edit other users address.
        """
        self.client.force_login(self.user)
        
        response = self.client.post(
            reverse(
                self.url_name,
                kwargs={"pk": self.other_address.pk}
            ),
            self.valid_data
        )
        
        self.assertEqual(response.status_code, 404)
        
        self.other_address.refresh_from_db()
        
        self.assertNotEqual(
            self.other_address.title,
            self.valid_data["title"]
        )