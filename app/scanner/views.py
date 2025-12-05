from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, serializers
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from openpyxl import Workbook

from drf_spectacular.utils import extend_schema

from .utils import generate_qr_base64
from .serializers import WorkerListSerializer, LoginSerializer, ScannerLogDeleteSerializer
from .pagination import DefaultPagination
from .models import Worker, ScannerLog, ScannerUser
from .authentication import ScannerTokenAuthentication
from .auth_utils import generate_token

from rest_framework.permissions import IsAuthenticated


def scan_view(request):
    return render(request, "scanner/scan.html")


@extend_schema(
    request=LoginSerializer,
    responses={200: serializers.DictField()}
)
class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = ScannerUser.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            return Response({"detail": "Invalid username or password"}, status=401)

        token = generate_token(user.id)
        return Response({"token": token}, status=200)


class GenerateQRAPIView(APIView):
    authentication_classes = [ScannerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=serializers.DictField(),
        responses={201: serializers.DictField()}
    )
    def post(self, request):
        full_name = request.data.get("full_name")
        if not full_name:
            return Response({"detail": "full_name is required"}, status=400)

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
    authentication_classes = [ScannerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: serializers.DictField()})
    def get(self, request):
        now = timezone.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        logs = ScannerLog.objects.filter(
            scanned_at__gte=start,
            scanned_at__lt=end
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
    authentication_classes = [ScannerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=serializers.DictField(),
        responses={200: serializers.DictField()}
    )
    def post(self, request):
        qr_text = request.data.get("qr_text")
        if not qr_text:
            return Response({"detail": "QR code is missing"}, status=400)

        if not qr_text.startswith("WORKER_ID:"):
            return Response({"detail": "Invalid QR format"}, status=400)

        worker_id = qr_text.replace("WORKER_ID:", "").strip()
        worker = Worker.objects.filter(id=worker_id).first()

        if not worker:
            return Response({"detail": "Worker not found"}, status=404)

        now = timezone.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        today_logs = ScannerLog.objects.filter(
            worker=worker,
            scanned_at__gte=start,
            scanned_at__lt=end
        ).order_by("scanned_at")

        count = today_logs.count()

        # ===============================
        #     LIMIT CHECK (max 2 scans)
        # ===============================
        if count >= 2:
            return Response(
                {"detail": "This worker has already scanned twice today"},
                status=403
            )

        # ===============================
        #      FIRST SCAN → ENTRY
        # ===============================
        if count == 0:
            log = ScannerLog.objects.create(worker=worker, scan_type="entry")
            return Response({
                "worker": worker.full_name,
                "scan_type": "entry",
                "time": log.scanned_at.strftime("%H:%M:%S"),
                "detail": "Entry recorded"
            })

        # ===============================
        #   SECOND SCAN (EXIT) — MUST WAIT 15 MINUTES
        # ===============================
        if count == 1:
            first_log = today_logs.first()
            diff = now - first_log.scanned_at

            # 15 minutes = 900 seconds
            if diff.total_seconds() < 900:
                remaining = int(900 - diff.total_seconds())
                minutes = remaining // 60
                seconds = remaining % 60

                return Response(
                    {
                        "detail": f"Exit scan is not allowed yet. Please wait {minutes} minutes and {seconds} seconds."
                    },
                    status=403
                )

            log = ScannerLog.objects.create(worker=worker, scan_type="exit")
            return Response({
                "worker": worker.full_name,
                "scan_type": "exit",
                "time": log.scanned_at.strftime("%H:%M:%S"),
                "detail": "Exit recorded"
            })



class WorkerListAPIView(generics.ListAPIView):
    authentication_classes = [ScannerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Worker.objects.all().order_by("-id")
    serializer_class = WorkerListSerializer
    pagination_class = DefaultPagination


class ScannedUsersListAPIView(APIView):
    authentication_classes = [ScannerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: serializers.ListSerializer(child=serializers.DictField())})
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
    authentication_classes = [ScannerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: None})
    def get(self, request):
        now = timezone.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        logs = ScannerLog.objects.select_related("worker").filter(
            scanned_at__gte=start,
            scanned_at__lt=end
        ).order_by("worker_id", "scanned_at")

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
        ws.title = "Daily Logs"
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
        response["Content-Disposition"] = 'attachment; filename=\"today_logs.xlsx\"'

        wb.save(response)
        return response


@extend_schema(
    description="Verilmiş ID-ə uyğun Workeri silir"
)
class WorkerDeleteAPIView(generics.DestroyAPIView):
    queryset = Worker.objects.all()
    serializer_class = WorkerListSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


@extend_schema(
    description="Verilmiş ID-ə uyğun ScannerLog-u silir"
)
class LogDeleteAPIView(generics.DestroyAPIView):
    queryset = ScannerLog.objects.all()
    serializer_class = ScannerLogDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"


# class ScannerLogDeleteAPIView(APIView):
#     authentication_classes = [ScannerTokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     @extend_schema(
#         request=serializers.DictField(),
#         responses={200: serializers.DictField()},
#         description="ScannerLog modelindən id-ə əsasən log silir (DELETE)"
#     )
#     def delete(self, request):
#         log_id = request.data.get("id")

#         if not log_id:
#             return Response({"detail": "id is required"}, status=400)

#         log = ScannerLog.objects.filter(id=log_id).first()
#         if not log:
#             return Response({"detail": "Log not found"}, status=404)

#         log.delete()

#         return Response(
#             {
#                 "success": True,
#                 "detail": f"Log #{log_id} deleted successfully"
#             },
#             status=200
#         )
