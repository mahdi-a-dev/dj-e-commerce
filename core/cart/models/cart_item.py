from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class CartItem(models.Model):
    cart = models.ForeignKey(
        "Cart",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سبد خرید"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        verbose_name="محصول"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="مقدار")

    def __str__(self):
        return f"{self.product.title} - {self.cart.user.phone_number.as_national}"
    
    
    class Meta:
        verbose_name = "قلم سبد خرید"
        verbose_name_plural = "اقلام سبد خرید"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart"
            )
        ]