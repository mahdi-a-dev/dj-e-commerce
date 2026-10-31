from django.contrib import admin
from .models import Product, ProductImage, Category


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 10
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "price", "is_stock", "is_active", "created", "updated")
    list_filter = ("category", "is_active", "is_stock")
    search_fields = ("price", "title")
    raw_id_fields = ("category",)
    date_hierarchy = "created"
    list_editable = ("is_active", "is_stock")
    ordering = ("-created", "-is_active",)
    prepopulated_fields = {"slug": ("title",)}
    
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image", "alt_text")
    search_fields = ("product", "alt_text")
    raw_id_fields = ("product",)
    list_editable = ("alt_text",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")


