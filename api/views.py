"""
API Views for monitoring dashboard application.
"""

import time
import psutil
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from prometheus_client import Counter, Histogram, Gauge

# Define custom metrics
request_counter = Counter(
    "api_requests_total", "Total API requests", ["method", "endpoint", "status"]
)

request_duration = Histogram(
    "api_request_duration_seconds",
    "API request duration in seconds",
    ["method", "endpoint"],
)

error_counter = Counter(
    "api_errors_total", "Total API errors", ["method", "endpoint", "status"]
)

database_connections = Gauge(
    "database_connections_active", "Active database connections"
)

memory_usage = Gauge(
    "application_memory_usage_bytes", "Application memory usage in bytes"
)

cpu_usage = Gauge("application_cpu_percent", "Application CPU usage percentage")


class HealthViewSet(viewsets.ViewSet):
    """
    Health check viewset for monitoring application status.
    """

    renderer_classes = [JSONRenderer]

    @action(detail=False, methods=["get"])
    def status(self, request):
        """
        Get application health status with system metrics.
        """
        start_time = time.time()

        try:
            # Collect system metrics
            process = psutil.Process()
            memory_info = process.memory_info()
            cpu_percent = process.cpu_percent(interval=0.1)

            # Update gauges
            memory_usage.set(memory_info.rss)
            cpu_usage.set(cpu_percent)

            # Database connection check (simulate)
            database_connections.set(1)

            duration = time.time() - start_time

            health_data = {
                "status": "healthy",
                "timestamp": time.time(),
                "version": "1.0.0",
                "service": "monitoring-dashboard",
                "metrics": {
                    "memory_mb": round(memory_info.rss / 1024 / 1024, 2),
                    "cpu_percent": round(cpu_percent, 2),
                    "database_connections": 1,
                },
                "response_time_ms": round(duration * 1000, 2),
            }

            request_counter.labels(
                method=request.method, endpoint="/health/status/", status=200
            ).inc()

            request_duration.labels(
                method=request.method, endpoint="/health/status/"
            ).observe(duration)

            return Response(health_data, status=status.HTTP_200_OK)

        except Exception as e:
            error_counter.labels(
                method=request.method, endpoint="/health/status/", status=500
            ).inc()

            return Response(
                {"status": "unhealthy", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def ready(self, request):
        """
        Readiness probe for Kubernetes/Docker orchestration.
        """
        return Response({"ready": True}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def live(self, request):
        """
        Liveness probe for Kubernetes/Docker orchestration.
        """
        return Response({"alive": True}, status=status.HTTP_200_OK)


class MetricsViewSet(viewsets.ViewSet):
    """
    Metrics information viewset providing application metrics details.
    """

    renderer_classes = [JSONRenderer]

    @action(detail=False, methods=["get"])
    def list_available(self, request):
        """
        List all available metrics being tracked.
        """
        start_time = time.time()

        metrics_info = {
            "application_metrics": [
                {
                    "name": "api_requests_total",
                    "type": "counter",
                    "description": "Total API requests by method, endpoint and status",
                    "labels": ["method", "endpoint", "status"],
                },
                {
                    "name": "api_request_duration_seconds",
                    "type": "histogram",
                    "description": "API request duration in seconds",
                    "labels": ["method", "endpoint"],
                },
                {
                    "name": "api_errors_total",
                    "type": "counter",
                    "description": "Total API errors by method, endpoint and status",
                    "labels": ["method", "endpoint", "status"],
                },
                {
                    "name": "database_connections_active",
                    "type": "gauge",
                    "description": "Active database connections",
                    "labels": [],
                },
                {
                    "name": "application_memory_usage_bytes",
                    "type": "gauge",
                    "description": "Application memory usage in bytes",
                    "labels": [],
                },
                {
                    "name": "application_cpu_percent",
                    "type": "gauge",
                    "description": "Application CPU usage percentage",
                    "labels": [],
                },
            ],
            "django_prometheus_metrics": [
                {
                    "name": "django_http_requests_total_by_method",
                    "type": "counter",
                    "description": "Django HTTP requests total by method",
                },
                {
                    "name": "django_http_requests_latency_seconds_by_view_method",
                    "type": "histogram",
                    "description": "Django HTTP request latency by view and method",
                },
                {
                    "name": "django_http_response_status_count",
                    "type": "counter",
                    "description": "Django HTTP response status code count",
                },
            ],
            "prometheus_metrics": [
                {
                    "name": "up",
                    "type": "gauge",
                    "description": "Whether the last scrape was successful",
                },
                {
                    "name": "scrape_duration_seconds",
                    "type": "gauge",
                    "description": "Seconds it took for the last scrape",
                },
            ],
        }

        duration = time.time() - start_time

        request_counter.labels(
            method=request.method, endpoint="/metrics-info/list_available/", status=200
        ).inc()

        request_duration.labels(
            method=request.method, endpoint="/metrics-info/list_available/"
        ).observe(duration)

        return Response(metrics_info, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def simulate_load(self, request):
        """
        Simulate API load for testing metrics collection.
        """
        iterations = int(request.data.get("iterations", 10))

        for i in range(iterations):
            request_counter.labels(
                method="POST", endpoint="/metrics-info/simulate_load/", status=200
            ).inc()

            time.sleep(0.01)  # Simulate processing

        return Response(
            {"message": f"Load simulation completed with {iterations} requests"},
            status=status.HTTP_200_OK,
        )
