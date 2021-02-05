from datetime import datetime

from django.db import models


class ServerMonitor(models.Model):
    monitor_type = models.CharField(max_length=50, null=False)          # 监控类型（服务器/数据库/中间件/网络设备/存储）
    specific_type = models.CharField(max_length=50, null=False)         # 具体类型（服务器：Linux/Windows）
    indicator = models.CharField(max_length=50, null=False)             # 指标项名称
    indicator_name = models.CharField(max_length=200, null=False)       # 指标项
    remark = models.CharField(max_length=255, null=False)               # 备注
    is_available = models.CharField(max_length=50, null=False)          # 告警可用
    is_delete = models.BooleanField(null=False, default=0)              # 删除状态
    remove_time = models.DateTimeField(null=True)                       # 移除时间
    create_time = models.DateTimeField(null=False, default=datetime.now)# 创建时间

    class Meta:
        db_table = "server_monitor"