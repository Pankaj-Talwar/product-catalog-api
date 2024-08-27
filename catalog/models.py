from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory_count = models.IntegerField()
    category = models.CharField(max_length=100)
    sales_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
