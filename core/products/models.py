from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CheckConstraint, Q


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
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Discounts"
        
        # percentage validation for database level
        constraints = [
            CheckConstraint(
                condition=Q(percentage__gt=0) & Q(percentage__lte=100),
                name="discount_percentage_must_be_between_1_and_100"
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
        