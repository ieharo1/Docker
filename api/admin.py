"""
Admin configuration for monitoring dashboard API.
"""

from django.contrib import admin
from .models import SystemMetric, ApiRequest, Alert


@admin.register(SystemMetric)
class SystemMetricAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "memory_mb",
        "cpu_percent",
        "database_connections",
        "requests_per_second",
    )
    list_filter = ("timestamp",)
    readonly_fields = ("timestamp",)
    search_fields = ("timestamp",)


@admin.register(ApiRequest)
class ApiRequestAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "method", "endpoint", "status", "response_time_ms")
    list_filter = ("status", "method", "timestamp")
    readonly_fields = ("timestamp",)
    search_fields = ("endpoint", "user_agent")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("name", "severity", "status", "metric", "threshold", "triggered_at")
    list_filter = ("severity", "status", "created_at")
    readonly_fields = ("created_at", "triggered_at", "resolved_at")
    search_fields = ("name", "metric")
