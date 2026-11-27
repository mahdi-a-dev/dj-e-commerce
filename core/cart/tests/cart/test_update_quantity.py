from django.contrib.auth import get_user_model
from django.test import TestCase
from products.models import Category, Product
from common.tests.accress_mixin import AnonymousUserAccessMixin, AuthenticatedUserAccessMixin
from cart.models import CartItem

user = get_user_model()


class TestAddItemView(
    TestCase,
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMixin
    ):
    
    url_name = "cart:update-quantity"
    valid_data = {
        "quantity": 4
    }
    
    expected_get_status = 405
    expected_post_status = 302
    
    @classmethod
    def setUpTestData(cls):
        cls.user = user.objects.create_user(
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
        
        cls.cart_item = CartItem.objects.create(
            cart=cls.cart,
            product=cls.product
        )
    
    def get_url_kwargs(self):
        return {"pk": self.product.pk}

    def test_user_can_update_item_quantity(self):
        self.client.force_login(self.user)
        
        response = self.client.post(
            self.get_url(),
            self.valid_data
        )
        
        self.assertEqual(response.status_code, 302)
        
        self.cart_item.refresh_from_db()
        
        self.assertEqual(
            self.cart_item.quantity,
            4
        )