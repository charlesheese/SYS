from django.contrib import admin
from .models import Product, User

# Product Admin configuration
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productID', 'title', 'price', 'is_sold', 'sellerID', 'createdAtProduct')
    list_filter = ('is_sold', 'createdAtProduct')  # Adds filter options for 'is_sold' and 'createdAtProduct'
    search_fields = ('title', 'sellerID')  # Allows search by 'title' and 'sellerID'

# User Admin configuration
class UserAdmin(admin.ModelAdmin):
    list_display = ('userID', 'username', 'email', 'createdAt')  # Columns to show in list view
    search_fields = ('username', 'email')  # Allows search by 'username' and 'email'

# Register models with their custom admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)

