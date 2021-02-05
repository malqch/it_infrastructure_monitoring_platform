from django.db import models
from logic_resource.models import Business
from tag.models import Tag
from data_center.models import Datacenter, Room, Rack
from logic_resource.models import Vendor, Staff


class Series(models.Model):
    series_name = models.CharField(max_length=50)

    class Meta:
        db_table = "asset_series"


class Device(models.Model):
    device_name = models.CharField(max_length=50)  # 设备名称
    device_type = models.CharField(max_length=50, null=True, default='服务器')  # 设备类型
    device_status = models.CharField(max_length=50, null=True, blank=True)  # 设备状态
    device_arrived_date = models.CharField(max_length=50, null=True, blank=True)  # 进机房时间（采购时间）
    device_expire_date = models.CharField(max_length=50, null=True, blank=True)  # 过保日期
    data_center = models.ForeignKey(Datacenter, null=True, on_delete=models.SET_NULL)  # 所属数据中心
    location_zone = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)  # 机房
    location_cabinet = models.ForeignKey(Rack, null=True, on_delete=models.SET_NULL)  # 机柜
    device_sn = models.CharField(max_length=50, null=True, blank=True)  # sn号
    device_vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)  # 供应商
    device_model = models.CharField(max_length=50, null=True, blank=True)  # 型号
    device_start_unit = models.CharField(max_length=50, null=True, blank=True)  # 起始U
    device_unit = models.CharField(max_length=50, null=True, blank=True)  # U高
    belong_business = models.ManyToManyField(Business, through='DeviceBusiness')  # 所属业务
    manage_address = models.CharField(max_length=50, null=True, blank=True)  # 管理地址
    manage_username = models.CharField(max_length=50, null=True, blank=True)  # 管理用户名
    manage_password = models.CharField(max_length=50, null=True, blank=True)  # 管理密码
    ssh_port = models.IntegerField(default=22, null=True, blank=True)  # ssh端口
    snmp_username = models.CharField(max_length=50, null=True, blank=True)  # snmp用户名
    snmp_password = models.CharField(max_length=50, null=True, blank=True)  # snmp密码
    snmp_version = models.IntegerField(default=2, null=True, blank=True)  # snmp的版本
    operate_system = models.CharField(max_length=50, null=True, blank=True)  # 操作系统
    system_version = models.CharField(max_length=50, null=True, blank=True)  # 系统版本
    hostname = models.CharField(max_length=50)  # 主机名
    cpu_model = models.CharField(max_length=50, null=True, blank=True)  # cpu型号
    cpu_cores = models.CharField(max_length=50, null=True, blank=True)  # cpu核数
    memory_capacity = models.IntegerField(null=True, blank=True)  # 内存容量
    disk_capacity = models.IntegerField(null=True, blank=True)  # 磁盘容量
    usage = models.CharField(max_length=50, null=True, blank=True)  # 用途
    label = models.ManyToManyField(Tag, through='DeviceLabel')  # 标签
    is_delete = models.BooleanField(default=False)
    device_ip = models.CharField(max_length=50, null=True, blank=True)  # 服务器ip
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    maintain_status = models.CharField(max_length=50, null=True, default='否')  # 维护状态
    series = models.ForeignKey(Series, null=True, on_delete=models.SET_NULL)  # 系列id
    remove_time = models.DateTimeField(null=True, blank=True)
    is_monitor = models.CharField(max_length=10, default="是")
    asset_manager = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)  # 资产管理者id

    class Meta:
        db_table = "asset_device"


