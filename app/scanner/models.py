from django.db import models

class ScanLog(models.Model):
    code = models.CharField(max_length=255)
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class Worker(models.Model):
    full_name = models.CharField(max_length=255)
    qr_code = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name