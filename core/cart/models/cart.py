from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="کاربر"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    def __str__(self):
        return f"Cart - ({self.user.phone_number.as_national})"
    
    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"