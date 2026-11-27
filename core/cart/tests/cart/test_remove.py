from django.contrib.auth import get_user_model
from django.test import TestCase
from products.models import Category, Product
from cart.models import CartItem
from common.tests.accress_mixin import (
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMixin
)
User = get_user_model()


class TestRemoveItemView(
    TestCase,
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMixin
    ):
    """
    Test remove item view.
    """
    url_name = "cart:remove"
    
    expected_get_status = 405
    expected_post_status = 302
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            phone_number="09190000000",
            password="test-123"
        )
        
        cls.cart = cls.user.cart
        
        cls.category = Category.objects.create(
            name="tech",
            slug="tech"
        )
        
        cls.product = Product.objects.create(
            category_id=cls.category.pk,
            title="Product",
            slug="Product",
            price=1000,
            main_image="other",
            stock_quantity=4 
        )
        
        CartItem.objects.create(
            cart=cls.cart,
            product=cls.product
        )
    
    def get_url_kwargs(self):
        return {"product_pk": self.product.pk}
    
    def test_user_can_remove_item(self):
        """
        Test user can remove item.
        """
        self.client.force_login(self.user)
        
        response = self.client.post(
            self.get_url()
        )
        
        self.assertEqual(response.status_code, 302)
        
        self.assertFalse(
            CartItem.objects.filter(
                cart=self.cart,
                product=self.product
            ).exists()
        )