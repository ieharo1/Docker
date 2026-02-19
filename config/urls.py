"""
URL Configuration for monitoring dashboard project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

# Import viewsets
from api.views import HealthViewSet, MetricsViewSet

# Create router
router = routers.DefaultRouter()
router.register(r"health", HealthViewSet, basename="health")
router.register(r"metrics-info", MetricsViewSet, basename="metrics-info")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    # Prometheus metrics endpoint (at /metrics)
    path("", include("django_prometheus.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
