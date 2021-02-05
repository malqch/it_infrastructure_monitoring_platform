from django.db import models
import datetime


class Staff(models.Model):
    username = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=10,
                              choices=(('male', '男'), ('female', '女')),
                              default='male', verbose_name='性别')
    remark = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    update_time = models.DateTimeField(auto_now=True)  # 修改时间

    class Meta:
        db_table = "asset_staff"


class Business(models.Model):
    name = models.CharField(max_length=50, null=False)
    remark = models.TextField(null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)
    staff = models.ForeignKey(to=Staff, blank=True, null=True, on_delete=models.SET_NULL)
    update_time = models.DateTimeField(auto_now=True)  # 修改时间

    class Meta:
        db_table = "asset_business"


class Contract(models.Model):
    contract_name = models.CharField(max_length=60, null=False)
    sign_time = models.CharField(max_length=50, null=True)  # 合同签署时间
    remark = models.TextField(null=True)  # 备注
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "asset_contract"


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=50)  # 供应商名称
    address = models.CharField(max_length=255)  # 地址
    contact = models.CharField(max_length=50)  # 联系人
    phone = models.CharField(max_length=255)  # 电话
    email = models.CharField(max_length=255)  # 邮件
    main_products = models.CharField(max_length=255, null=True, blank=True)  # 主要产品说明
    sign_up_time = models.CharField(max_length=50, null=True, blank=True)  # 成立时间
    enterprise_type = models.CharField(max_length=50, null=True, blank=True)  # 企业类型
    remark = models.TextField(null=True, blank=True)  # 备注
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(auto_now=True)  # 修改时间

    class Meta:
        db_table = "asset_vendor"
