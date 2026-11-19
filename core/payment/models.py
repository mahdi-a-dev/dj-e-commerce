from django.db import models
from common.models.time_stamps import TimeStampeModel


class Payment(TimeStampeModel):
    class Status(models.TextChoices):
        """
        A TextChoise class for payment status
        """
        PENDING = "pending", "در انتطار پرداخت"
        SUCCESS = "success", "موفق"
        FAILED = "failed", "ناموفق"
        CANCELED = "canceled", "لغو شده"
        
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="پرداخت ها"
    )
    
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="مبلغ پرداخت"
    )
    
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    class Meta(TimeStampeModel.Meta):
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت ها"
