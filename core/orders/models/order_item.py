from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True
    )
    
    # Product snapshot
    product_title = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=12, decimal_places=0)
    
    quantity = models.PositiveIntegerField()
    discount_amount = models.DecimalField(max_digits=12, decimal_places=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=0)