from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, help_text="Name of the product")
    description = models.TextField(help_text="Description of the product")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product")
    inventory_count = models.IntegerField(help_text="Number of items available in inventory")
    category = models.CharField(max_length=100, help_text="Category of the product")
    sales_count = models.PositiveIntegerField(default=0, help_text="Number of items sold")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-sales_count']  # Default ordering by sales_count descending
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['sales_count']),
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"
