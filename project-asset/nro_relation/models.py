
from datetime import datetime

from django.db import models

from data_center.models import Datacenter, Room, Rack
from device.models import Series
from logic_resource.models import Business, Vendor, Staff
from tag.models import Tag


class DeviceModel(models.Model):
    """
    设备的模型
    """
    id = models.CharField(max_length=36, primary_key=True) #  设备的id
    name = models.CharField(max_length=32, null=False)  #  设备的名称
    ipaddr = models.CharField(max_length=16, null=False)  #  设备的管理ip
    macaddr = models.CharField(max_length=17, null=True, blank=True)  #  设备的mac地址
    type = models.CharField(max_length=24, null=False)  #  设备的类型，目前包含的种类有：sdn,vcenter,switch,fw,openstack
    model = models.CharField(max_length=32, null=True, blank=True)  #  设备的型号
    location = models.CharField(max_length=32, null=True)  #  设备的位置
    manufacture = models.CharField(max_length=128, null=True, blank=True)  #  生产厂家
    status = models.IntegerField(null=False, default=0)  #  设备的状态 0表示在线 1表示离线
    version = models.CharField(max_length=16, null=True, blank=True)  #  设备的版本号
    source = models.CharField(max_length=36, null=False, default="manual")  #  设备的来源，分为manual和sdn的id，默认为manual
    cloudname = models.CharField(max_length=32, null=True)  #  SDN设备的云平台名称，SDN设备专用的字段
    maximum = models.IntegerField(null=True)  #  物理设备支持的虚拟最大数量。FW设备专用字段
    projectname = models.CharField(max_length=32, null=True)  #  OpenStack的项目名称。OpenStack设备专用字段
    desc = models.CharField(max_length=32, null=True, blank=True)  #  设备的描述信息
    dgid = models.CharField(max_length=36, null=False)  #  设备组的id
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    device_arrived_date = models.CharField(max_length=50, null=True)  #  进机房时间（采购时间）
    device_expire_date = models.CharField(max_length=50, null=True)  #  过保日期
    data_center = models.ForeignKey(Datacenter, null=True, on_delete=models.SET_NULL)  # 所属数据中心
    location_zone = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)  # 机房
    location_cabinet = models.ForeignKey(Rack, null=True, on_delete=models.SET_NULL)  # 机柜
    device_sn = models.CharField(max_length=50, null=True, blank=True)  # sn号
    device_model = models.CharField(max_length=50, null=True, blank=True)  # 型号
    device_start_unit = models.CharField(max_length=50, null=True, blank=True)  # 起始U
    device_unit = models.CharField(max_length=50, null=True, blank=True)  # U高
    belong_business = models.ManyToManyField(Business, through='DeviceModelBusiness')  # 所属业务
    manage_address = models.CharField(max_length=50, null=True, blank=True)  # 管理地址
    manage_username = models.CharField(max_length=50, null=True, blank=True)  # 管理用户名
    manage_password = models.CharField(max_length=50, null=True, blank=True)  # 管理密码
    snmp_username = models.CharField(max_length=50, null=True, blank=True)  # snmp用户名
    snmp_password = models.CharField(max_length=50, null=True, blank=True)  # snmp密码
    snmp_version = models.IntegerField(default=2)  # snmp的版本
    operate_system = models.CharField(max_length=50, null=True, blank=True)  # 操作系统
    system_version = models.CharField(max_length=50, null=True, blank=True)  # 系统版本
    hostname = models.CharField(max_length=50, null=True, blank=True)  # 主机名
    cpu_model = models.CharField(max_length=50, null=True, blank=True)  # cpu型号
    cpu_cores = models.CharField(max_length=50, null=True, blank=True)  # cpu核数
    memory_capacity = models.IntegerField(null=True, blank=True)  # 内存容量
    disk_capacity = models.IntegerField(null=True, blank=True)  # 磁盘容量
    usage = models.CharField(max_length=50, null=True, blank=True)  # 用途
    label = models.ManyToManyField(Tag, through='DeviceModelLabel')  # 标签
    maintain_status = models.CharField(max_length=50, null=True, default='否')  # 维护状态
    series = models.ForeignKey(Series, null=True, on_delete=models.SET_NULL)  # 系列id
    department_id = models.IntegerField(null=False, default=1)
    random_id = models.IntegerField(null=True)
    is_monitor = models.CharField(max_length=10, default="是")
    asset_manager = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)  # 资产管理者id

    class Meta:
        db_table = 'device'


class DeviceModelBusiness(models.Model):
    network = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    class Meta:
        db_table = "network_business"


class DeviceModelLabel(models.Model):
    network = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    label = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = "network_label"