from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CheckConstraint, Q, F
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ValidationError


class Category(models.Model):
    """
    Represent a category model for product model.
    """
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse("products:category-list", args=[self.slug])

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name, allow_unicode=True)
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "categories"


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
    

class ProductManager(models.Manager):
    """
    Custome manager for product model.
    """
    def get_queryset(self):
        """
        Filter products by is_active filed.
        """
        return super().get_queryset().filter(is_active=True)
    

class Product(models.Model):
    """
    Represent product model.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    
    main_image = models.ImageField(upload_to="products/main/")
    
    # product category
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(0)]
    )
    # product discount
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    
    is_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # default manager
    objects = models.Manager()
    # cuscomize manager
    products = ProductManager()
    
    @property
    def discount_price(self):
        """
        Calculate price after discount.
        """
        discount = self.discount
        
        if not discount or not discount.is_valid:
            return None
        
        percentage = discount.percentage

        return self.price * (Decimal("1") - percentage / Decimal("100"))
    
    @property
    def final_price(self):
        """
        To get final price after discount or haven't discount.
        """
        discount = self.discount_price
        
        if discount is not None:
            return discount
        
        return self.price
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title, allow_unicode=True)
        
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("products:product-detail", args=[self.slug])
    

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Products"
        ordering = ("-created",)
        
        # Price Validation for database level
        constraints = [
            CheckConstraint(
                condition=Q(price__gte=0),
                name="product_price_non_negative"
            )
        ]


class ProductImage(models.Model):
    """
    Represent Product images model for product model.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery_images"
    )
    image = models.ImageField(
        upload_to="products/gallery/"
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True
    )
    
    def __str__(self):
        return self.alt_text
    
    class Meta:
        verbose_name_plural = "Product Images"
        