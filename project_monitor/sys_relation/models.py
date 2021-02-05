from django.db import models
import datetime



class Role(models.Model):
    name = models.CharField(max_length=50)
    mark = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "sys_role"

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)
    roles = models.ManyToManyField(Role, through='RoleUser')

    class Meta:
        db_table = "sys_user"

class RoleUser(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "sys_user_role"