class DeviceBusiness(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    class Meta:
        db_table = "asset_device_business"


class DeviceLabel(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    label = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = "asset_device_label"


class VirtualServer(models.Model):
    virtual_ip = models.CharField(max_length=50, null=True)  # 服务器ip
    hostname = models.CharField(max_length=50)
    type = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    belong_business = models.ManyToManyField(to=Business, through='VirtualServerBusiness')
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    ssh_port = models.IntegerField(default=22, null=True, blank=True)  # ssh端口
    snmp_username = models.CharField(max_length=50, null=True, blank=True)
    snmp_password = models.CharField(max_length=50, null=True, blank=True)
    operate_system = models.CharField(max_length=50, null=True)
    operate_system_version = models.CharField(max_length=50, null=True)
    cpu_cores = models.CharField(max_length=50, null=True)
    memory_capacity = models.IntegerField(null=True)
    disk_capacity = models.IntegerField(null=True)
    usage = models.CharField(max_length=255, null=True, blank=True)
    label = models.ManyToManyField(to=Tag, through='VirtualServerLabel')
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    maintain_status = models.CharField(max_length=50, null=True, default='否')  # 维护状态
    remove_time = models.DateTimeField(null=True)
    is_monitor = models.CharField(max_length=10, default='是')
    asset_manager = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)  # 资产管理者id

    class Meta:
        db_table = "virtual_server"


class VirtualServerBusiness(models.Model):
    virtual_server = models.ForeignKey(VirtualServer, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    class Meta:
        db_table = "virtual_server_business"


class VirtualServerLabel(models.Model):
    virtual_server = models.ForeignKey(VirtualServer, on_delete=models.CASCADE)
    label = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = "virtual_server_label"


class Storage(models.Model):
    storage_name = models.CharField(max_length=50)  # 设备名称
    hostname = models.CharField(max_length=50)  # 主机名
    port = models.IntegerField(null=True, blank=True)  # 端口
    sn = models.CharField(max_length=50, null=True, blank=True)  # sn号
    vendor = models.ForeignKey(Vendor, null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name='vendor')  # 供应商
    series = models.ForeignKey(Series, null=True,
                               on_delete=models.SET_NULL)  # 系列id
    storage_model = models.CharField(max_length=50, null=True, blank=True)  # 型号
    data_center = models.ForeignKey(Datacenter, null=True,
                                    on_delete=models.SET_NULL)  # 所属数据中心
    location_zone = models.ForeignKey(Room, null=True,
                                      on_delete=models.SET_NULL)  # 机房
    location_cabinet = models.ForeignKey(Rack, null=True,
                                         on_delete=models.SET_NULL)  # 机柜
    manage_address = models.CharField(max_length=50, null=True, blank=True)  # 管理地址
    manage_ip = models.CharField(max_length=50, null=True, blank=True)  # 管理地址
    manage_username = models.CharField(max_length=50, null=True, blank=True)  # 管理用户名
    manage_password = models.CharField(max_length=50, null=True, blank=True)  # 管理密码
    storage_start_unit = models.CharField(max_length=50, null=True, blank=True)  # 起始U
    storage_unit = models.CharField(max_length=50, null=True, blank=True)  # U高
    label = models.ManyToManyField(Tag, through='StorageLabel')  # 标签
    belong_business = models.ManyToManyField(Business,
                                             through='StorageBusiness')  # 所属业务
    usage = models.CharField(max_length=50, null=True, blank=True)  # 用途
    disk_capacity = models.IntegerField(null=True, blank=True)  # 磁盘容量
    disk_model = models.CharField(max_length=50, null=True, blank=True)  # 磁盘型号
    disk_vendor = models.ForeignKey(Vendor, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='disk_vendor')  # 磁盘厂商
    is_delete = models.BooleanField(default=False)
    controller_num = models.IntegerField(null=True, blank=True)  # 控制器数量
    controller_system_version = models.CharField(max_length=50,
                                                 null=True, blank=True)  # 控制器系统版本
    host_port_type = models.CharField(max_length=50, null=True, blank=True)  # 主机端口类型
    host_port_num = models.IntegerField(null=True, blank=True)  # 主机端口数量
    extension_port_type = models.CharField(max_length=50, null=True, blank=True)  # 扩展端口类型
    extension_port_num = models.IntegerField(null=True, blank=True)  # 扩展端口数量
    extension_rack_type = models.CharField(max_length=50, null=True, blank=True)  # 扩展柜类型
    extension_rack_num = models.IntegerField(null=True, blank=True)  # 扩展柜数量
    controller_rack_disk_num = models.IntegerField(null=True, blank=True)  # 控制柜硬盘数量
    extension_rack_disk_num = models.IntegerField(null=True, blank=True)  # 扩展柜硬盘数量
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    arrived_date = models.CharField(max_length=50, null=True, blank=True)  # 进机房时间（采购时间）
    expire_date = models.CharField(max_length=50, null=True, blank=True)  # 过保日期
    remove_time = models.DateTimeField(null=True)
    snmp_username = models.CharField(max_length=50, null=True, blank=True)  # snmp用户名
    snmp_password = models.CharField(max_length=50, null=True, blank=True)  # snmp密码
    snmp_version = models.IntegerField(default=2, null=True, blank=True)  # snmp的版本
    is_monitor = models.CharField(max_length=10, default="是")
    asset_manager = models.ForeignKey(Staff, null=True, on_delete=models.SET_NULL)  # 资产管理者id

    class Meta:
        db_table = 'storage'


class StorageBusiness(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    class Meta:
        db_table = "storage_business"


class StorageLabel(models.Model):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    label = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        db_table = "storage_label"


class Network(models.Model):
    mac = models.CharField(max_length=50, null=True)
    netmask = models.CharField(max_length=50, null=True)
    ip = models.CharField(max_length=50, null=True)
    broadcast = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50, null=True, default='内网')  # 类型，外网/内网
    device = models.ForeignKey(Device, null=True, on_delete=models.SET_NULL)
    virtual_server = models.ForeignKey(VirtualServer, null=True, on_delete=models.SET_NULL)
    storage = models.ForeignKey(Storage, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "dev_network"



