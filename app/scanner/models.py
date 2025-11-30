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

from django.contrib.auth.hashers import make_password, check_password


class ScannerUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_pass):
        self.password = make_password(raw_pass)

    def check_password(self, raw_pass):
        return check_password(raw_pass, self.password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.username
