from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_qr_base64
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from datetime import timedelta

from .serializers import WorkerCreateSerializer, WorkerListSerializer
from .pagination import DefaultPagination
from .models import Worker, ScannerLog

def scan_view(request):
    return render(request, "scanner/scan.html")


@extend_schema(
    request=WorkerCreateSerializer,
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



class TodayLogsAPIView(APIView):
    def get(self, request):
        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        logs = ScannerLog.objects.filter(
            scanned_at__gte=start_of_day,
            scanned_at__lt=end_of_day
        ).select_related("worker").order_by("-scanned_at")

        data = [
            {
                "worker_name": log.worker.full_name,
                "scan_type": log.scan_type,
                "time": log.scanned_at
            }
            for log in logs
        ]
        return Response({"logs": data})



class ScanAPIView(APIView):

    def post(self, request):
        qr = request.data.get("qr_code")

        if not qr:
            return Response({"detail": "QR kod göndərilməyib"}, status=400)
        worker = Worker.objects.filter(qr_code=qr).first()

        if not worker:
            return Response({"detail": "Bu QR kod üzrə işçi tapılmadı"}, status=404)

        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        today_logs = ScannerLog.objects.filter(
            worker=worker,
            scanned_at__gte=start_of_day,
            scanned_at__lt=end_of_day
        ).order_by("scanned_at")

        count = today_logs.count()

        if count >= 2:
            return Response(
                {"detail": "Bu işçi bu gün artıq 2 dəfə scan olunub"},
                status=403
            )

        if count == 0:
            log = ScannerLog.objects.create(worker=worker, scan_type="entry")
            return Response({
                "worker": worker.full_name,
                "scan_type": "entry",
                "detail": "Giriş qeydə alındı"
            })

        if count == 1:
            log = ScannerLog.objects.create(worker=worker, scan_type="exit")
            return Response({
                "worker": worker.full_name,
                "scan_type": "exit",
                "detail": "Çıxış qeydə alındı"
            })
        
class WorkerListAPIView(generics.ListAPIView):
    queryset = Worker.objects.all().order_by("-id")
    serializer_class = WorkerListSerializer
    pagination_class = DefaultPagination