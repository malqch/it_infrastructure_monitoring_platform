from django.db import models
import datetime
from django_mysql.models import JSONField


class PxeServer(models.Model):
    pxe_name = models.CharField(max_length=50, null=False)
    pxe_server_ip = models.CharField(max_length=50)
    ipmi_server_ip = models.CharField(max_length=50)
    ifenable = models.CharField(max_length=50)  # 是否启用
    device_usage = models.CharField(max_length=50, null=True)  # 用途
    remark = models.TextField(null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "pxe_server"


class PxeServerOs(models.Model):
    os_name = models.CharField(max_length=50, null=True)  # os名称
    os_version = models.CharField(max_length=50, null=True)  # os版本
    ks_content = models.TextField(null=True)
    # pxe_server_ip = models.CharField(max_length=50, null=True)  # os所属pxe server
    pxe_server_id = models.IntegerField(null=True)  # os所属pxe server
    ks_name = models.CharField(max_length=50, null=True)  # ks文件名称
    ifenable = models.CharField(max_length=50, null=True, default='disabled')  # 是否启用
    profile = models.CharField(max_length=20, null=True)  # profile名称
    type = models.CharField(max_length=20, null=True)  # 系统类型（vm/rhel/rhev/exit）
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "pxe_server_os"


class JobCheck(models.Model):
    device_name = models.CharField(max_length=50)  # 设备名称
    hostname = models.CharField(max_length=50, null=True)  # 主机名
    sn = models.CharField(max_length=50)  # 设备编号
    status = models.CharField(max_length=20, default="WAITING")  # 状态
    usage = models.CharField(max_length=50)  # 设备用途
    location = models.CharField(max_length=50)  # 物理机位置
    console_ip = models.CharField(max_length=50)  # 物理机ip
    console_user = models.CharField(max_length=50)  # 物理机用户名
    console_password = models.CharField(max_length=50)  # 物理机密码
    ipmi_server_ip = models.CharField(max_length=50)  # ipmitool服务器ip
    pxe_server_ip = models.CharField(max_length=50)  # pxe server的ip
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间

    class Meta:
        db_table = "job_check"


class Port(models.Model):
    mac = models.CharField(max_length=50, null=True)
    switch = models.CharField(max_length=50, null=True)
    port = models.CharField(max_length=50, null=True)
    vlan = models.CharField(max_length=50, null=True)
    ifname = models.CharField(max_length=50, null=True)
    job_check = models.ForeignKey(JobCheck, null=True, on_delete=models.SET_NULL, related_name="job_check")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pm_port"


class JobInstall(models.Model):
    device_name = models.CharField(max_length=50)  # 设备名称
    sn = models.CharField(max_length=50)  # 设备编号
    status = models.CharField(max_length=20, default="WAITING")  # 装机状态
    ip = models.CharField(max_length=50)  # 设备需修改成的ip地址
    gateway = models.CharField(max_length=50)  # 网关
    netmask = models.CharField(max_length=50)  # 子网掩码
    hostname = models.CharField(max_length=50)  # 主机hostname
    usage = models.CharField(max_length=50)  # 设备用途
    location = models.CharField(max_length=50)  # 物理机位置
    type = models.CharField(max_length=10)  # Vm/rhev/rhel/exi
    console_ip = models.CharField(max_length=50)  # ip
    console_user = models.CharField(max_length=50)  # 名称
    console_password = models.CharField(max_length=50)  # user密码
    ipmi_server_ip = models.CharField(max_length=50)  # 堡垒机：ipmitool机器
    os_name = models.CharField(max_length=50)  # os名称
    os_version = models.CharField(max_length=50)  # os版本
    ks_name = models.CharField(max_length=50)  # ks文件名称
    profile = models.CharField(max_length=50)  # os信息
    pxe_server_ip = models.CharField(max_length=50)
    install = models.IntegerField(null=True)  # 安装状态
    # vlanid = models.CharField(max_length=20, null=True)
    mac = JSONField()  # 与pxe绑定的mac地址
    ifname = JSONField()  # 接口名称
    install_ip = models.CharField(max_length=50, null=True)  # 安装操作系统时的私网ip
    update_time = models.DateTimeField(auto_now=True)  # 创建时间和更新时间

    class Meta:
        db_table = "job_install"
