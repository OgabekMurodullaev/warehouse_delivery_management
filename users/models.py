import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


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


class VerificationCode(models.Model):
    class Methods(models.TextChoices):
        EMAIL = 'email', 'Email'
        PHONE = 'phone', 'Phone'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verification_codes', null=True, blank=True)
    target = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=Methods.choices)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    max_attempts = models.PositiveSmallIntegerField(default=5)
    is_used = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return f"Verification code for user {self.user}"

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def can_attempts(self):
        return self.attempts < self.max_attempts and not self.is_expired() and not self.is_used

    def mark_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])