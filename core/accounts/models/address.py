from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from common.models.time_stamps import TimeStampeModel

user_model = get_user_model()
postal_code_validator = RegexValidator(
    regex=r"^\d{10}$",
    message="کد پستی باید دقیقاً شامل ۱۰ رقم باشد.")


class AddressManager(models.Manager):
    def get_user_addresses(self, user):
        return self.filter(user=user)
    
    
class Address(TimeStampeModel):
    """
    Address model, details about user addresses
    """
    user = models.ForeignKey(
        user_model,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name="کاربر"
    )
    
    title = models.CharField(max_length=100, verbose_name="عنوان")
    province = models.CharField(max_length=100, verbose_name="استان")
    city = models.CharField(max_length=100, verbose_name="شهر")
    postal_code = models.CharField(
        max_length=10,
        validators=[postal_code_validator],
        verbose_name="آدرس پستی"
    )
    full_address = models.TextField(max_length=500, verbose_name="آدرس کامل")
        
    objects = AddressManager()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"
        ordering = ("-created",)