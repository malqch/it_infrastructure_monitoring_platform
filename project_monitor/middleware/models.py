from django.db import models
from datetime import datetime
# Create your models here.


class Middleware(models.Model):

    name = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
    username = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    remark = models.CharField(max_length=200, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    remove_time = models.DateTimeField(null=True)
    middleware_type = models.CharField(max_length=20, null=False)
    main_mode = models.CharField(max_length=10, default='否')
    is_monitor = models.CharField(max_length=10)

    class Meta:
        db_table = "monitor_middleware"


class MiddlewareItem(models.Model):
    item_name = models.CharField(max_length=50, null=False)
    item = models.CharField(max_length=30, null=False)
    middleware_type = models.CharField(max_length=20, null=False)
    remark = models.TextField(max_length=200, null=True)
    is_available = models.CharField(max_length=50, null=False)  # 告警可用
    create_time = models.DateTimeField(null=False, default=datetime.now)  # 创建时间

    class Meta:
        db_table = "middleware_item"
