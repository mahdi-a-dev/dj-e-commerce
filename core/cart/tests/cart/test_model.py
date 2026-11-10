from django.test import TestCase
from cart.models import Cart
from django.contrib.auth import get_user_model

user = get_user_model()


class TestCartModel(TestCase):

    def setUp(self):
        self.user = user.objects.create_user(
            phone_number="09101478512",
            password="user-password-123"
        )
        self.cart = Cart.objects.create(
            user=self.user
        )

    def test_cart_model_entry(self):
        """
        Test Cart model data insertion/types/field attributes
        """
        data = self.cart
        self.assertTrue(isinstance(data, Cart))
        self.assertEqual(str(data), f"Cart - ({data.user.phone_number.as_national})")
