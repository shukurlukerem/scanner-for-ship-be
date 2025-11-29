# app/serializers.py
from rest_framework import serializers
from .models import Worker

class WorkerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ["id", "full_name", "qr_code"]
        read_only_fields = ["qr_code"]


class WorkerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ["id", "full_name", "qr_code"]
