from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        WAREHOUSE_MANAGER = 'warehouse_manager', 'Warehouse Manager'
        DELIVERY_MANAGER = 'delivery_manager', 'Delivery Manager'
        DRIVER = 'driver'
        CLIENT = 'client'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CLIENT)

    def __str__(self):
        return self.username