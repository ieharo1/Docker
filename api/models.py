"""
Django models for monitoring dashboard.
"""

from django.db import models


class SystemMetric(models.Model):
    """
    Model to store system metrics collected over time.
    """

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    memory_mb = models.FloatField(help_text="Memory usage in MB")
    cpu_percent = models.FloatField(help_text="CPU usage percentage")
    database_connections = models.IntegerField(default=0)
    requests_per_second = models.FloatField(default=0)
    error_rate = models.FloatField(default=0)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "System Metric"
        verbose_name_plural = "System Metrics"
        indexes = [
            models.Index(fields=["-timestamp"]),
        ]

    def __str__(self):
        return f"SystemMetric at {self.timestamp}"


class ApiRequest(models.Model):
    """
    Model to log API requests for monitoring purposes.
    """

    STATUS_CHOICES = [
        ("2xx", "2xx Success"),
        ("3xx", "3xx Redirect"),
        ("4xx", "4xx Client Error"),
        ("5xx", "5xx Server Error"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    method = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=255, db_index=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    response_time_ms = models.IntegerField(help_text="Response time in milliseconds")
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "API Request"
        verbose_name_plural = "API Requests"
        indexes = [
            models.Index(fields=["-timestamp"]),
            models.Index(fields=["endpoint", "-timestamp"]),
        ]

    def __str__(self):
        return f"{self.method} {self.endpoint} - {self.status}"


class Alert(models.Model):
    """
    Model to store alert rules and their states.
    """

    SEVERITY_CHOICES = [
        ("info", "Info"),
        ("warning", "Warning"),
        ("critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("resolved", "Resolved"),
        ("acknowledged", "Acknowledged"),
    ]

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    metric = models.CharField(max_length=255)
    threshold = models.FloatField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    triggered_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"

    def __str__(self):
        return f"{self.name} - {self.severity}"
