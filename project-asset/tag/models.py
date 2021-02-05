from datetime import datetime

from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, null=False)
    tag_remark = models.CharField(max_length=255, null=False)
    is_delete = models.BooleanField(null=False, default=0)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "tag"