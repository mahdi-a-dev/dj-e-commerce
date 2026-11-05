from django.db import models
from django.contrib.auth import get_user_model

user_model = get_user_model()


class Address(models.Model):
    user = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name="addresses"
    )
    
    title = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    address = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.title}"
    
    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ("-created",)