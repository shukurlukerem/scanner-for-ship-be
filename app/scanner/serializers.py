from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import Worker, ScannerLog
from rest_framework import serializers

class WorkerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ["id", "full_name", "qr_code"]
        read_only_fields = ["qr_code"]


class ScannerLogSerializer(serializers.ModelSerializer):
    worker = serializers.StringRelatedField()

    class Meta:
        model = ScannerLog
        fields = ["id", "worker", "scan_type", "scanned_at"]

class WorkerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ["id", "full_name", "qr_code", "created_at"]

class ScannerLogListSerializer(serializers.ModelSerializer):
    worker_name = serializers.CharField(source="worker.full_name", read_only=True)
    time = serializers.SerializerMethodField()

    class Meta:
        model = ScannerLog
        fields = ["id", "worker_name", "scan_type", "scanned_at", "time"]

    def get_time(self, obj):
        return obj.scanned_at.strftime("%H:%M:%S")