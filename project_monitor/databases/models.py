from django.db import models
from datetime import datetime
# Create your models here.


class Databases(models.Model):

    name = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField()
    physicalip = models.GenericIPAddressField()
    port = models.IntegerField()
    sid = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    remark = models.CharField(max_length=200, null=True)
    is_delete = models.BooleanField(default=False)
    remove_time = models.DateTimeField(null=True)
    db_type = models.CharField(max_length=20, default='MYSQL', null=False)
    main_mode = models.CharField(max_length=10, default='否')
    is_monitor = models.CharField(max_length=10)

    class Meta:
        db_table = "monitor_db"


class DBItem(models.Model):
    item_name = models.CharField(max_length=50, null=False)
    item = models.CharField(max_length=30, null=False)
    db_type = models.CharField(max_length=20, null=False, default='MYSQL')
    remark = models.TextField(max_length=200, null=True)

    is_available = models.CharField(max_length=50, null=False)  # 告警可用
    is_delete = models.BooleanField(null=False, default=0)  # 删除状态
    remove_time = models.DateTimeField(null=True)  # 移除时间
    create_time = models.DateTimeField(null=False, default=datetime.now)  # 创建时间

    class Meta:
        db_table = "db_item"

