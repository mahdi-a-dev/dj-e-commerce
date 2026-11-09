from django.contrib import admin
from cart.models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "updated")
    search_fields = ("user",)
    raw_id_fields = ("user",)
    date_hierarchy = "created"
    ordering = ("-created",)
    

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")
    
