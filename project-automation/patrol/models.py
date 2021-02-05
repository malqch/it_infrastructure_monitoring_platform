from django.db import models
import datetime
from script.models import Script

class Patrol(models.Model):
    patrol_name = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_delete = models.BooleanField(default=False)
    script = models.ManyToManyField(to=Script, through='PatrolScript')  # 执行的脚本
    period = models.CharField(max_length=50)  # 脚本的执行周期
    exec_time = models.CharField(max_length=50, null=True) # 脚本的执行时间
    uuid = models.CharField(max_length=50, null=True)
    params = models.CharField(max_length=255)  # 参数信息
    status = models.CharField(max_length=50, default='未执行')  # 状态
    create_time = models.DateTimeField(default=datetime.datetime.now)
    update_time = models.DateTimeField(default=datetime.datetime.now)


    class Meta:
        db_table = "automation_patrol"

class PatrolScript(models.Model):
    patrol = models.ForeignKey(Patrol, on_delete=models.CASCADE)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)

    class Meta:
        db_table = "patrol_script"





