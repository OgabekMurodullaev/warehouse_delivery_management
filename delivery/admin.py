from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import DeliveryVehicle, Delivery, DeliveryLog


@admin.register(DeliveryVehicle)
class DeliveryVehicleAdmin(ModelAdmin):
    list_display = ("vehicle_number", "vehicle_type", "capacity_kg", "is_available")
    list_filter = ("vehicle_type", "is_available")
    search_fields = ("vehicle_number", "vehicle_type")
    ordering = ("vehicle_number",)


class DeliveryLogInline(admin.TabularInline):
    model = DeliveryLog
    extra = 1
    readonly_fields = ("timestamp",)


@admin.register(Delivery)
class DeliveryAdmin(ModelAdmin):
    list_display = (
        "id", "order", "source_warehouse", "destination_address",
        "vehicle", "driver", "status", "estimated_delivery_date", "actual_delivery_date", "created_at"
    )
    list_filter = ("status", "source_warehouse", "created_at")
    search_fields = ("order__id", "destination_address", "driver__username", "vehicle__vehicle_number")
    ordering = ("-created_at",)
    autocomplete_fields = ("order", "source_warehouse", "vehicle", "driver")
    inlines = [DeliveryLogInline]
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Delivery Info", {
            "fields": ("order", "source_warehouse", "destination_address")
        }),
        ("Transport", {
            "fields": ("vehicle", "driver")
        }),
        ("Status & Dates", {
            "fields": ("status", "estimated_delivery_date", "actual_delivery_date")
        }),
        ("System Info", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )


@admin.register(DeliveryLog)
class DeliveryLogAdmin(ModelAdmin):
    list_display = ("delivery", "status", "note", "timestamp")
    list_filter = ("status", "timestamp")
    search_fields = ("delivery__id", "note")
    autocomplete_fields = ("delivery",)
    readonly_fields = ("timestamp",)
