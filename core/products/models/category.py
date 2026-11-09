from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Represent a category model for product model.
    """
    
    # categories can have subcategory
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="subcategory",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name, allow_unicode=True)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("products:category-list", args=[self.slug])
    
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ("-parent__id",)