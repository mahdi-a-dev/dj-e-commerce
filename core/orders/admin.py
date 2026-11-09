from django.contrib import admin
from orders.models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "full_name", "phone_number", "status")
    search_fields = ("user",)
    raw_id_fields = ("user",)
    date_hierarchy = "created"
    ordering = ("-created",)
    

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity")
    
