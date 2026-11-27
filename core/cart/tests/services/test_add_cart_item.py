from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from products.models import Category, Product
from cart.services import add_cart_item
from cart.models import CartItem

user = get_user_model()


class TestAddCartItemService(TestCase):
    """
    Test add cart item service.
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
    
    def test_adding_a_item_successful(self):
        add_cart_item(self.cart, self.product.pk)
        
        self.cart.refresh_from_db()
        
        self.assertTrue(
            CartItem.objects.filter(
                cart=self.cart,
                product=self.product
            ).exists()
        )
    
    def test_adding_a_item_failed(self):
        product = Product.objects.create(
            category_id=self.category.pk,
            title="Product",
            slug="Product",
            price=1000,
            main_image="other",
            stock_quantity=0  
        )
        
        with self.assertRaises(ValidationError):
            add_cart_item(self.cart, product.pk)
            
    def test_Adding_duplicate_item_does_not_result_in_an_increase_in_quantity(self):
        add_cart_item(self.cart, self.product.pk)
        add_cart_item(self.cart, self.product.pk)
        
        item = CartItem.objects.get(
            cart=self.cart,
            product=self.product    
        )
        
        self.assertEqual(item.quantity, 1)
        