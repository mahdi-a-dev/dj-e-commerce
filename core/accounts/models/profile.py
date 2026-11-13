from django.db import models
from django.contrib.auth import get_user_model
from common.models.time_stamps import TimeStampeModel

user_model = get_user_model()

class Profile(TimeStampeModel):
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
        
    def __str__(self):
        return f"{self.user.phone_number} - {self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "پروفایل‌"
        verbose_name_plural = "پروفایل‌ها"
        ordering = ("-created",)