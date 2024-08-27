from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'inventory_count', 'category', 'sales_count']
    
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_inventory_count(self, value):
        if value < 0:
            raise serializers.ValidationError("Inventory count cannot be negative.")
        return value

class InventoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['inventory_count']
    
    def validate_inventory_count(self, value):
        if value < 0:
            raise serializers.ValidationError("Inventory count cannot be negative.")
        return value
