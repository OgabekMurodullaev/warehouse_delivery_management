from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Warehouse, Stock, StockHistory


@admin.register(Warehouse)
class WarehouseAdmin(ModelAdmin):
    list_display = ("name", "location", "capacity", "unit")
    list_filter = ("unit",)
    search_fields = ("name", "location")
    ordering = ("name",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "location")
        }),
        ("Capacity Details", {
            "fields": ("capacity", "unit"),
            "description": "Specify the maximum capacity and its measurement unit."
        }),
    )


@admin.register(Stock)
class StockAdmin(ModelAdmin):
    list_display = ("product", "warehouse", "quantity", "unit", "last_updated")
    list_filter = ("warehouse", "unit")
    search_fields = ("product__name", "warehouse__name")
    ordering = ("-last_updated",)
    autocomplete_fields = ("product", "warehouse")

    fieldsets = (
        ("Stock Info", {
            "fields": ("product", "warehouse", "quantity", "unit")
        }),
        ("Timestamps", {
            "fields": ("last_updated",),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ("last_updated",)


@admin.register(StockHistory)
class StockHistoryAdmin(ModelAdmin):
    list_display = ("stock", "change_amount", "changed_by", "change_type", "timestamp")
    list_filter = ("changed_by", "change_type")
    readonly_fields = ("timestamp", )
