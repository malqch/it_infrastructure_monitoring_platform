
from django.db import models


class StorageItem(models.Model):
    item_name = models.CharField(max_length=50, null=False)
    item = models.CharField(max_length=30, null=False)
    item_obj = models.CharField(max_length=100, null=False)
    storage_type = models.CharField(max_length=20, null=False, default='HUAWEI')
    remark = models.TextField(max_length=200, null=True)

    class Meta:
        db_table = "storage_item"

