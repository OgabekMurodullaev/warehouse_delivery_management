from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin  # unfold dan foydalanamiz
from django.utils.html import format_html
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ('id', 'email', 'phone_number', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_active', 'date_joined')
    search_fields = ('email', 'phone_number')
    ordering = ('-date_joined',)
    list_editable = ('is_verified', 'is_active')

    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            'fields': ('email', 'phone_number', 'password', 'role', 'is_verified')
        }),
        ("Ruxsatlar", {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ("Tizim ma'lumotlari", {
            'fields': ('last_login', 'date_joined')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'profile_image_preview')
    search_fields = ('first_name', 'last_name', 'user__email', 'user__phone_number')

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="40" style="border-radius:50%;" />', obj.profile_image.url)
        return "-"
    profile_image_preview.short_description = "Rasm"

    fieldsets = (
        ("Asosiy ma'lumotlar", {
            'fields': ('user', 'first_name', 'last_name', 'date_of_birth')
        }),
        ("Qo‘shimcha ma'lumotlar", {
            'fields': ('address', 'profile_image')
        }),
    )
