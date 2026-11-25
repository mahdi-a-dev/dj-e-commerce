from django.test import TestCase
from products.models import Product, Category
from django.urls import reverse
from products.tests.mixins.product_mixin import ProductListTestMixin


class ProductListTests(ProductListTestMixin, TestCase):
    """
    Test ProductList view.
    
    Use ProductListMixin which contains 
    Active product, Pagination and Ordering Tests.
    
    """
    @classmethod
    def setUpTestData(cls):
        # Initializing Categories and Products

        cls.category = Category.objects.create(
            name="tech",
            slug="tech"
        )
        # Active product to be displayed
        cls.active_product = Product.objects.create(
            category_id=cls.category.pk,
            title="pc",
            slug="pc",
            price="2000",
            main_image="pc",
            stock_quantity=3,
        )
        # Inactive product that should not be displayed
        cls.inactive_product = Product.objects.create(
            category_id=cls.category.pk,
            title="pc 2",
            slug="pc 2",
            price="40000",
            main_image="pc",
            stock_quantity=10,
            is_active=False,
        )
        # View url
        cls.url = reverse("products:list")
        
       # Another active product for use in product sorting
        Product.objects.create(
            category_id=cls.category.pk,
            title="new",
            slug="mew",
            price="1000",
            main_image="new",
            stock_quantity=7,
        )
        
        
         
        

        