from datetime import datetime

from django.db import models


class Series(models.Model):
    source_id = models.IntegerField(null=False)       # 资产id
    vendor_id = models.IntegerField(null=False)       # 厂商id
    series_name = models.CharField(max_length=25)     # 系列名称

    class Meta:
        db_table = 'net_series'


class NetworkMonitor(models.Model):
    indicator_name = models.CharField(max_length=50, null=False)                # 指标名称
    indicator_code = models.CharField(max_length=50, null=False)                # 指标
    indicator_oid = models.CharField(max_length=200, null=False)                # 指标标识
    indicator_type = models.CharField(max_length=255, null=False)               # 指标类型
    series_id = models.CharField(max_length=10)                                 # 系列id
    is_active = models.CharField(max_length=50, null=False)                     # 是否使用
    collect_type = models.IntegerField(null=False, default=0)                   # 采集方式
    is_delete = models.BooleanField(null=False, default=0)                      # 是否被删除
    gmt_create = models.DateTimeField(null=True)                                # 创建时间
    gmt_modified = models.DateTimeField(null=False, default=datetime.now)       # 更新时间
    remove_time = models.DateTimeField(null=True)                               # 删除时间
    remark = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "network_monitor"