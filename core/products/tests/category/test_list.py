from django.test import TestCase
from products.models import Product, Category
from django.urls import reverse
from products.tests.mixins.product_mixin import ProductListTestMixin


class CategoryListTests(ProductListTestMixin, TestCase):
    """
    Test CategoryList view.
    
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
        
       # Another active product for use in product sorting
        Product.objects.create(
            category_id=cls.category.pk,
            title="new",
            slug="mew",
            price="1000",
            main_image="new",
            stock_quantity=6,
        )
        
        # View url
        cls.url = reverse(
            "products:category-list",
            kwargs={
                "slug": cls.category.slug
            }
        )

        # another category
        category = Category.objects.create(
            name="other-category",
            slug="other-category"
        )
        
        # product with this category
        cls.product = Product.objects.create(
            category_id=category.pk,
            title="other",
            slug="mew",
            price="10000",
            main_image="new",
            stock_quantity=6,
        )
        
    
    def test_filters_products_by_category(self):
        """
        Category list shows only products fron requested category.
        """
        response = self.client.get(
            self.url,
        )
                
        self.assertNotContains(response, self.product)
        
        