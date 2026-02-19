"""
Django REST Framework serializers for API endpoints.
"""

from rest_framework import serializers
from .models import SystemMetric, ApiRequest, Alert


class SystemMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMetric
        fields = "__all__"
        read_only_fields = ("timestamp",)


class ApiRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiRequest
        fields = "__all__"
        read_only_fields = ("timestamp",)


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"
        read_only_fields = ("created_at", "triggered_at", "resolved_at")
