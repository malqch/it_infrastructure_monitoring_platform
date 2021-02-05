from django.db import models
import datetime
# Create your models here.


class ServerAnalysis(models.Model):

    host_ip = models.GenericIPAddressField()
    host_name = models.CharField(max_length=100, null=True)
    indicator_name = models.CharField(max_length=100, null=True)
    indicator_value = models.CharField(max_length=50)
    indicator_code = models.CharField(max_length=50)
    service_type = models.CharField(max_length=200, null=True)
    insert_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "test_analysis"


