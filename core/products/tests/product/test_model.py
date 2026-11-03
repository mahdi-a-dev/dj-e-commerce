from django.test import TestCase
from django.urls import reverse
from ...models import Product, Category
from django.db import IntegrityError, transaction


class TestProductModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='django', slug='django')
        self.data1 = Product.objects.create(category_id=self.category.pk, title='django beginners',
                                            slug='django-beginners', price='20', main_image='django')
        self.data2 = Product.products.create(category_id=self.category.pk, title='django advanced',
                                             slug='django-advanced', price='20', main_image='django', is_active=False)

    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')

    def test_products_url(self):
        """
        Test product model slug and URL reverse
        """
        data = self.data1
        url = reverse('products:product-detail', args=[data.pk, data.slug])
        self.assertEqual(url, f'/{data.pk}/{data.slug}/')
        response = self.client.get(
            reverse('products:product-detail', args=[data.pk, data.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_products_custom_manager (self):
        """
        Test product model custom manager returns only active products
        """
        data = Product.products.all()
        self.assertEqual(data.count(), 1)
    
    def test_price_cannot_be_negative(self):
        """
        Test product fails to save when price is negative
        """
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Product.objects.create(category_id=self.category.pk, title='django',
                    slug='django', price='-1', main_image='django')
        
        