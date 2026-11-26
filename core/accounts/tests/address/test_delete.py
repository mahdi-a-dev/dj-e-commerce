from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Address
from common.tests.accress_mixin import (
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMisin
)

User = get_user_model()


class DeleteAddressTests(
    TestCase,
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMisin
    ):
    """
    Test DeleteAddress view.
    """
    url_name = "accounts:delete"
    
    expected_get_status = 200
    expected_post_status = 302
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            phone_number="09122589632",
            password="regular-password-123"
        )
           
        # The address we use for delete
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
        
    def test_user_can_delete_address(self):
        """
        Test users can delete thier addresses.
        """
        self.client.force_login(self.user)
        
        response = self.client.post(
            self.get_url()
        )
            
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Address.objects.filter(
                pk=self.address.pk
            ).exists()
        )