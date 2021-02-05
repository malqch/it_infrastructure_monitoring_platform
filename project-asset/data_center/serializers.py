from rest_framework import serializers
from data_center.models import Datacenter, Room, Rack


class DatacenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datacenter
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    datacenter = DatacenterSerializer(read_only=True)

    class Meta:
        model = Room
        fields = '__all__'


class RackSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Rack
        fields = '__all__'
