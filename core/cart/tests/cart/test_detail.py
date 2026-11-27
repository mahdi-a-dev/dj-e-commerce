from django.contrib.auth import get_user_model
from django.test import TestCase
from products.models import Category, Product
from common.tests.accress_mixin import (
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMixin
)

from cart.models import CartItem

user = get_user_model()


class TestCartDetailView(
    TestCase,
    AnonymousUserAccessMixin,
    AuthenticatedUserAccessMixin
    ):
    """
    Test CartDetailView.
    """
    url_name = "cart:detail"
    
    expected_get_status = 200
    expected_post_status = 405
    
    @classmethod
    def setUpTestData(cls):
        # The user to test cart
        cls.user = user.objects.create_user(
            phone_number="09101236789",
            password="password-123"
        )
        # The other user
        cls.other_user = user.objects.create_user(
            phone_number="09100000000",
            password="password-123"
        )
        # Users carts
        cls.cart = cls.user.cart
        cls.other_cart = cls.other_user.cart
        
        category = Category.objects.create(
            name="tech",
            slug="tech"
        )
        
        products = Product.objects.bulk_create(
            [
                Product(
                    category_id=category.pk,
                    title=f"Product {i}",
                    slug=f"Product-{i}",
                    price=1000 * i,
                    main_image=f"P {i}",
                    stock_quantity=4
                )
                for i in range(1, 6)
            ]
        )
        
        # Items present in the user's cart
        cls.cart_items = CartItem.objects.bulk_create(
            [
                CartItem(
                    cart=cls.cart,
                    product=product,
                    quantity=1
                )
                for product in products
            ]
        )
        
        
        
        other_product = Product.objects.create(
            category_id=category.pk,
            title="Other Product",
            slug="Other-Product",
            price=1000,
            main_image="other",
            stock_quantity=4  
        )
        # An item that is not present in the user's cart
        CartItem.objects.create(
            cart=cls.other_cart,
            product=other_product,
            quantity=1
        )
        
    def test_user_can_see_own_cart_items(self):
        """
        The user can only view items that belong to their own cart.
        """
        self.client.force_login(self.user)
        
        response = self.client.get(
            self.get_url()
        )
        
        self.assertEqual(response.status_code, 200)
        
        self.assertQuerySetEqual(
            response.context["cart_items"],
            self.cart_items,
            ordered=False
        )
        
    def test_user_cannot_see_other_users_cart_items(self):
        """
        The user cannot view items that do not belong to their own cart.
        """
        self.client.force_login(self.user)
        
        response = self.client.get(
            self.get_url()
        )
        
        self.assertEqual(response.status_code, 200)
        
        cart_items = response.context["cart_items"]
        
        self.assertEqual(
            {item.cart.id for item in cart_items},
            {self.cart.id}
        )