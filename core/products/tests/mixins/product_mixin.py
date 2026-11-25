from products.models import Product


class ActiveProductTestMixin:
    
    def test_only_active_products(self):
        """
        Test only active product are displayed.
        """
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, 200)
            
        self.assertContains(response, self.active_product.title)
        self.assertNotContains(response, self.inactive_product.title) 


class ProductListTestMixin(ActiveProductTestMixin):
     
    def test_pagination(self):
        """
        Test productList view is paginate by 20 products.
        """
        for i in range(22):
            Product.objects.create(
            category_id=self.category.pk,
            slug=f"django-{i}",
            title=f"django-{i}",
            price="20",
            main_image="django",
            stock_quantity=3,
        )
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(response.context["is_paginated"])
        
        page_obj = response.context["page_obj"]
        self.assertEqual(len(page_obj.object_list), 20)
    
    def test_search(self):
        """
        Test productlist search returns the match title.
        """
        response = self.client.get(
            self.url,
            {"q": "pc"}
        )
        self.assertEqual(response.status_code, 200)
        
        products = response.context["products"]

        self.assertIn(self.active_product, products)
        self.assertNotIn(self.inactive_product, products)
            
    def test_ordering_by_price_ascending(self):
        """
        Test productlist sorted by price_asc
        """
        response = self.client.get(
            self.url,
            {"ordering": "price_asc"}
        )
        
        self.assertEqual(response.status_code, 200)

        products = list(response.context["products"])
        
        self.assertEqual(
            [p.price for p in products],
            sorted([p.price for p in products])
        )
    
    def test_ordering_by_price_descending(self):
        """
        Test productlist sorted by price_desc
        """
        response = self.client.get(
            self.url,
            {"ordering": "price_desc"}
        )
        
        self.assertEqual(response.status_code, 200)

        products = list(response.context["products"])
        
        self.assertEqual(
            [p.price for p in products],
            sorted([p.price for p in products], reverse=True)
        )