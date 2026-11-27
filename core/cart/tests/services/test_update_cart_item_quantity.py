from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from products.models import Category, Product
from cart.services import update_cart_item_quantity
from cart.models import CartItem

User = get_user_model()


class TestUpdateCartItemQuantityService(TestCase):
    """
    Test update cart item quantity service.
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
        
        cls.cart_item = CartItem.objects.create(
            cart=cls.cart,
            product=cls.product
        )
    
    def test_update_cart_item_quantity(self):
        """
        Test update item quantity for valid product.
        """
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
        
    def test_update_quantity_for_unavailable_product_failed(self):
        """
        Test update quantity for unavailable product failed.
        """
        self.product.delete()
        
        with self.assertRaises(CartItem.DoesNotExist):
            update_cart_item_quantity(
                self.cart,
                self.cart_item.pk,
                1
            )
            
    def test_update_quantity_for_inactive_item_failed(self):
        """
        Test update quantity for inactive product failed.
        """        
        self.product.is_active = False
        
        self.product.save(update_fields=["is_active"])
        
        with self.assertRaises(ValidationError):
            update_cart_item_quantity(
                self.cart,
                self.cart_item.pk,
                2
            )
            
    def test_update_quantity_for_out_of_stock_item_failed(self):
        """
        Test update quantity for a out of stock product failed.
        """
        self.product.stock_quantity = 0
        self.product.save(update_fields=["stock_quantity"])
        
        with self.assertRaises(ValidationError):
            update_cart_item_quantity(
                self.cart,
                self.cart_item.pk,
                1
            )
    
    def test_item_with_insufficient_stock_will_not_be_increased(self):
        """
        Test item with issufficient stock will not be increased.
        """
        with self.assertRaises(ValidationError):
            update_cart_item_quantity(
                cart=self.cart,
                item_pk=self.cart_item.pk,
                quantity=5
            )
        
        self.cart_item.refresh_from_db()
        
        self.assertEqual(self.cart_item.quantity, 1)
        
    
    
        
        