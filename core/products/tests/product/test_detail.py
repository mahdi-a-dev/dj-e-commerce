from django.test import TestCase
from products.models import Product, Category
from django.urls import reverse
from products.tests.mixins.product_mixin import ActiveProductTestMixin


class ProductDetailTest(ActiveProductTestMixin, TestCase):
    """
    Test ProductDetail view.
        
    Use ActiveProductTestMixin which contains Active product Tests. 
    """
    @classmethod
    def setUpTestData(cls):
        # Initializing Categories and Products
        
        category = Category.objects.create(
            name="tech",
            slug="tech"
        )
        
        # Active product to be displayed
        cls.active_product = Product.objects.create(
            category_id=category.pk,
            title="product-1",
            slug="product-1",
            price="23400",
            main_image="product",
            stock_quantity=30,
        )
        
        # Inactive product that should not be displayed
        cls.inactive_product = Product.objects.create(
            category_id=category.pk,
            title="product-2",
            slug="product-2",
            price="26400",
            main_image="product",
            stock_quantity=30,
            is_active=False
        )
        
        # View url
        cls.url = reverse(
            "products:detail",
            kwargs={
                "pk": cls.active_product.pk,
                "slug": cls.active_product.slug
            }
        )
        