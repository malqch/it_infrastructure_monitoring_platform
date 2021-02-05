from datetime import datetime

from django.db import models


class Tag(models.Model):
    tag_name = models.CharField(max_length=50, null=False)
    tag_remark = models.CharField(max_length=255, null=False)
    is_delete = models.BooleanField(null=False, default=0)
    create_time = models.DateTimeField(null=True, default=datetime.now)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "tag"


class Staff(models.Model):
    username = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=10,
                              choices=(('male', '男'), ('female', '女')),
                              default='male', verbose_name='性别')
    remark = models.TextField(null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.now)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "asset_staff"

class Business(models.Model):
    name = models.CharField(max_length=50, null=False)
    remark = models.TextField(null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.now)
    remove_time = models.DateTimeField(null=True)
    staff = models.OneToOneField(to=Staff, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "asset_business"


class Datacenter(models.Model):
    dc_name = models.CharField(max_length=60, null=False)
    dc_address = models.CharField(max_length=100, null=False)
    remark = models.CharField(max_length=255, null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.now)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "asset_datacenter"


class Room(models.Model):
    room_name = models.CharField(max_length=60, null=False)
    room_address = models.CharField(max_length=100, null=False)
    remark = models.CharField(max_length=255, null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.now)
    remove_time = models.DateTimeField(null=True)
    datacenter = models.ForeignKey(to=Datacenter, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "asset_room"


class Rack(models.Model):
    rack_name = models.CharField(max_length=50, null=False)
    rack_address = models.CharField(max_length=255, null=True)
    remark = models.CharField(max_length=255, null=True)
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.now)
    remove_time = models.DateTimeField(null=True)
    room = models.ForeignKey(to=Room, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "asset_rack"



class Vendor(models.Model):
    vendor_name = models.CharField(max_length=50)  # 供应商名称
    address = models.CharField(max_length=255)  # 地址
    contact = models.CharField(max_length=50)  # 联系人
    phone = models.CharField(max_length=255)  # 电话
    email = models.CharField(max_length=255)  # 邮件
    main_products = models.CharField(max_length=255, null=True)  # 主要产品说明
    sign_up_time = models.CharField(max_length=50, null=True)  # 成立时间
    enterprise_type = models.CharField(max_length=50, null=True)  # 企业类型
    remark = models.TextField(null=True)  # 备注
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(default=datetime.now)
    remove_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "asset_vendor"


class Series(models.Model):
    series_name = models.CharField(max_length=50)

    class Meta:
        db_table = "asset_series"


class Device(models.Model):
    device_name = models.CharField(max_length=50)  # 设备名称
    device_type = models.CharField(max_length=50, null=True)  # 设备类型
    device_status = models.CharField(max_length=50, null=True)  # 设备状态
    device_arrived_date = models.CharField(max_length=50, null=True)  # 进机房时间（采购时间）
    device_expire_date = models.CharField(max_length=50, null=True)  # 过保日期
    data_center = models.ForeignKey(Datacenter, null=True, on_delete=models.SET_NULL)  # 所属数据中心
    location_zone = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)  # 机房
    location_cabinet = models.ForeignKey(Rack, null=True, on_delete=models.SET_NULL)  # 机柜
    device_sn = models.CharField(max_length=50, null=True)  # sn号
    device_vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)  # 供应商
    device_model = models.CharField(max_length=50, null=True)  # 型号
    device_start_unit = models.CharField(max_length=50, null=True)  # 起始U
    device_unit = models.CharField(max_length=50, null=True)  # U高
    belong_business = models.ManyToManyField(Business, through='DeviceBusiness')  # 所属业务
    manage_address = models.CharField(max_length=50, null=True)  # 管理地址
    manage_username = models.CharField(max_length=50, null=True)  # 管理用户名
    manage_password = models.CharField(max_length=50, null=True)  # 管理密码
    snmp_username = models.CharField(max_length=50, null=True)  # snmp用户名
    snmp_password = models.CharField(max_length=50, null=True)  # snmp密码
    snmp_version = models.IntegerField(default=2, null=True)  # snmp的版本
    operate_system = models.CharField(max_length=50, null=True)  # 操作系统
    system_version = models.CharField(max_length=50, null=True)  # 系统版本
    hostname = models.CharField(max_length=50)  # 主机名
    cpu_model = models.CharField(max_length=50, null=True)  # cpu型号
    cpu_cores = models.CharField(max_length=50, null=True)  # cpu核数
    memory_capacity = models.IntegerField(null=True)  # 内存容量
    disk_capacity = models.IntegerField(null=True)  # 磁盘容量
    usage = models.CharField(max_length=50, null=True)  # 用途
    label = models.ManyToManyField(Tag, through='DeviceLabel')  # 标签
    is_delete = models.BooleanField(default=False)
    device_ip = models.CharField(max_length=50, null=True)  # 服务器ip
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    maintain_status = models.CharField(max_length=50, null=True, default='否')  # 维护状态
    series = models.ForeignKey(Series, null=True, on_delete=models.SET_NULL)  # 系列id
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
    snmp_username = models.CharField(max_length=50, null=True)
    snmp_password = models.CharField(max_length=50, null=True)
    operate_system = models.CharField(max_length=50, null=True)
    operate_system_version = models.CharField(max_length=50, null=True)
    cpu_cores = models.CharField(max_length=50, null=True)
    memory_capacity = models.IntegerField(null=True)
    disk_capacity = models.IntegerField(null=True)
    usage = models.CharField(max_length=255, null=True)
    label = models.ManyToManyField(to=Tag, through='VirtualServerLabel')
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    maintain_status = models.CharField(max_length=50, null=True, default='否')  # 维护状态
    remove_time = models.DateTimeField(null=True)
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


