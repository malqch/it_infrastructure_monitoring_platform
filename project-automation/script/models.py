from django.db import models
import datetime

class Script(models.Model):
    script_name = models.CharField(max_length=50)
    script_type = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    desc = models.CharField(max_length=255, null=True, blank=True)
    use = models.IntegerField(choices=((0, u'脚本'), (1, u'巡检脚本')), default=0)
    param = models.CharField(max_length=255, null=True, blank=True)
    test_status = models.CharField(max_length=50)
    ef_time = models.DateTimeField()
    ex_time = models.DateTimeField()
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    update_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "automation_script"

class ScriptLog(models.Model):
    script_name = models.CharField(max_length=50)
    network_ip = models.CharField(max_length=50)
    hostname = models.CharField(max_length=255)
    username = models.CharField(max_length=20)
    executor = models.CharField(max_length=50)
    script_output = models.CharField(max_length=255)
    execute_time = models.DateTimeField(default=datetime.datetime.now)
    execute_res = models.CharField(max_length=255)
    log_use = models.IntegerField(choices=((0, u'脚本'), (1, u'巡检脚本')), default=0)
    patrol_name = models.CharField(max_length=50)
    is_delete = models.BooleanField(default=False)
    uuid = models.CharField(max_length=255)

    class Meta:
        db_table = "automation_script_log"

class ScriptTimedTask(models.Model):
    script_name = models.CharField(max_length=50)
    host_info = models.TextField()
    execute_type = models.CharField(max_length=50)
    execute_time = models.CharField(max_length=50)
    execute_week = models.CharField(max_length=50, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    param = models.CharField(max_length=255, null=True, blank=True)
    status = models.IntegerField(choices=((0, u'运行中'), (1, u'已暂停')), default=0)
    executor = models.CharField(max_length=50)
    is_delete = models.BooleanField(default=False)
    uuid = models.CharField(max_length=255)
    create_time = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "automation_script_timed_task"




