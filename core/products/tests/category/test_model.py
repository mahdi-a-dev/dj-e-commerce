from django.test import TestCase
from django.urls import reverse

from products.models import Category


class TestCategoryModel(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="django", slug="django")

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.category
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), "django")

    def test_category_url(self):
        """
        Test category model slug and URL reverse
        """
        data = self.category
        response = self.client.get(
            reverse("products:category-list", kwargs={"slug": data.slug}))
        self.assertEqual(response.status_code, 200)
