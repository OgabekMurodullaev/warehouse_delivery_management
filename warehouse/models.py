from django.conf import settings
from django.db import models

from products.models import Product


class Warehouse(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    capacity = models.DecimalField(max_digits=20, decimal_places=2)
    unit = models.CharField(max_length=2, choices=[
        ('kg', 'Kilograms'),
        ('t', 'Tons'),
        ('l', 'litters'),
        ('m3', 'Cubic Meters'),
    ])

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_items')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_items')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=10, choices=Product.UnitChoices.choices)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('product', 'warehouse')

    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.unit} in {self.warehouse.name}"


class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='history')
    change_amount = models.DecimalField(max_digits=10, decimal_places=2)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    change_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.stock} - {self.change_amount} ({self.change_type})"
