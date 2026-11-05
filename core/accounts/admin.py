from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, Profile, Address


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = ("phone_number", "is_staff", "is_active", "is_superuser")
    list_filter = ("phone_number", "is_staff", "is_active", "is_superuser")
    fieldsets = (
        ("Authentication", {"fields": ("phone_number", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser",)}),
        ("Group permissions", {"fields": ("groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),

    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number", "password1", "password2", "is_staff",
                "is_active", "is_superuser",
            )}
        ),
    )

    search_fields = ("phone_number",)
    ordering = ("phone_number",)
    list_editable = ("is_staff", "is_active", "is_superuser")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "email")
    search_fields = ("user__phone_number",)
    raw_id_fields = ("user",)
    date_hierarchy = "created"


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "province", "city", "postal_code")
    search_fields = ("user__phone_number",)
    raw_id_fields = ("user",)
    date_hierarchy = "created"
