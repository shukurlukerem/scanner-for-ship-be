from django.contrib import admin
from .models import ScanLog
from django.utils.html import format_html
from .models import Worker

@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ("code", "scanned_at")


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "qr_preview", "created_at")
    readonly_fields = ("qr_image_large",)
    search_fields = ("full_name",)

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="60" height="60" style="border:1px solid #ccc; border-radius:4px;"/>',
                obj.qr_code
            )
        return "-"
    qr_preview.short_description = "QR Kod"

    def qr_image_large(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" width="200" style="border:1px solid #ccc;"/>',
                obj.qr_code
            )
        return "QR code mövcud deyil."
    qr_image_large.short_description = "QR Kod (Böyük)"