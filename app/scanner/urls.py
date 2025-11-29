# app/urls.py
from django.urls import path
from .views import GenerateQRAPIView

urlpatterns = [
    path("generate-qr/", GenerateQRAPIView.as_view(), name="generate-qr"),
]
