from django.db import models
import datetime


class Datacenter(models.Model):
    dc_name = models.CharField(max_length=60, null=False)
    dc_address = models.CharField(max_length=100, null=False)
    remark = models.CharField(max_length=255, null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    update_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "asset_datacenter"


class Room(models.Model):
    room_name = models.CharField(max_length=60, null=False)
    room_address = models.CharField(max_length=100, null=False)
    remark = models.CharField(max_length=255, null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    update_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)
    datacenter = models.ForeignKey(to=Datacenter, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "asset_room"

    # @property
    # def create_time(self):
    #     return int(round(self._create_time.to_python(self._create_time).timestamp() * 1000))


class Rack(models.Model):
    rack_name = models.CharField(max_length=50, null=False)
    rack_address = models.CharField(max_length=255, null=True)
    remark = models.CharField(max_length=255, null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    update_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)
    room = models.ForeignKey(to=Room, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "asset_rack"

    # @property
    # def create_time(self):
    #     return int(round(self._create_time.to_python(self._create_time).timestamp() * 1000))



