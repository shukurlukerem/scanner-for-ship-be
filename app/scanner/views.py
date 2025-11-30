from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_qr_base64
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from openpyxl import Workbook


from .serializers import WorkerCreateSerializer, WorkerListSerializer,ScannerLogListSerializer
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

        worker = Worker.objects.create(full_name=full_name)

        qr_text = f"WORKER_ID:{worker.id}"

        qr_code_base64 = generate_qr_base64(qr_text)

        worker.qr_code = qr_code_base64
        worker.save()

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
                "time": log.scanned_at.strftime("%H:%M:%S")
            }
            for log in logs
        ]
        return Response({"logs": data})




class ScanAPIView(APIView):
    def post(self, request):
        qr_text = request.data.get("qr_text")  

        if not qr_text:
            return Response({"detail": "QR kod göndərilməyib"}, status=400)

        if not qr_text.startswith("WORKER_ID:"):
            return Response({"detail": "QR formatı yanlışdır"}, status=400)

        worker_id = qr_text.replace("WORKER_ID:", "").strip()

        worker = Worker.objects.filter(id=worker_id).first()
        if not worker:
            return Response({"detail": "Bu işçi tapılmadı"}, status=404)

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
                "time": log.scanned_at.strftime("%H:%M:%S"),
                "detail": "Giriş qeydə alındı"
            })

        if count == 1:
            log = ScannerLog.objects.create(worker=worker, scan_type="exit")
            return Response({
                "worker": worker.full_name,
                "scan_type": "exit",
                "time": log.scanned_at.strftime("%H:%M:%S"),
                "detail": "Çıxış qeydə alındı"
            })

        
class WorkerListAPIView(generics.ListAPIView):
    queryset = Worker.objects.all().order_by("-id")
    serializer_class = WorkerListSerializer
    pagination_class = DefaultPagination


class ScannedUsersListAPIView(generics.ListAPIView):
    def get(self, request):
        logs = ScannerLog.objects.select_related("worker").order_by("scanned_at")

        grouped = {}  

        for log in logs:
            worker_id = log.worker.id
            date_str = log.scanned_at.strftime("%Y-%m-%d")

            key = f"{worker_id}_{date_str}"

            if key not in grouped:
                grouped[key] = {
                    "worker_name": log.worker.full_name,
                    "date": date_str,
                    "entry_time": None,
                    "exit_time": None
                }

            if log.scan_type == "entry":
                grouped[key]["entry_time"] = log.scanned_at.strftime("%H:%M:%S")

            elif log.scan_type == "exit":
                grouped[key]["exit_time"] = log.scanned_at.strftime("%H:%M:%S")

        return Response(list(grouped.values()))


class ExportTodayExcelAPIView(APIView):
    def get(self, request):
        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        logs = ScannerLog.objects.select_related("worker").filter(
            scanned_at__gte=start_of_day,
            scanned_at__lt=end_of_day
        ).order_by("worker_id", "scanned_at")

        # --- GÜNƏ GÖRƏ QRUPLAŞDIR ---
        grouped = {}

        for log in logs:
            worker_id = log.worker.id
            date_str = log.scanned_at.strftime("%Y-%m-%d")

            key = f"{worker_id}_{date_str}"

            if key not in grouped:
                grouped[key] = {
                    "worker_name": log.worker.full_name,
                    "date": date_str,
                    "entry_time": None,
                    "exit_time": None
                }

            if log.scan_type == "entry":
                grouped[key]["entry_time"] = log.scanned_at.strftime("%H:%M:%S")
            elif log.scan_type == "exit":
                grouped[key]["exit_time"] = log.scanned_at.strftime("%H:%M:%S")

        wb = Workbook()
        ws = wb.active
        ws.title = "Giriş-Çıxış Cədvəli"

        ws.append(["Name Surname", "Date", "Entry Time", "Exit Time"])

        for row in grouped.values():
            ws.append([
                row["worker_name"],
                row["date"],
                row["entry_time"] or "-",
                row["exit_time"] or "-"
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        response["Content-Disposition"] = 'attachment; filename="today_logs.xlsx"'

        wb.save(response)

        return response