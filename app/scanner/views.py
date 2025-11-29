from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkerCreateSerializer
from .utils import generate_qr_base64
from .models import Worker
from rest_framework import generics

from drf_spectacular.utils import extend_schema

def scan_view(request):
    return render(request, "scanner/scan.html")


@extend_schema(
    summary="Worker üçün QR code yarat",
    description="Full name göndər → base64 QR code yaradır"
)
class GenerateQRAPIView(APIView):
    def post(self, request):
        full_name = request.data.get("full_name")

        if not full_name:
            return Response({"detail": "full_name tələb olunur."}, status=400)

        qr_code = generate_qr_base64(full_name)

        worker = Worker.objects.create(full_name=full_name, qr_code=qr_code)

        return Response({
            "id": worker.id,
            "full_name": worker.full_name,
            "qr_code": worker.qr_code
        }, status=201)


class WorkerListAPIView(generics.ListAPIView):
    queryset = Worker.objects.all().order_by("-id")
    serializer_class = WorkerCreateSerializer