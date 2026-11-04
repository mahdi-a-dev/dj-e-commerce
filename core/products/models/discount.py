from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CheckConstraint, Q, F
from django.utils import timezone
from django.core.exceptions import ValidationError


class Discount(models.Model):
    """
    Represent a discount model for product model.
    """
    name = models.CharField(max_length=100)
    
    # discount percentage
    percentage = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100)
        ]
    )
    
    start_date = models.DateField(validators=[MinValueValidator(timezone.localdate)])
    end_date = models.DateField()
    
    is_active = models.BooleanField(default=True)
    
    @property
    def is_valid(self):
        """
        Is discount valid.
        The discount must be active and not have expired.
        """
        now = timezone.localdate()
        
        return (
            self.is_active
            and self.start_date <= now
            and self.end_date > now
        )

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError({
                'end_date': 'End date must be after start date.'
            })
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Discounts"
        
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