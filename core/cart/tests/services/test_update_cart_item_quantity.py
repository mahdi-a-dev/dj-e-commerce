from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from products.models import Category, Product
from cart.services import update_cart_item_quantity
from cart.models import CartItem

user = get_user_model()


class TestRemoveCartItemService(TestCase):
    """
    Test update cart item quantity service.
    """
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
    
    def test_update_cart_item_quantity(self):
        update_cart_item_quantity(
            cart=self.cart,
            item_pk=self.cart_item.pk,
            quantity=2
        )
        
        item = CartItem.objects.get(
            cart=self.cart,
            product=self.product
        )
        
        self.assertEqual(
            item.quantity,
            2
        )
    
    def test_item_with_insufficient_stock_will_not_be_increased(self):
        product = Product.objects.create(
            category_id=self.category.pk,
            title="Product",
            slug="Product",
            price=1000,
            main_image="other",
            stock_quantity=3
        )
        
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=product
        )
        
        with self.assertRaises(ValidationError):
            update_cart_item_quantity(
                cart=self.cart,
                item_pk=cart_item.pk,
                quantity=4
            )