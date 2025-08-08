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
