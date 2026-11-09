from django.contrib import admin
from .models import Product, ProductImage, Category, Discount


class ProductImageInline(admin.TabularInline):
    """
    Inline of product image model to product model.
    """
    model = ProductImage
    extra = 1
    max_num = 10

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    search_fields = ("name", "slug")
    raw_id_fields = ("parent",)
    prepopulated_fields = {"slug": ("name",)}
    
    
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "percentage", "start_date", "end_date", "is_active")
    search_fields = ("name", "percentage")
    ordering = ("-start_date", "is_active")
    list_editable = ("is_active",)
    
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "price", "stock_quantity", "is_active", "created", "updated")
    list_filter = ("category", "is_active", "stock_quantity")
    search_fields = ("price", "title")
    raw_id_fields = ("category",)
    date_hierarchy = "created"
    list_editable = ("is_active",)
    ordering = ("-created", "-is_active",)
    prepopulated_fields = {"slug": ("title",)}
    
    # use product image inline
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image", "alt_text")
    search_fields = ("product", "alt_text")
    raw_id_fields = ("product",)
    list_editable = ("alt_text",)
    