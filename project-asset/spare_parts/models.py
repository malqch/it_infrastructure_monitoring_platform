from datetime import datetime

from django.db import models


class Disk(models.Model):
    disk_vendor = models.CharField(max_length=50, null=False)
    disk_capacity = models.IntegerField(null=False, default=0)
    disk_sn = models.CharField(max_length=50, null=False)
    disk_status = models.CharField(max_length=50, default='空闲', null=False)
    disk_host = models.CharField(max_length=50, null=True)
    is_delete = models.BooleanField(default=0, null=False)
    disk_service_start_time = models.CharField(max_length=50, null=True)
    disk_service_end_time = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = "dev_disk"


class Hba(models.Model):
    id = models.AutoField(primary_key=True)
    hba_vendor = models.CharField(max_length=60, null=False)
    hba_sn = models.CharField(max_length=50, null=False)
    hba_pn = models.CharField(max_length=50, null=False)
    hba_status = models.CharField(max_length=50, default='空闲', null=True)
    hba_host = models.CharField(max_length=50, null=True)
    hba_description = models.CharField(null=True, max_length=200)
    is_delete = models.BooleanField(default=0, null=False)
    hba_service_start_time = models.CharField(max_length=50, null=True)
    hba_service_end_time = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'dev_hba'


class Hca(models.Model):
    hca_vendor = models.CharField(max_length=50, null=False)
    hca_sn = models.CharField(max_length=50, null=False)
    hca_status = models.CharField(max_length=50, default='空闲', null=True)
    hca_host = models.CharField(max_length=50, null=True)
    hca_description = models.CharField(null=True, max_length=200)
    is_delete = models.BooleanField(default=0, null=False)
    hca_service_start_time = models.CharField(max_length=50, null=True)
    hca_service_end_time = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'dev_hca'


class Nic(models.Model):
    nic_vendor = models.CharField(max_length=60, null=False)
    nic_sn = models.CharField(max_length=50, null=False)
    nic_pn = models.CharField(max_length=50, null=False)
    nic_status = models.CharField(max_length=50, default='空闲', null=True)
    nic_host = models.CharField(max_length=50, null=True)
    nic_description = models.CharField(null=True, max_length=200)
    is_delete = models.BooleanField(default=0, null=False)
    nic_service_start_time = models.CharField(max_length=50, null=True)
    nic_service_end_time = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'dev_nic'


class Ssd(models.Model):
    ssd_vendor = models.CharField(max_length=60, null=False)
    ssd_capacity = models.IntegerField(null=False, default=0)
    ssd_sn = models.CharField(max_length=50, null=False)
    ssd_status = models.CharField(max_length=50, default='空闲', null=True)
    ssd_host = models.CharField(max_length=50, null=True)
    ssd_description = models.CharField(null=True, max_length=200)
    is_delete = models.BooleanField(default=0, null=False)
    ssd_service_start_time = models.CharField(max_length=50, null=True)
    ssd_service_end_time = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'dev_ssd'

