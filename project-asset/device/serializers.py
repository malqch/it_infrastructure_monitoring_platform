from rest_framework import serializers
from device.models import Device, Network, VirtualServer, Series, Storage
from logic_resource.serializers import BusinessSerializer
from tag.serializers import TagSerializer
from data_center.serializers import DatacenterSerializer, RackSerializer, RoomSerializer
from logic_resource.serializers import VendorSerializer, StaffSerializer


class SeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Series
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    belong_business = BusinessSerializer(read_only=True, many=True)
    label = TagSerializer(read_only=True, many=True)
    data_center = DatacenterSerializer(read_only=True)
    location_zone = RoomSerializer(read_only=True)
    location_cabinet = RackSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    device_vendor = VendorSerializer(read_only=True)
    asset_manager = StaffSerializer(read_only=True)

    class Meta:
            model = Device
            fields = '__all__'
            # exclude = ('manage_password', 'snmp_password')


class VirtualServerSerializer(serializers.ModelSerializer):
    belong_business = BusinessSerializer(read_only=True, many=True)
    label = TagSerializer(read_only=True, many=True)
    asset_manager = StaffSerializer(read_only=True)

    class Meta:
        model = VirtualServer
        fields = '__all__'
        # exclude = ('password', 'snmp_password')


class StorageSerializer(serializers.ModelSerializer):
    belong_business = BusinessSerializer(read_only=True, many=True)
    label = TagSerializer(read_only=True, many=True)
    data_center = DatacenterSerializer(read_only=True)
    location_zone = RoomSerializer(read_only=True)
    location_cabinet = RackSerializer(read_only=True)
    series = SeriesSerializer(read_only=True)
    vendor = VendorSerializer(read_only=True)
    disk_vendor = VendorSerializer(read_only=True)
    asset_manager = StaffSerializer(read_only=True)

    class Meta:
        model = Storage
        fields = '__all__'
        # exclude = ('manage_password',)


class NetworkSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    virtual_server = VirtualServerSerializer(read_only=True)
    asset_manager = StaffSerializer(read_only=True)

    class Meta:
        model = Network
        fields = '__all__'
