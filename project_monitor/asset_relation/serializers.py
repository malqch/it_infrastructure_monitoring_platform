from rest_framework import serializers
from asset_relation.models import Tag, Business, Device, Staff, Series, VirtualServer, DeviceModel

#
class TagSerializer(serializers.ModelSerializer):
    # rule_detail = Jsonserializer()

    class Meta:
        model = Tag
        fields = '__all__'
#
#
class DeviceSerializer(serializers.ModelSerializer):
    # rule_detail = Jsonserializer()

    class Meta:
        model = Device
        fields = '__all__'
#
#
#
class BusinessSerializer(serializers.ModelSerializer):
    # rule_detail = Jsonserializer()

    class Meta:
        model = Business
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    # rule_detail = Jsonserializer()

    class Meta:
        model = Staff
        fields = '__all__'
#

class SeriesSerializer(serializers.ModelSerializer):
    # rule_detail = Jsonserializer()

    class Meta:
        model = Series
        fields = '__all__'

#
#
class VirtualServerSerializer(serializers.ModelSerializer):
    # rule_detail = Jsonserializer()

    class Meta:
        model = VirtualServer
        fields = '__all__'


class DeviceModelSerializer(serializers.ModelSerializer):
    # rule_detail = Jsonserializer()

    class Meta:
        model = DeviceModel
        fields = '__all__'