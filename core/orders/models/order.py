from django.db import models
from django.contrib.auth import get_user_model
from common.models.time_stamps import TimeStampeModel
from accounts.models.address import postal_code_validator
import uuid

user = get_user_model()


class Order(TimeStampeModel):
    
    class Status(models.TextChoices):
        """
        A TextChoise class for order status
        """
        PLACED = "placed", "ثبت شده"
        PROCESSING = "processing", "در حال پردازش"
        SHIPPED = "shipped", "ارسال شده"
        DELIVERED = "delivered", "تحویل شده"
        CANCELED = "cancelled", "لغو شده"


    user = models.ForeignKey(
        user,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="کاربر"
    )
    address = models.ForeignKey(
        "accounts.Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="آدرس"
    )
    
    # General order code
    order_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    
    # َ User information at the time of placing an order
    full_name = models.CharField(max_length=250, verbose_name="نام و نام خانوادگی")
    phone_number = models.CharField(max_length=13, verbose_name="شماره موبایل")
    
    # Address snapshot
    shipping_province = models.CharField(max_length=100, verbose_name="استان مقصد")
    shipping_city = models.CharField(max_length=100, verbose_name="شهر مقصد")
    shipping_postal_code = models.CharField(
        max_length=10,
        validators=[postal_code_validator],
        verbose_name="آدرس پستی مقصد"
    )
    shipping_full_address = models.TextField(verbose_name="آدرس کامل مقصد")
    
    # Order status
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLACED,
        verbose_name="وضعیت سفارش"
    )
    
    # Order amounts
    # Formula, total = subtotal - discount_amount + shipping_cost
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="جمع مبلغ اقلام"
    )
    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="مبلغ تخفیف"
    )
    shipping_cost = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="هزینه ارسال"
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="مبلغ قابل پرداخت"
    )
        
    
    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"