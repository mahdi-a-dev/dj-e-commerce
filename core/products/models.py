from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def get_absolute_url(self):
        return reverse("products:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    products = ProductManager()

    def get_absolute_url(self):
        return reverse("products:product_detail", args=[self.slug])

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Products"
        ordering = ("-created",)



class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(
        upload_to="products/"
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True
    )
    
    def __str__(self):
        return self.alt_text
    
    class Meta:
        verbose_name_plural = "ProductImages"
    
