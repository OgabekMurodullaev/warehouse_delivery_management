from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ProductCategory, Product


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "slug", "description")
    ordering = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "description")
        }),
        ("Status", {
            "fields": ("is_active",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("name", "category", "price", "unit", "sku", "is_active", "created_at")
    list_filter = ("category", "unit", "is_active", "created_at")
    search_fields = ("name", "description", "sku")
    ordering = ("name",)
    autocomplete_fields = ("category",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "category", "description", "image")
        }),
        ("Pricing & Stock", {
            "fields": ("price", "unit", "sku")
        }),
        ("Status", {
            "fields": ("is_active",),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    readonly_fields = ("created_at", "updated_at")

