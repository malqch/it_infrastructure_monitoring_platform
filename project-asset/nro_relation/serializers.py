from rest_framework import serializers

from data_center.serializers import DatacenterSerializer, RoomSerializer, RackSerializer
from device.serializers import SeriesSerializer
from logic_resource.serializers import BusinessSerializer, VendorSerializer, StaffSerializer
from nro_relation.models import DeviceModel
from tag.serializers import TagSerializer


class DeviceModelSerializer(serializers.ModelSerializer):
    belong_business = BusinessSerializer(read_only=True, many=True)
    label = TagSerializer(read_only=True, many=True)
    data_center = DatacenterSerializer(read_only=True)
    location_zone = RoomSerializer(read_only=True)
    location_cabinet = RackSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    asset_manager = StaffSerializer(read_only=True)

    class Meta:
            model = DeviceModel
            fields = '__all__'
            # exclude = ('manage_password', 'snmp_password')