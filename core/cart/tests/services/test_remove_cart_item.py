from django.contrib.auth import get_user_model
from django.test import TestCase
from products.models import Category, Product
from cart.services import remove_cart_item
from cart.models import CartItem

User = get_user_model()


class TestRemoveCartItemService(TestCase):
    """
    Test remove cart item service.
    """
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
    
    def test_remove_cart_item(self):
        """
        Test remove a cart item.
        """
        remove_cart_item(self.cart, self.product.pk)
        
        self.assertFalse(
            CartItem.objects.filter(
                cart=self.cart,
                product=self.product
            ).exists()
        )