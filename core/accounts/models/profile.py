from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

user_model = get_user_model()

class Profile(models.Model):
    """
    Profile model contains user personal details
    """
    user = models.OneToOneField(
        user_model,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="کاربر"
    )
    
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")
    
    email = models.EmailField(
        max_length=200,
        unique=True,
        null=True,
        verbose_name="ایمیل"
    )
    
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    def __str__(self):
        return f"{self.user.phone_number} - {self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "پروفایل‌"
        verbose_name_plural = "پروفایل‌ها"
        ordering = ("-created",)