from rest_framework import serializers
from network_monitor.models import NetworkMonitor, Series


class NetworkMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkMonitor
        fields = '__all__'


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'
