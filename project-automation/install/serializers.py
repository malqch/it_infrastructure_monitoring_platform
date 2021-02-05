from rest_framework import serializers
from install.models import PxeServer, PxeServerOs, JobInstall, JobCheck, Port


class PxeServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PxeServer
        fields = '__all__'


class PxeServerOsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PxeServerOs
        fields = '__all__'


class PmPortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        fields = '__all__'


class JobCheckSerializer(serializers.ModelSerializer):
    job_check = PmPortSerializer(many=True)

    class Meta:
        model = JobCheck
        fields = ['id', 'job_check', "device_name", "hostname", "sn", "status",
                  "usage", "location", "console_ip", "console_user", "console_password",
                  "ipmi_server_ip", "pxe_server_ip", "update_time"]


class JobInstallSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInstall
        fields = '__all__'

