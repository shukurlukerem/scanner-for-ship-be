from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from scanner.views import scan_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('scan/', scan_view, name='scan'),

    # API docs (Swagger + Redoc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # scanner app API-lər
    path('api/', include("scanner.urls")),
]
