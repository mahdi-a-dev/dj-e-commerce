from django.test import TestCase
from django.urls import reverse
from ...models import Product, Category, Discount
from django.db import IntegrityError, transaction
from django.utils import timezone
from datetime import timedelta


class TestDiscountModel(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='django', slug='django')
        self.data1 = Product.objects.create(category_id=self.category.pk, title='django beginners',
                                            slug='django-beginners', price='20', main_image='django')
        self.data2 = Product.products.create(category_id=self.category.pk, title='django advanced',
                                             slug='django-advanced', price='20', main_image='django', is_active=False)
        
        self.data = Discount.objects.create(name="Discount", percentage=50, start_date=timezone.now(),
                                            end_date=timezone.now() + timedelta(days=10))

    def test_discount_model_entry(self):
        """
        Test discount model data insertion/types/field attributes
        """
        data = self.data
        self.assertTrue(isinstance(data, Discount))
        self.assertEqual(str(data), 'Discount')
    
    def test_percentage_must_be_between_1_and_100(self):
        """
        Test Discount fails to save when percenttage is not between 1 and 100
        """
        # little than 1
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Discount.objects.create(name="discount1", percentage=0, start_date=timezone.localdate(),
                    end_date=timezone.now() + timedelta(days=10))
                
        # greatter then 100
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Discount.objects.create(name="discount1", percentage=101, start_date=timezone.localdate(),
                    end_date=timezone.now() + timedelta(days=10))
    
    def test_start_date_must_be_little_than_end_date(self):
        """
        Test Discount fails to save when start_date is not little than end_date
        """
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Discount.objects.create(name="discount", percentage=50, start_date=timezone.localdate(),
                    end_date=timezone.localdate() - timedelta(days=1))


        