class DeviceModel(models.Model):
    """
    设备的模型
    """
    id = models.CharField(max_length=36, primary_key=True) #  设备的id
    name = models.CharField(max_length=32, null=False)  #  设备的名称
    ipaddr = models.CharField(max_length=16, null=False)  #  设备的管理ip
    macaddr = models.CharField(max_length=17, null=True)  #  设备的mac地址
    type = models.CharField(max_length=24, null=False)  #  设备的类型，目前包含的种类有：sdn,vcenter,switch,fw,openstack
    model = models.CharField(max_length=32, null=False)  #  设备的型号
    location = models.CharField(max_length=32, null=True)  #  设备的位置
    manufacture = models.CharField(max_length=32, null=False)  #  生产厂家
    status = models.IntegerField(null=False)  #  设备的状态 0表示在线 1表示离线
    version = models.CharField(max_length=16, null=False)  #  设备的版本号
    source = models.CharField(max_length=36, null=False, default="manual")  #  设备的来源，分为manual和sdn的id，默认为manual
    cloudname = models.CharField(max_length=32, null=True)  #  SDN设备的云平台名称，SDN设备专用的字段
    maximum = models.IntegerField(null=True)  #  物理设备支持的虚拟最大数量。FW设备专用字段
    projectname = models.CharField(max_length=32, null=True)  #  OpenStack的项目名称。OpenStack设备专用字段
    desc = models.CharField(max_length=32, null=True)  #  设备的描述信息
    dgid = models.CharField(max_length=36, null=False)  #  设备组的id
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)

    device_arrived_date = models.CharField(max_length=50, null=True)  # 进机房时间（采购时间）
    device_expire_date = models.CharField(max_length=50, null=True)  # 过保日期
    data_center = models.ForeignKey(Datacenter, null=True, on_delete=models.SET_NULL)  # 所属数据中心
    location_zone = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)  # 机房
    location_cabinet = models.ForeignKey(Rack, null=True, on_delete=models.SET_NULL)  # 机柜
    device_sn = models.CharField(max_length=50, null=True)  # sn号
    device_model = models.CharField(max_length=50, null=True)  # 型号
    device_start_unit = models.CharField(max_length=50, null=True)  # 起始U
    device_unit = models.CharField(max_length=50, null=True)  # U高
    belong_business = models.ManyToManyField(Business, through='DeviceModelBusiness')  # 所属业务
    manage_address = models.CharField(max_length=50, null=True)  # 管理地址
    manage_username = models.CharField(max_length=50, null=True)  # 管理用户名
    manage_password = models.CharField(max_length=50, null=True)  # 管理密码
    snmp_username = models.CharField(max_length=50, null=True)  # snmp用户名
    snmp_password = models.CharField(max_length=50, null=True)  # snmp密码
    snmp_version = models.IntegerField(default=2, null=True)  # snmp的版本
    operate_system = models.CharField(max_length=50, null=True)  # 操作系统
    system_version = models.CharField(max_length=50, null=True)  # 系统版本
    hostname = models.CharField(max_length=50)  # 主机名
    cpu_model = models.CharField(max_length=50, null=True)  # cpu型号
    cpu_cores = models.CharField(max_length=50, null=True)  # cpu核数
    memory_capacity = models.IntegerField(null=True)  # 内存容量
    disk_capacity = models.IntegerField(null=True)  # 磁盘容量
    usage = models.CharField(max_length=50, null=True)  # 用途
    label = models.ManyToManyField(Tag, through='DeviceModelLabel')  # 标签
    # device_ip = models.CharField(max_length=50, null=True)  # 服务器ip
    maintain_status = models.CharField(max_length=50, null=True, default='否')  # 维护状态
    series = models.ForeignKey(Series, null=True, on_delete=models.SET_NULL)  # 系列id
    department_id = models.IntegerField()
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


