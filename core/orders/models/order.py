from django.db import models
from django.contrib.auth import get_user_model
from accounts.models.address import postal_code_validator
import uuid

user = get_user_model()


class Order(models.Model):
    
    class Status(models.TextChoices):
        """
        A TextChoise class for order status
        """
        PLACED = "placed", "Placed"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELED = "cancelled", "Cancelled"


    user = models.ForeignKey(
        user,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    address = models.ForeignKey(
        "accounts.Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # General order code
    order_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    
    # َ User information at the time of placing an order
    full_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=13)
    
    # Address snapshot
    shipping_province = models.CharField(max_length=100)
    shipping_city = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=10, validators=[postal_code_validator])
    shipping_full_address = models.TextField()
    
    # Order status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLACED
    )
    
    # Order amounts
    # Formula, total = subtotal - discount_amount + shipping_cost
    subtotal = models.DecimalField(max_digits=12, decimal_places=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=0)
    total = models.DecimalField(max_digits=12, decimal_places=0)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)