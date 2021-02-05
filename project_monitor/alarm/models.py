from datetime import datetime

from django.db import models
# from django_mysql.models import JSONFileld


class AlarmSeverity(models.Model):
    grade_name = models.CharField(max_length=50, null=False)            # 告警等级名称
    grade_level = models.IntegerField(null=False)
    remark = models.CharField(max_length=255, null=False)               # 备注
    is_delete = models.BooleanField(null=False, default=0)              # 删除状态
    remove_time = models.DateTimeField(null=True)                       # 移除时间
    create_time = models.DateTimeField(null=False, default=datetime.now)# 创建时间

    class Meta:
        db_table = "alarm_severity"


class AlarmStrategy(models.Model):
    strategy_name = models.CharField(max_length=50, null=False)           # 告警策略名称
    strategy_level = models.IntegerField(null=False)
    remark = models.TextField(null=False)                                 # 描述
    is_delete = models.BooleanField(null=False, default=0)                # 删除状态
    remove_time = models.DateTimeField(null=True)                         # 移除时间
    create_time = models.DateTimeField(null=False, default=datetime.now)  # 创建时间

    class Meta:
        db_table = "alarm_strategy"


class AlarmRule(models.Model):
    rule_name = models.CharField(max_length=50, null=False)                # 告警规则名称
    alarm_object = models.CharField(max_length=50, null=False)             #　监控对象
    tag = models.CharField(max_length=255, null=False)                     # 标签id
    device_name = models.CharField(max_length=50, null=False)
    server_type = models.CharField(max_length=50)
    rule_detail = models.TextField(null=False)                              # 规则详情
    # index = models.CharField(max_length=50, null=False)                    # 指标项
    # threshold = models.IntegerField(null=False)                            # 阈值
    # alarm_severity = models.CharField(max_length=50, null=False, default="notification")  # 告警等级
    # alarm_strategy = models.CharField(max_length=50, null=False)           # 告警策略
    # num = models.IntegerField(null=False)                                  # 告警次数
    # operator = models.CharField(max_length=50, null=False)                 # 运算符号
    # notification = models.CharField(max_length=50, null=False)             # 告警通知方式
    create_time = models.DateTimeField(default=datetime.now)               # 告警规则创建时间
    update_time = models.DateTimeField(default=datetime.now)               # 告警规则修改时间
    remove_time = models.DateTimeField(null=True)                          # 告警规则移除时间
    is_delete = models.BooleanField(default=0)                             # 告警规则删除状态

    class Meta:
        db_table = 'alarm_rule'


class AlarmDetail(models.Model):
    alarm_ip = models.CharField(max_length=25, null=False)
    alarm_server_name = models.CharField(max_length=25, null=False)
    indicator_name = models.CharField(max_length=25, null=False)
    indicator_code = models.CharField(max_length=25,null=False)
    alarm_strategy = models.IntegerField(null=False)
    alarm_level = models.IntegerField(null=False)
    notice_code = models.IntegerField(null=False)
    server_type = models.CharField(max_length=20, null=False)
    collect_value = models.CharField(max_length=50, null=False)
    deal_flag = models.BooleanField(null=False)
    alarm_status = models.CharField(max_length=25, null=False)
    alarm_count = models.IntegerField(null=False)
    remark = models.CharField(max_length=255, null=False)
    alarm_first_time = models.DateTimeField(default=datetime.now)
    alarm_last_time = models.DateTimeField(null=False)
    alarm_time = models.DateTimeField(null=True)
    upgrade_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)

    class Meta:
        db_table = 'alarm_details'


