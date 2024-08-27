from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'inventory_count', 'sales_count')  # Add sales_count here
    search_fields = ('name', 'category')
    list_editable = ('sales_count',)