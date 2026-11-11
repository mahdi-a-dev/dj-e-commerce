from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import CheckConstraint, Q, F
from django.core.validators import MinValueValidator, MaxValueValidator


class Discount(models.Model):
    """
    Represent a discount model for product model.
    """
    name = models.CharField(max_length=100, verbose_name="نام")
    
    percentage = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ],
        verbose_name="درصد"
    )
    
    start_date = models.DateField(
        validators=[MinValueValidator(timezone.localdate)],
        verbose_name="تاریخ شروع"
    )
    end_date = models.DateField(verbose_name="تاریخ پایان")
    
    is_active = models.BooleanField(default=True, verbose_name="فعال بودن")
    
    def __str__(self):
        return self.name
    
    @property
    def is_valid(self):
        """
        The discount must be active and not have expired.
        """
        now = timezone.localdate()
        
        return (
            self.is_active
            and self.start_date <= now
            and self.end_date > now
        )

    def clean(self):
        # Check end_date be after start_date
        if self.start_date >= self.end_date:
            raise ValidationError({
                'end_date': 'End date must be after start date.'
            })
    
    
    class Meta:
        verbose_name = "تخفیف"
        verbose_name_plural = "تخفیف ها"
        
        # percentage validation for database level
        constraints = [
            CheckConstraint(
                condition=Q(percentage__gt=0) & Q(percentage__lte=100),
                name="discount_percentage_between_1_and_100"
            ),
            CheckConstraint(
                condition=Q(end_date__gt=F("start_date")),
                name="discount_end_after_start"
            )
        ]