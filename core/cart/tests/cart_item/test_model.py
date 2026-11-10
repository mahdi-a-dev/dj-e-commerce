from django.test import TestCase
from cart.models import Cart, CartItem
from products.models import Product, Category
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

user = get_user_model()


class TestCartItemModel(TestCase):

    @classmethod
    def setUpTestData(self):
        self.user = user.objects.create_user(
            phone_number="09101478512",
            password="user-password-123"
        )
        self.cart = Cart.objects.create(
            user=self.user
        )
        self.category = Category.objects.create(name='django', slug='django')
        self.product = Product.objects.create(
            category_id=self.category.pk,
            title='django beginners',
            slug='django-beginners',
            main_image='django',
            stock_quantity=2,
            price='20'
        )
        
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )

    def test_cart_item_model_entry(self):
        """
        Test CartItem model data insertion/types/field attributes
        """
        data = self.cart_item
        self.assertTrue(isinstance(data, CartItem))
        self.assertEqual(str(data), f"{self.product.title} - {data.cart.user.phone_number.as_national}")

    def test_unique_product_per_cart(self):
        """
        Test Saving a `CartItem` fails when the shopping cart and the product are not unique.
        """
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                CartItem.objects.create(
                    cart=self.cart,
                    product=self.product,
                    quantity=1
                )