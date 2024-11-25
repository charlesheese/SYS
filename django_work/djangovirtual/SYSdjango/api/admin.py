from django.contrib import admin
from .models import Product, User  # Ensure this imports only your custom models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Product Admin configuration
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productID', 'title', 'seller', 'price', 'created_at', 'is_sold')  # Corrected fields
    list_filter = ('is_sold', 'created_at')  # Corrected fields


# User Admin configuration
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


# Register models with their admin classes
admin.site.register(Product, ProductAdmin)

try:
    admin.site.unregister(User)  # Avoid duplicate registration if already registered
except admin.sites.NotRegistered:
    pass

admin.site.register(User, UserAdmin)

