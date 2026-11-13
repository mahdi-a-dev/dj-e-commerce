from django.db import models
from django.contrib.auth import get_user_model
from common.models.time_stamps import TimeStampeModel

user = get_user_model()


class Cart(TimeStampeModel):
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="کاربر"
    )

    def __str__(self):
        return f"Cart - ({self.user.phone_number.as_national})"
    
    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"