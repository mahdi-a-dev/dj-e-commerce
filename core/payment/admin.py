from django.contrib import admin
from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "amount", "status", "created", "updated")
    search_fields = ("order",)
    raw_id_fields = ("order",)
    date_hierarchy = "created"
    ordering = ("-created",)
    