class Storage(models.Model):
    storage_name = models.CharField(max_length=50)  # 设备名称
    hostname = models.CharField(max_length=50)  # 主机名
    sn = models.CharField(max_length=50, null=True)  # sn号
    vendor = models.ForeignKey(Vendor, null=True,
                               on_delete=models.SET_NULL,
                               related_name='vendor')  # 供应商
    series = models.ForeignKey(Series, null=True,
                               on_delete=models.SET_NULL)  # 系列id
    storage_model = models.CharField(max_length=50, null=True)  # 型号
    data_center = models.ForeignKey(Datacenter, null=True,
                                    on_delete=models.SET_NULL)  # 所属数据中心
    location_zone = models.ForeignKey(Room, null=True,
                                      on_delete=models.SET_NULL)  # 机房
    location_cabinet = models.ForeignKey(Rack, null=True,
                                         on_delete=models.SET_NULL)  # 机柜
    manage_address = models.CharField(max_length=50, null=True)  # 管理地址
    manage_ip = models.CharField(max_length=50, null=True)  # 管理地址
    manage_username = models.CharField(max_length=50, null=True)  # 管理用户名
    manage_password = models.CharField(max_length=50, null=True)  # 管理密码
    storage_start_unit = models.CharField(max_length=50, null=True)  # 起始U
    storage_unit = models.CharField(max_length=50, null=True)  # U高
    label = models.ManyToManyField(Tag, through='StorageLabel')  # 标签
    belong_business = models.ManyToManyField(Business,
                                             through='StorageBusiness')  # 所属业务
    usage = models.CharField(max_length=50, null=True)  # 用途
    disk_capacity = models.IntegerField(null=True)  # 磁盘容量
    disk_model = models.CharField(max_length=50, null=True)  # 磁盘型号
    disk_vendor = models.ForeignKey(Vendor, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='disk_vendor')  # 磁盘厂商
    is_delete = models.BooleanField(default=False)
    controller_num = models.IntegerField(null=True)  # 控制器数量
    controller_system_version = models.CharField(max_length=50,
                                                 null=True)  # 控制器系统版本
    host_port_type = models.CharField(max_length=50, null=True)  # 主机端口类型
    host_port_num = models.IntegerField(null=True)  # 主机端口数量
    extension_port_type = models.CharField(max_length=50, null=True)  # 扩展端口类型
    extension_port_num = models.IntegerField(null=True)  # 扩展端口数量
    extension_rack_type = models.CharField(max_length=50, null=True)  # 扩展柜类型
    extension_rack_num = models.IntegerField(null=True)  # 扩展柜数量
    controller_rack_disk_num = models.IntegerField(null=True)  # 控制柜硬盘数量
    extension_rack_disk_num = models.IntegerField(null=True)  # 扩展柜硬盘数量
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    arrived_date = models.CharField(max_length=50,
                                           null=True)  # 进机房时间（采购时间）
    expire_date = models.CharField(max_length=50, null=True)  # 过保日期
    remove_time = models.DateTimeField(null=True)
    snmp_username = models.CharField(max_length=50, null=True)  # snmp用户名
    snmp_password = models.CharField(max_length=50, null=True)  # snmp密码
    snmp_version = models.IntegerField(default=2, null=True)  # snmp的版本
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



