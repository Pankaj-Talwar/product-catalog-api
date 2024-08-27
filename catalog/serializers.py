from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'inventory_count', 'category', 'sales_count']  # Add sales_count here

class InventoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['inventory_count']