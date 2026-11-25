from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product


class TestProductModel(TestCase):
    """
    Test product model.
    """
    @classmethod
    def setUpTestData(self):
        self.category = Category.objects.create(name="django", slug="django")
        self.data1 = Product.objects.create(
            category_id=self.category.pk,
            title="django beginners",
            slug="django-beginners",
            price="20",
            main_image="django",
            stock_quantity=3,
        )
        self.data2 = Product.objects.create(
            category_id=self.category.pk,
            title="django advanced",
            slug="django-advanced",
            price="20",
            main_image="django",
            stock_quantity=10,
            is_active=False,
        )

    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), "django beginners")

    def test_products_url(self):
        """
        Test product model slug and URL reverse
        """
        data = self.data1
        url = reverse("products:detail", args=[data.pk, data.slug])
        self.assertEqual(url, f"/products/{data.pk}/{data.slug}/")
        response = self.client.get(
            reverse("products:detail", args=[data.pk, data.slug])
        )
        self.assertEqual(response.status_code, 200)

    def test_price_cannot_be_negative(self):
        """
        Test product fails to save when price is negative
        """
        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.create(
                category_id=self.category.pk,
                title="django",
                slug="django",
                price="-1",
                main_image="django",
            )

    def test_is_in_stock(self):
        """
        Test is_in_stock method
        """
        product = Product.objects.create(
            category_id=self.category.pk,
            title="product",
            slug="product",
            price="20",
            main_image="django",
        )

        self.assertFalse(product.is_in_stock)
        self.assertTrue(self.data1.is_in_stock)

    def test_is_low_stock(self):
        """
        Test is_low_stock method
        """
        self.assertFalse(self.data2.is_low_stock)
        self.assertTrue(self.data1.is_low_stock)
