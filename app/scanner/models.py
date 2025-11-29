from django.utils import timezone
from django.db import models

class Worker(models.Model):
    full_name = models.CharField(max_length=255)
    qr_code = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
    


class ScannerLog(models.Model):
    SCAN_TYPES = (
        ("entry", "Giriş"),
        ("exit", "Çıxış"),
    )

    worker = models.ForeignKey(
        "Worker",
        on_delete=models.CASCADE,
        related_name="logs"
    )

    scan_type = models.CharField(max_length=10, choices=SCAN_TYPES)
    scanned_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.worker.full_name} - {self.scan_type} - {self.scanned_at}"