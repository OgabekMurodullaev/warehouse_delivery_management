from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ("total_price",)
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("id", "customer", "warehouse", "status", "total_amount", "created_at", "updated_at")
    list_filter = ("status", "warehouse", "created_at")
    search_fields = ("id", "customer__username", "customer__email")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]
    autocomplete_fields = ("customer", "warehouse")
    readonly_fields = ("created_at", "updated_at", "total_amount")

    fieldsets = (
        ("Order Info", {
            "fields": ("customer", "warehouse", "status")
        }),
        ("Amounts", {
            "fields": ("total_amount",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price", "total_price")
    list_filter = ("product",)
    search_fields = ("order__id", "product__name")
    autocomplete_fields = ("order", "product")
    readonly_fields = ("total_price",)
