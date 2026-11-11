from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سفارش"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="محصول"
    )
    
    # Product snapshot
    product_title = models.CharField(max_length=255, verbose_name="عنوان محصول")
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="قیمت واحد"
    )
    
    quantity = models.PositiveIntegerField(verbose_name="مقدار")
    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="مبلغ تخفیف"
    )
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="قیمت کل"
    )
    
    
    class Meta:
        verbose_name = "قلم سفارش"
        verbose_name_plural = "اقلام سفارش"
        
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_product_per_order"
            )
        ]