from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    capacity = models.DecimalField(max_length=20, decimal_places=2)
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
