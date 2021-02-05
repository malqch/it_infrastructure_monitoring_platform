from rest_framework import serializers
from spare_parts.models import Disk, Hba, Hca, Nic, Ssd


class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk
        fields = '__all__'


class HbaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hba
        fields = '__all__'


class HcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hca
        fields = '__all__'


class NicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nic
        fields = '__all__'


class SsdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ssd
        fields = '__all__'

