import datetime
from django.db import models

# Create your models here.

class HuaweiyunManager(models.Model):
    hw_address = models.CharField(max_length=255)
    hw_ip = models.CharField(max_length=50)
    hw_username = models.CharField(max_length=50)
    hw_password = models.CharField(max_length=255)
    update_time = models.DateTimeField(null=True)
    create_time = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "huaweiyun_manager"

