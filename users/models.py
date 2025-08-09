from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        WAREHOUSE_MANAGER = 'warehouse_manager', 'Warehouse Manager'
        DELIVERY_MANAGER = 'delivery_manager', 'Delivery Manager'
        DRIVER = 'driver'
        CLIENT = 'client'

    username = None
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CLIENT)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or self.phone_number or ""


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profiles/')
    address = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else str(self.user) or ""