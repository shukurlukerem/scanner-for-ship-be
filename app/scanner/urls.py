# app/urls.py
from django.urls import path
from .views import (GenerateQRAPIView,
                    ScanAPIView, 
                    TodayLogsAPIView,
                    WorkerListAPIView, 
                    ScannedUsersListAPIView,
                    ExportTodayExcelAPIView,
                    LoginAPIView,
                    WorkerDeleteAPIView)

urlpatterns = [
    path("generate-qr/", GenerateQRAPIView.as_view(), name="generate-qr"),
    path("scan/", ScanAPIView.as_view(), name="scan-qr"),
    path("today-logs/", TodayLogsAPIView.as_view(), name="today-logs"),
    path("workers/", WorkerListAPIView.as_view(), name="worker-list"),
    path("scanned-users/", ScannedUsersListAPIView.as_view(), name="scanned-users"),
    path("export-excel/", ExportTodayExcelAPIView.as_view(), name="export-excel"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("workers/<int:id>/", WorkerDeleteAPIView.as_view(), name="worker-delete"),

]
