from django.contrib import admin
from django.utils.html import format_html
from .models import Worker, ScannerLog

@admin.register(ScannerLog)
class ScannerLogAdmin(admin.ModelAdmin):
    list_display = ("worker", "scan_type", "scanned_at")
    list_filter = ("scan_type", "scanned_at")
    search_fields = ("worker__full_name", "worker__qr_code")


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
    qr_image_large.short_description = "QR Kod"


    from django.contrib import admin
from .models import ScannerUser

@admin.register(ScannerUser)
class ScannerUserAdmin(admin.ModelAdmin):
    list_display = ("username", "created_at")

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)