from django.db import models


class TimeStampeModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )
    
    
    class Meta:
        abstract = True
        ordering = ("-created",)
