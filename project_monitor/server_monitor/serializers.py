from rest_framework import serializers
from server_monitor.models import ServerMonitor


class ServerMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerMonitor
        fields = '__all__'
