# app/urls.py
from django.urls import path
from .views import GenerateQRAPIView, WorkerListAPIView

urlpatterns = [
    path("generate-qr/", GenerateQRAPIView.as_view(), name="generate-qr"),
    path("workers/", WorkerListAPIView.as_view(), name="worker-list"),
]
