# app/urls.py
from django.urls import path
from .views import GenerateQRAPIView,ScanAPIView, TodayLogsAPIView,WorkerListAPIView, ScannedUsersListAPIView

urlpatterns = [
    path("generate-qr/", GenerateQRAPIView.as_view(), name="generate-qr"),
    path("scan/", ScanAPIView.as_view(), name="scan-qr"),
    path("today-logs/", TodayLogsAPIView.as_view(), name="today-logs"),
    path("workers/", WorkerListAPIView.as_view(), name="worker-list"),
    path("scanned-users/", ScannedUsersListAPIView.as_view(), name="scanned-users"),
]
