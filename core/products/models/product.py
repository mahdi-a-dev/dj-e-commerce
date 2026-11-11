from django.db import models
from django.urls import reverse
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import CheckConstraint, Q
from django.core.validators import MinValueValidator

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
    LOW_STOCK_THRESHOLD = 5
    
    title = models.CharField(max_length=255, verbose_name="عنوان")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="اسلاگ")
    
    main_image = models.ImageField(upload_to="products/main/", verbose_name="تصویر اصلی")
    
    # product category
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="دسته بندی"
    )
    
    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name="قیمت"
    )
    # product discount
    discount = models.ForeignKey(
        "Discount",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        verbose_name="تخفیف"
        
    )
    
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="تعداد موجودی")
    is_active = models.BooleanField(default=True, verbose_name="فعال بودن")
    
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    
    # default manager
    objects = models.Manager()
    # cuscomize manager
    active = ProductManager()
    
    def __str__(self):
        return self.title
    
    @property
    def is_in_stock(self):
        """
        The availability of a product
        """
        return self.stock_quantity > 0

    @property
    def is_low_stock(self):
        """
        Checking for low stock of a product
        """
        return 0 < self.stock_quantity <= self.LOW_STOCK_THRESHOLD
    
    @property
    def discount_price(self):
        """
        Calculate price after discount.
        """
        discount = self.discount
        
        if not discount or not discount.is_valid:
            return None
        
        discount_rate = discount.percentage / Decimal("100")
        
        return (
            self.price * (Decimal("1") - discount_rate) 
        ).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP
        )
    
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


    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
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
        related_name="gallery_images",
        verbose_name="محصول"
    )
    image = models.ImageField(
        upload_to="products/gallery/",
        verbose_name="تصویر"
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="متن جایگزین"
    )
    
    def __str__(self):
        return self.alt_text
    
    
    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "گالری محصولات"
        