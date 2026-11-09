from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

user_model = get_user_model()
postal_code_validator = RegexValidator(
    regex=r"^\d{10}$",
    message="Postal code must contain exactly 10 digits."
)


class Address(models.Model):
    """
    Address model, details about user addresses
    """
    user = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name="addresses"
    )
    
    title = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10, validators=[postal_code_validator])
    full_address = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.phone_number} - {self.title}"
    
    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ("-created",)