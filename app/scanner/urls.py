# app/urls.py
from django.urls import path
from .views import GenerateQRAPIView,ScanAPIView, TodayLogsAPIView

urlpatterns = [
    path("generate-qr/", GenerateQRAPIView.as_view(), name="generate-qr"),
    path("scan/", ScanAPIView.as_view(), name="scan-qr"),
    path("today-logs/", TodayLogsAPIView.as_view(), name="today-logs"),
]
