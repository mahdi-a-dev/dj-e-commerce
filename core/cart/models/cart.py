from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        user,
        on_delete=models.CASCADE,
        related_name="cart"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
