from django.db import models
import datetime

class Menu(models.Model):
    name = models.CharField(max_length=50)
    action_code = models.CharField(max_length=255, null=True, blank=True)
    prev_menu = models.CharField(max_length=50, null=True, blank=True)
    menu_url = models.CharField(max_length=255, null=True, blank=True)
    p_id = models.BigIntegerField()
    application = models.CharField(max_length=255)
    is_function = models.BooleanField(default=False)
    icon = models.CharField(max_length=255, null=True)
    is_delete = models.BooleanField(default=False)
    perms = models.CharField(max_length=255, null=True, blank=True)
    menu_type = models.CharField(max_length=255)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "sys_menu"

class Role(models.Model):
    name = models.CharField(max_length=50)
    mark = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)
    menus = models.ManyToManyField(Menu, through='RoleMenu')

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

class Token(models.Model):
    user = models.OneToOneField(to=User, blank=True, null=True, on_delete=models.SET_NULL)
    token = models.CharField(max_length=64)
    expire_time = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = "sys_token"

class RoleMenu(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = "sys_role_menu"
