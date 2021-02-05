from django.forms import model_to_dict
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from auth.views import MyAuthentication
from data_center.models import Datacenter, Rack
from device.models import Device, Network, DeviceBusiness, DeviceLabel, \
    VirtualServer, VirtualServerLabel, VirtualServerBusiness, Series, Storage, \
    StorageBusiness, StorageLabel
from device.serializers import DeviceSerializer, NetworkSerializer, \
    VirtualServerSerializer, SeriesSerializer, StorageSerializer
from django.core.paginator import Paginator
import xlrd
from logic_resource.views import Business, Vendor
import datetime
from tag.views import Tag
from django.db.models import Count
from nro_relation.models import DeviceModel


logger = logging.getLogger('log')


class CommonUtil(object):
    @staticmethod
    def is_chinese(string):
        """
        检查整个字符串是否包含中文
        :param string: 需要检查的字符串
        :return: bool
        """
        for ch in str(string):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True

        return False


class DeviceViewSet(viewsets.ModelViewSet):
    # authentication_classes = [MyAuthentication, ]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def create(self, request, *args, **kwargs):
        logger.info(request.data)
        # 查询是否有同名device_name
        device_info = Device.objects.filter(device_name=request.data.get('device_name'), is_delete=0).all()
        # 查询是否有同名hostname
        device_info_hostname = Device.objects.filter(hostname=request.data.get('hostname'), is_delete=0).all()
        if len(device_info) == 0 and len(device_info_hostname) == 0:
            device_network = request.data.get("network", [])
            belong_business_name = request.data.get("belong_business", [])
            business_info = Business.objects.filter(
                name__in=belong_business_name).filter(is_delete=0).all()
            if 'belong_business' in request.data.keys():
                request.data.pop("belong_business")
            # 获得标签的id
            labels_name = request.data.get('label', [])
            labels = Tag.objects.filter(tag_name__in=labels_name).filter(
                is_delete=0).all()
            if 'label' in request.data.keys():
                request.data.pop("label")
            request.data['data_center_id'] = request.data.get('data_center', '')
            request.data['location_zone_id'] = request.data.get('location_zone', '')
            request.data['location_cabinet_id'] = request.data.get('location_cabinet', '')
            request.data.pop('data_center')
            request.data.pop('location_zone')
            request.data.pop('location_cabinet')
            series = request.data.get('series', '')
            if series:
                request.data['series_id'] = series
                request.data.pop('series')
            device_vendor = request.data.get('device_vendor', None)
            if device_vendor:
                request.data['device_vendor_id'] = device_vendor
                request.data.pop('device_vendor')
            device = Device.objects.create(**request.data)
            for business in business_info:
                device.belong_business.add(business)
            for label in labels:
                device.label.add(label)
            list_ = []
            for network in device_network:
                netmask = network.get("netmask")
                mac = network.get('mac')
                ip = network.get('ip')
                broadcast = network.get('broadcast')
                type = network.get("type")
                if netmask or mac or ip or broadcast:
                    list_.append(Network(netmask=netmask, mac=mac, ip=ip,
                                     broadcast=broadcast, device=device, type=type))
            Network.objects.bulk_create(list_)
            serializer = DeviceSerializer(device)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            result = {'msg': '主机名或设备名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        network_info = request.data.get("network", [])
        device_id = request.data.get("id", None)
        device_name = request.data.get('device_name', '')
        device_name_object = Device.objects.filter(device_name=device_name, is_delete=0).first()
        if device_name_object and device_name_object.id != device_id:
            result = {'msg': '设备名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)
        # 查询是否有同名hostname
        hostname = request.data.get('hostname', '')
        device_hostname_object = Device.objects.filter(hostname=hostname, is_delete=0).first()
        if device_hostname_object and device_hostname_object.id != device_id:
            result = {'msg': '主机名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)
        device = self.get_object()
        device.series_id = request.data.get('series', '')
        device.data_center_id = request.data.get('data_center', '')
        device.location_zone_id = request.data.get('location_zone', '')
        device.location_cabinet_id = request.data.get('location_cabinet', '')
        device.device_vendor_id = request.data.get('device_vendor', '')
        device.asset_manager_id = request.data.get('asset_manager', '')
        device.save()
        # 获得业务的名称
        belong_business_name = request.data.get("belong_business")
        business_obj = Business.objects.filter(name__in=belong_business_name).filter(is_delete=0).all()
        # 获得标签的名称
        labels_name = request.data.get('label')
        labels_obj = Tag.objects.filter(tag_name__in=labels_name).filter(is_delete=0).all()

        DeviceBusiness.objects.filter(device=device_id).delete()
        DeviceLabel.objects.filter(device=device_id).delete()
        for business in business_obj:
            device.belong_business.add(business)
        for label in labels_obj:
            device.label.add(label)
        list_ = []
        Network.objects.filter(device=device_id).delete()
        for network in network_info:
            netmask = network.get("netmask")
            mac = network.get('mac')
            ip = network.get('ip')
            broadcast = network.get('broadcast')
            type = network.get("type")
            if netmask or mac or ip or broadcast:
                list_.append(Network(netmask=netmask, mac=mac, ip=ip,
                                 broadcast=broadcast, device=device, type=type))
        Network.objects.bulk_create(list_)
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        # 定义条件查询参数
        search_dict = dict()
        device_type = request.query_params.get('device_type', None)
        if device_type:
            search_dict['device_type'] = device_type
        device_ip = request.query_params.get('device_ip', None)
        if device_ip:
            search_dict['device_ip'] = device_ip
        device_name = request.query_params.get("device_name", None)
        if device_name:
            search_dict['device_name'] = device_name
        device_status = request.query_params.get("device_status", None)
        if device_status:
            search_dict['device_status'] = device_status
        device_vendor = request.query_params.get("device_vendor", None)
        if device_vendor:
            search_dict['device_vendor'] = device_vendor
        maintain_status = request.query_params.get("maintain_status", None)
        if maintain_status:
            search_dict['maintain_status'] = maintain_status
        hostname = request.query_params.get("hostname", None)
        if hostname:
            search_dict['hostname'] = hostname
        asset_manager = request.query_params.get("asset_manager", None)
        if asset_manager:
            search_dict['asset_manager'] = asset_manager
        search_dict['is_delete'] = 0
        device_info = Device.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(device_info, pre_page)
            result = paginator.page(current_page)
            data = self.get_serializer(result, many=True).data
            # 定义返回结果
            res = dict()
            res['total_page'] = paginator.num_pages
            res['current_page'] = current_page
            res['pre_page'] = pre_page
            res['total_count'] = paginator.count
            res['data'] = data
            return Response(res)
        else:
            return Response(self.get_serializer(device_info, many=True).data)

    @action(detail=False, methods=['post'])
    def excel(self, request):
        """ 导入Excel数据，pk是所属项目的pk """
        excel_obj = request.FILES.get("file", "")
        filename = excel_obj.name
        if filename and '.' in filename and filename.rsplit('.', 1)[1] == "xls":
            excel_data = xlrd.open_workbook(filename=None, file_contents=excel_obj.read(), formatting_info=True)
        elif filename and '.' in filename and filename.rsplit('.', 1)[1] == 'xlsx':
            excel_data = xlrd.open_workbook(filename=None, file_contents=excel_obj.read())
        else:
            result = {'msg': '文件格式错误'}
            return Response(result, status=status.HTTP_412_PRECONDITION_FAILED)
        table = excel_data.sheets()[0]  # 打开第一张表
        nrows = table.nrows
        list_ = []
        device_name_list = []
        hostname_list = []
        for row in range(1, nrows):
            res_dict = dict()
            device_name = table.cell(row, 0).value
            chinese_res = CommonUtil.is_chinese(device_name)
            if chinese_res:
                result = {'msg': '设备名称不能包含中文'}
                return Response(result, status=status.HTTP_409_CONFLICT)
            device_info = Device.objects.filter(
                device_name=device_name, is_delete=0).all()
            if len(device_info) > 0 or device_name in device_name_list:
                result = {'msg': '设备:' + device_name + ',已存在或excel中有重复数据'}
                return Response(result, status=status.HTTP_409_CONFLICT)
            device_name_list.append(device_name)
            res_dict['device_name'] = device_name
            res_dict['device_ip'] = table.cell(row, 1).value
            res_dict['device_sn'] = table.cell(row, 2).value
            res_dict['device_status'] = table.cell(row, 3).value
            res_dict['device_model'] = table.cell(row, 4).value
            res_dict['device_start_unit'] = table.cell(row, 5).value
            res_dict['device_unit'] = table.cell(row, 6).value
            res_dict['usage'] = table.cell(row, 7).value
            res_dict['manage_username'] = table.cell(row, 8).value
            res_dict['manage_password'] = table.cell(row, 9).value
            res_dict['manage_address'] = table.cell(row, 10).value
            res_dict['snmp_username'] = table.cell(row, 11).value
            res_dict['snmp_password'] = table.cell(row, 12).value
            hostname = table.cell(row, 13).value
            chinese_res = CommonUtil.is_chinese(hostname)
            if chinese_res:
                result = {'msg': '主机名不能包含中文'}
                return Response(result, status=status.HTTP_409_CONFLICT)
            device_info = Device.objects.filter(
                hostname=hostname, is_delete=0).all()
            if len(device_info) > 0 or hostname in hostname_list:
                result = {'msg': '主机名:' + hostname + ',已存在或excel中有重复数据'}
                return Response(result, status=status.HTTP_409_CONFLICT)
            hostname_list.append(hostname)
            res_dict['hostname'] = hostname
            res_dict['operate_system'] = table.cell(row, 14).value
            res_dict['system_version'] = table.cell(row, 15).value
            res_dict['cpu_model'] = table.cell(row, 16).value
            res_dict['cpu_cores'] = table.cell(row, 17).value
            res_dict['memory_capacity'] = table.cell(row, 18).value
            res_dict['disk_capacity'] = table.cell(row, 19).value
            # res_dict['device_arrived_date'] = table.cell(row, 20).value
            # res_dict['device_expire_date'] = table.cell(row, 21).value
            device_arrived_date = table.cell(row, 20).value
            device_expire_date = table.cell(row, 21).value
            arrived_ctype = table.cell(row, 20).ctype
            if arrived_ctype == 3:
                arrived_value = datetime.datetime(
                    *xlrd.xldate_as_tuple(device_arrived_date, 0))
                device_arrived_date = arrived_value.strftime('%Y-%d-%m')
            res_dict['device_arrived_date'] = device_arrived_date
            expire_ctype = table.cell(row, 21).ctype
            if expire_ctype == 3:
                expire_value = datetime.datetime(
                    *xlrd.xldate_as_tuple(device_expire_date, 0))
                device_expire_date = expire_value.strftime('%Y-%d-%m')
            res_dict['device_expire_date'] = device_expire_date
            res_dict['is_monitor'] = "是"
            list_.append(Device(**res_dict))
        Device.objects.bulk_create(list_)
        result = {'msg': '插入成功'}
        return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        device = self.get_object()
        business_info = DeviceBusiness.objects.filter(device=device)
        if len(business_info):
            result = {'msg': '该设备有关联业务，请先确定是否取消关联'}
            return Response(result)
        label_info = DeviceLabel.objects.filter(device=device)
        if len(label_info):
            result = {'msg': '该设备有关联标签，请先确定是否取消关联'}
            return Response(result)
        device.is_delete = 1
        device.remove_time = datetime.datetime.now()
        DeviceBusiness.objects.filter(device=device).delete()
        DeviceLabel.objects.filter(device=device).delete()
        Network.objects.filter(device=device).update(device="")
        device.series_id = ''
        device.data_center_id = ''
        device.location_cabinet_id = ''
        device.location_zone_id = ''
        device.device_vendor_id = ''
        device.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['PUT'])
    def update_maintain_state(self, request, pk):
        device_obj = self.get_object()
        device_obj.maintain_status = request.data.get("maintain_status", "否")
        device_obj.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def hostname_list(self, request):
        """
        查询hostnamel列表中的数据
        :param request:
        :return:
        """
        hostname_list = request.data.get("hostname_list", [])
        device_type = request.data.get("device_type", "")
        device_info = Device.objects.filter(hostname__in=hostname_list,
                                            device_type=device_type, is_delete=0).values(
            "device_name", "device_sn", "location_zone", "manage_address",
            "manage_username", "manage_password", "hostname", "usage", "device_type")
        return Response(device_info)

    @action(detail=False, methods=['GET'])
    def visualization(self, request):
        """
        查询系统内各类资产数量
        :param request:
        :return:
        """
        dict_ = dict()
        # 查询系统内各类资产数量
        asset_info = list(Device.objects.filter(is_delete=0).values("device_type").annotate(Count("device_type")))
        storage_count = Storage.objects.filter(is_delete=0).count()
        device_info = list(DeviceModel.objects.values("type").annotate(device_type__count=Count("type")))
        for device in device_info[:]:
            if device.get('type') == 'FW':
                device.pop('type')
                device['device_type'] = '防火墙'
            elif device.get('type') == 'LB':
                device.pop('type')
                device['device_type'] = '负载均衡'
            elif device.get('type') == 'Router':
                device.pop('type')
                device['device_type'] = '路由器'
            elif device.get('type') == 'Switch':
                device.pop('type')
                device['device_type'] = '交换机'
            else:
                device_info.remove(device)
        asset_info.extend(device_info)
        asset_info.append({"device_type": "存储", "device_type__count": storage_count})
        dict_['asset_info'] = asset_info
        # 查询系统内物理服务器与虚拟服务器信息
        server_info = list()
        [server_info.append(asset) for asset in asset_info if asset['device_type'] == '服务器']
        virtual_server_count = VirtualServer.objects.filter(is_delete=0).count()
        if virtual_server_count != 0:
            virtual_server_info = [{'device_type': '虚拟服务器', 'device_type__count': virtual_server_count}]
            server_info.extend(virtual_server_info)
        dict_['server_data'] = server_info
        # 查询系统内各类操作系统数量
        operate_system_info = list(
            Device.objects.filter(device_type='服务器', is_delete=0).values(
                "operate_system").annotate(Count("operate_system")))
        virtual_operate_system = list(VirtualServer.objects.filter(is_delete=0).values(
            "operate_system").annotate(Count("operate_system")))
        operate_system_info.extend(virtual_operate_system)
        dic = dict()
        for operate_system in operate_system_info:
            value = operate_system.get('operate_system', None)
            if value and value in dic.keys():
                dic[value] = dic[value] + operate_system.get('operate_system__count', 0)
            elif value and value not in dic.keys():
                dic[value] = operate_system.get('operate_system__count', 0)
        dict_['operate_system_data'] = [{'operate_system': k, 'operate_system__count': v} for k,v in dic.items()]
        # 查询各物理资产所属厂商数量
        vendor_dict = dict()
        ventor_group = list(Device.objects.filter(is_delete=0, device_type='服务器').values('device_vendor').annotate(Count('device_vendor')))
        device_vendor = []
        for device in ventor_group:
            device_dict = {}
            vendor_id = device.get("device_vendor")
            if vendor_id:
                device_dict['value'] = device.get('device_vendor__count')
                vendor_info = Vendor.objects.filter(id=vendor_id).first()
                device_dict['name'] = vendor_info.vendor_name
                device_vendor.append(device_dict)
        vendor_dict['服务器'] = device_vendor
        storage_group = list(Storage.objects.filter(is_delete=0).values('vendor').annotate(Count('vendor')))
        storage_vendor = []
        for storage in storage_group:
            storage_dict = {}
            vendor_id = storage.get("vendor")
            if vendor_id:
                storage_dict['value'] = storage.get('vendor__count')
                vendor_info = Vendor.objects.filter(id=vendor_id).first()
                storage_dict['name'] = vendor_info.vendor_name
                storage_vendor.append(storage_dict)
        vendor_dict['存储'] = storage_vendor

        network_group = DeviceModel.objects.values('manufacture', 'type').annotate(
            Count('manufacture'))
        for network in network_group:
            type_ = network.get('type')
            if type_ != 'Switch' and type_ != 'Router' and type_ != 'LB' and type_ != "FW":
                continue
            elif type_ == 'Switch':
                name = "交换机"
            elif type_ == 'Router':
                name = "路由器"
            elif type_ == 'LB':
                name = '负载均衡'
            elif type_ == 'FW':
                name = '防火墙'
            manufacture = network.get('manufacture')
            manufacture_count = network.get('manufacture__count')
            if name in vendor_dict.keys():
                value_ = vendor_dict.get(name)
                value_.append({'name': manufacture, 'value': manufacture_count})
            else:
                vendor_dict[name] = [{'name': manufacture, 'value': manufacture_count}]
        dict_['vendor_dict'] = vendor_dict
        # 查询机房信息
        datacenter_list = Datacenter.objects.filter(is_delete=0).annotate(num_room=Count('room'))
        data_list = []
        # 遍历数据中心查询机房
        for datacenter in datacenter_list:
            datacenter_dict = {}
            datacenter_name = datacenter.dc_name
            datacenter_id = datacenter.id
            num_room = datacenter.num_room
            datacenter_dict['datacenter_name'] = datacenter_name
            datacenter_dict['num_room'] = num_room
            datacenter_dict['datacenter_id'] = datacenter_id
            room_list = datacenter.room_set.all()
            room_info = []
            # 遍历机房查询机柜
            for room in room_list:
                room_dict = {}
                room_name = room.room_name
                room_id = room.id
                rack_list = room.rack_set.all()
                num_rack = len(rack_list)
                room_dict['room_name'] = room_name
                room_dict['num_rack'] = num_rack
                room_dict['room_id'] = room_id
                # 遍历机柜查询机柜中服务器的信息及数量
                rack_info = []
                for rack in rack_list:
                    rack_dict = {}
                    rack_dict['location_cabinet'] = rack.rack_name
                    rack_dict['rack_id'] = rack.id
                    rack_dict['device_num'] = rack.device_set.filter(is_delete=0, device_type="服务器").count()
                    rack_dict['storage_num'] = rack.storage_set.filter(is_delete=0).count()
                    rack_dict['network_num'] = rack.devicemodel_set.filter(type__in=['Switch', 'Router', 'LB', "FW"]).count()
                    rack_dict['num_device'] = int(rack_dict['device_num']) + int(rack_dict['storage_num']) + int(rack_dict['network_num'])
                    rack_info.append(rack_dict)
                room_dict['rack_info'] = rack_info
                room_info.append(room_dict)
            datacenter_dict['room_info'] = room_info
            data_list.append(datacenter_dict)
        dict_['datacenter_info'] = data_list
        # 查询即将过保的设备
        now_time = datetime.datetime.now()
        date = ((now_time + datetime.timedelta(days=30)).strftime(
            "%Y-%m-%d %H:%M:%S"))
        expire_info = Device.objects.filter(device_expire_date__lt=date,
                                            device_expire_date__gt=now_time, is_delete=0).all()
        res = [model_to_dict(device, fields=["hostname", "device_sn",
                                             "device_ip", "device_arrived_date",
                                             "device_expire_date", "device_type"]) for device in expire_info]
        dict_['expire_info'] = res
        # 查询业务上的数量
        device_list = Business.objects.filter(is_delete=0).annotate(
            num_device=Count('device'))
        virtual_server_list = Business.objects.filter(is_delete=0).annotate(
            num_device=Count('virtualserver'))
        business_list = device_list.union(virtual_server_list, all=True)
        business_dict = dict()
        for b in business_list:
            if b.name not in business_dict:
                business_dict[b.name] = b.num_device
            else:
                business_dict[b.name] += b.num_device
        business_count = [{"name": k, "value": v} for k, v in business_dict.items()]
        dict_['business_device_count'] = business_count
        return Response(dict_)

    @action(detail=False,  methods=['GET'])
    def rack_device_info(self, request):
        rack_id = request.query_params.get("rack_id", None)
        rack_object = Rack.objects.get(id=rack_id)
        device_info = rack_object.device_set.filter(is_delete=0, device_type="服务器")
        device_res = []
        for device in device_info:
            device_vendor = ''
            if device.device_vendor:
                device_vendor = device.device_vendor.vendor_name
            device_res.append({"device_vendor": device_vendor, "device_ip": device.device_ip,
                          "operate_system": device.operate_system, "cpu_cores":device.cpu_cores,
                          "memory_capacity": device.memory_capacity,
                          "disk_capacity": device.disk_capacity, "device_type":device.device_type})
        network_info = rack_object.devicemodel_set.filter(type__in=['Switch', 'Router', 'LB', "FW"])
        network_res = []
        for network in network_info:
            if network.type == "Switch":
                device_type = "交换机"
            elif network.type == "Router":
                device_type = "路由器"
            elif network.type == "LB":
                device_type = "负载均衡"
            elif network.type == "FW":
                device_type = "防火墙"
            network_res.append({"device_vendor": network.manufacture, "device_ip": network.ipaddr,
                        "operate_system": network.operate_system, "cpu_cores": network.cpu_cores,
                        "memory_capacity": network.memory_capacity, "disk_capacity": network.disk_capacity,
                         "device_type": device_type})
        device_res.extend(network_res)
        storage_res = []
        storage_info = rack_object.storage_set.filter(is_delete=0)
        for storage in storage_info:
            storage_vendor = ''
            if storage.vendor:
                storage_vendor = storage.vendor.vendor_name
            storage_res.append({"device_vendor": storage_vendor, "device_ip": storage.manage_ip,
                                "disk_capacity": storage.disk_capacity,
                                "controller_system_version": storage.controller_system_version,
                                "controller_rack_disk_num":storage.controller_rack_disk_num,
                                "extension_rack_disk_num": storage.extension_rack_disk_num,
                                "controller_num": storage.controller_num,
                                "host_port_num": storage.host_port_num,
                                "extension_port_num": storage.extension_port_num,
                                "extension_rack_num": storage.extension_rack_num,
                                "device_type": "存储"})
        device_res.extend(storage_res)
        return Response(device_res)

    @action(detail=False, methods=['GET'])
    def device(self, request):
        query = request.query_params.get('query', None)
        device_type = request.query_params.get('device_type', '服务器')
        if query:
            device_info = Device.objects.get_queryset().filter(
                is_delete=0, device_type__contains=device_type, hostname__contains=query).order_by('-create_time')
            if not len(device_info):
                device_info = Device.objects.get_queryset().filter(
                    is_delete=0, device_type__contains=device_type, device_ip__contains=query).order_by(
                    '-create_time')
            return Response(
                    self.get_serializer(device_info, many=True).data)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def device_virtualserver(self, request):
        query = request.query_params.get('query', None)
        # device_type = request.query_params.get('device_type', '服务器')
        if query:
            device_object = Device.objects.get_queryset().filter(
                is_delete=0, device_type__contains="服务器", is_monitor="是",
                hostname__contains=query).order_by('-create_time')
            device_info = [{'hostname': device.hostname, 'ip': device.device_ip} for device in device_object]
            virtual_object = list(VirtualServer.objects.get_queryset().filter(is_monitor="是",
                is_delete=0, hostname__contains=query).order_by('-create_time'))
            virtual_info = [{'hostname': virtual.hostname, 'ip': virtual.virtual_ip} for virtual in virtual_object]
            device_info.extend(virtual_info)
            if not len(device_info):
                device_object = Device.objects.get_queryset().filter(
                    is_delete=0, device_type__contains="服务器", is_monitor="是",
                    device_ip__contains=query).order_by(
                    '-create_time')
                device_info = [
                    {'hostname': device.hostname, 'ip': device.device_ip} for
                    device in device_object]
                virtual_object = VirtualServer.objects.get_queryset().filter(is_monitor="是",
                    is_delete=0, virtual_ip__contains=query).order_by('-create_time')
                virtual_info = [
                    {'hostname': virtual.hostname, 'ip': virtual.virtual_ip}
                    for virtual in virtual_object]
                device_info.extend(virtual_info)
            return Response(device_info)
        return Response(status=status.HTTP_200_OK)


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer

    @action(detail=False, methods=['GET'])
    def networks(self, request):
        device_id = request.query_params.get('device_id', None)
        if device_id:
            device = Device.objects.get(id=device_id)
            network_info = device.network_set.all()
        storage_id = request.query_params.get('storage_id', None)
        if storage_id:
            storage = Storage.objects.get(id=storage_id)
            network_info = storage.network_set.all()
        return Response(self.get_serializer(network_info, many=True).data)

    @action(detail=False, methods=['GET'])
    def virtual_networks(self, request):
        virtual_server_id = request.query_params.get('virtual_server_id')
        virtual_server = VirtualServer.objects.get(id=virtual_server_id)
        network_info = virtual_server.network_set.all()
        return Response(self.get_serializer(network_info, many=True).data)

    @action(detail=False, methods=['GET'])
    def network_type(self, request):
        """
        查询物理服务器和虚拟服务器的内网ip数据
        :param request:
        :return:
        """
        hostname = request.query_params.get("hostname", None)
        if hostname:
            device_info = Device.objects.filter(device_type="服务器", hostname__contains=hostname).all()
        else:
            device_info = Device.objects.filter(device_type="服务器").all()
        datalist = []
        for data in device_info:
            if data.operate_system and data.operate_system != 'Windows':
                row = {}
                row['hostname'] = data.hostname
                row['network_ip'] = data.device_ip
                row['operate_system'] = data.operate_system
                row['username'] = data.manage_username
                row['password'] = data.manage_password
                row['ssh_port'] = data.ssh_port
                row['type'] = "物理机"
                datalist.append(row)
            # networks_info = data.network_set.all()
            # ip_list = []
            # for network in networks_info:
            #     if network.type == "内网":
            #         ip_list.append(network.ip)
            # row['network_ip'] = ip_list
            # if ip_list:
            #     datalist.append(row)
        if hostname:
            virtual_info = VirtualServer.objects.filter(hostname__contains=hostname).all()
        else:
            virtual_info = VirtualServer.objects.all()
        for virtual in virtual_info:
            if virtual.operate_system and virtual.operate_system != 'Windows':
                row = {}
                row['hostname'] = virtual.hostname
                row['network_ip'] = virtual.virtual_ip
                row['operate_system'] = virtual.operate_system
                row['username'] = virtual.username
                row['password'] = virtual.password
                row['ssh_port'] = virtual.ssh_port
                row['type'] = "虚拟机"
                datalist.append(row)
            # virtual_networks_info = virtual.network_set.all()
            # ip_list = []
            # for network in virtual_networks_info:
            #     if network.type == "内网":
            #         ip_list.append(network.ip)
            # row['network_ip'] = ip_list
            # if ip_list:
            #     datalist.append(row)
        return Response(datalist)


class VirtualServerViewSet(viewsets.ModelViewSet):
    queryset = VirtualServer.objects.all()
    serializer_class = VirtualServerSerializer

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        # 定义条件查询参数
        search_dict = dict()
        type = request.query_params.get('type', None)
        if type:
            search_dict['type'] = type
        hostname = request.query_params.get("hostname", None)
        if hostname:
            search_dict['hostname'] = hostname
        status = request.query_params.get("status", None)
        if status:
            search_dict['status'] = status
        virtual_ip = request.query_params.get('virtual_ip', None)
        if virtual_ip:
            search_dict['virtual_ip'] = virtual_ip
        maintain_status = request.query_params.get('maintain_status', None)
        if maintain_status:
            search_dict['maintain_status'] = maintain_status
        asset_manager = request.query_params.get('asset_manager', None)
        if asset_manager:
            search_dict['asset_manager'] = asset_manager
        search_dict['is_delete'] = 0
        server_info = VirtualServer.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(server_info, pre_page)
            result = paginator.page(current_page)
            data = self.get_serializer(result, many=True).data
            # 定义返回结果
            res = dict()
            res['total_page'] = paginator.num_pages
            res['current_page'] = current_page
            res['pre_page'] = pre_page
            res['total_count'] = paginator.count
            res['data'] = data
            return Response(res)
        else:
            return Response(self.get_serializer(server_info, many=True).data)

    def create(self, request, *args, **kwargs):
        virtual_server = VirtualServer.objects.filter(hostname=request.data.get('hostname'), is_delete=0).all()
        if len(virtual_server) == 0:
            device_network = request.data.get("network")
            belong_business_name = request.data.get("belong_business")
            business_obj = Business.objects.filter(
                name__in=belong_business_name).filter(is_delete=0).all()
            # 获得标签的id
            labels_name = request.data.get('label')
            labels_obj = Tag.objects.filter(tag_name__in=labels_name).filter(
                is_delete=0).all()

            request.data.pop("belong_business")
            request.data.pop("label")
            virtual_object = VirtualServer.objects.create(**request.data)
            for business in business_obj:
                virtual_object.belong_business.add(business)
            for label in labels_obj:
                virtual_object.label.add(label)
            list_ = []
            for network in device_network:
                netmask = network.get("netmask")
                mac = network.get('mac')
                ip = network.get('ip')
                broadcast = network.get('broadcast')
                type = network.get("type")
                if netmask or mac or ip or broadcast:
                    list_.append(Network(netmask=netmask, mac=mac, ip=ip,
                                broadcast=broadcast, virtual_server=virtual_object, type=type))
            Network.objects.bulk_create(list_)
            serializer = VirtualServerSerializer(virtual_object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            result = {'msg': '资源已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        network_info = request.data.get("network")
        virtual_server_id = request.data.get("id")
        virtual_server = VirtualServer.objects.filter(
            hostname=request.data.get('hostname'), is_delete=0).first()
        if virtual_server and virtual_server.id != virtual_server_id:
            result = {'msg': '主机名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)
        virtual_server.asset_manager_id = request.data.get('asset_manager', '')
        virtual_server.save()
        Network.objects.filter(virtual_server=virtual_server_id).delete()
        virtual_server = self.get_object()
        belong_business_name = request.data.get("belong_business")
        business_obj = Business.objects.filter(
            name__in=belong_business_name).filter(is_delete=0).all()
        # belong_business = [obj.id for obj in business_obj]
        # 获得标签的id
        labels_name = request.data.get('label')
        labels_obj = Tag.objects.filter(tag_name__in=labels_name).filter(
            is_delete=0).all()
        # labels = [obj.id for obj in labels_obj]
        VirtualServerBusiness.objects.filter(virtual_server=virtual_server_id).delete()
        VirtualServerLabel.objects.filter(virtual_server=virtual_server_id).delete()
        for business in business_obj:
            virtual_server.belong_business.add(business)
        for label in labels_obj:
            virtual_server.label.add(label)
        list_ = []
        for network in network_info:
            netmask = network.get("netmask")
            mac = network.get('mac')
            ip = network.get('ip')
            broadcast = network.get('broadcast')
            type = network.get('type')
            if netmask or mac or ip or broadcast:
                list_.append(Network(netmask=netmask, mac=mac, ip=ip,
                                 broadcast=broadcast, virtual_server=virtual_server, type=type))
        Network.objects.bulk_create(list_)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        virtual_server = self.get_object()
        business_info = VirtualServerBusiness.objects.filter(virtual_server=virtual_server)
        if len(business_info):
            result = {'msg': '该设备有关联业务，请先确定是否取消关联'}
            return Response(result)
        label_info = VirtualServerLabel.objects.filter(virtual_server=virtual_server)
        if len(label_info):
            result = {'msg': '该设备有关联标签，请先确定是否取消关联'}
            return Response(result)
        virtual_server.is_delete = 1
        virtual_server.remove_time = datetime.datetime.now()
        VirtualServerBusiness.objects.filter(virtual_server=virtual_server).delete()
        VirtualServerLabel.objects.filter(virtual_server=virtual_server).delete()
        Network.objects.filter(virtual_server=virtual_server).update(virtual_server="")
        virtual_server.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def excel(self, request):
        """ 导入Excel数据"""
        excel_obj = request.FILES.get("file", "")
        filename = excel_obj.name
        if filename and '.' in filename and filename.rsplit('.', 1)[
            1] == "xls":
            excel_data = xlrd.open_workbook(filename=None,
                                            file_contents=excel_obj.read(),
                                            formatting_info=True)
        elif filename and '.' in filename and filename.rsplit('.', 1)[
            1] == 'xlsx':
            excel_data = xlrd.open_workbook(filename=None,
                                            file_contents=excel_obj.read())
        else:
            result = {'msg': '文件格式错误'}
            return Response(result, status=status.HTTP_412_PRECONDITION_FAILED)
        table = excel_data.sheets()[0]  # 打开第一张表
        nrows = table.nrows
        list_ = []
        hostname_list = []
        for row in range(1, nrows):
            res_dict = dict()
            hostname = table.cell(row, 0).value
            chinese_res = CommonUtil.is_chinese(hostname)
            if chinese_res:
                result = {'msg': '主机名不能包含中文'}
                return Response(result, status=status.HTTP_409_CONFLICT)
            virtual_server = VirtualServer.objects.filter(
                hostname=hostname).all()
            if len(virtual_server) > 0 or hostname in hostname_list:
                return Response({'msg': hostname + ':主机名已存在或excel中有重复数据'}, status=status.HTTP_409_CONFLICT)
            hostname_list.append(hostname)
            res_dict['hostname'] = hostname
            res_dict['type'] = table.cell(row, 1).value
            res_dict['status'] = table.cell(row, 2).value
            res_dict['usage'] = table.cell(row, 3).value
            res_dict['username'] = table.cell(row, 4).value
            res_dict['password'] = table.cell(row, 5).value
            res_dict['snmp_username'] = table.cell(row, 6).value
            res_dict['snmp_password'] = table.cell(row, 7).value
            res_dict['operate_system'] = table.cell(row, 8).value
            res_dict['operate_system_version'] = table.cell(row, 9).value
            res_dict['cpu_cores'] = table.cell(row, 10).value
            res_dict['memory_capacity'] = table.cell(row, 11).value
            res_dict['disk_capacity'] = table.cell(row, 12).value
            res_dict['virtual_ip'] = table.cell(row, 13).value
            res_dict['is_monitor'] = "是"
            list_.append(VirtualServer(**res_dict))
        VirtualServer.objects.bulk_create(list_)
        result = {'msg': '插入成功'}
        return Response(result, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['PUT'])
    def update_maintain_state(self, request, pk):
        virtual_obj = self.get_object()
        virtual_obj.maintain_status = request.data.get("maintain_status", "否")
        virtual_obj.save()
        return Response(status=status.HTTP_200_OK)


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer


class StorageViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

    def create(self, request, *args, **kwargs):
        logger.info(request.data)
        # 查询是否有同名device_name
        storage_info = Storage.objects.filter(storage_name=request.data.get('storage_name'), is_delete=0).all()
        # 查询是否有同名hostname
        storage_info_hostname = Storage.objects.filter(hostname=request.data.get('hostname'), is_delete=0).all()
        if len(storage_info) == 0 and len(storage_info_hostname) == 0:
            device_network = request.data.get("network", [])
            belong_business_name = request.data.get("belong_business", [])
            business_info = Business.objects.filter(
                name__in=belong_business_name).filter(is_delete=0).all()
            if 'belong_business' in request.data.keys():
                request.data.pop("belong_business")
            # 获得标签的id
            labels_name = request.data.get('label', [])
            labels = Tag.objects.filter(tag_name__in=labels_name).filter(
                is_delete=0).all()
            if 'label' in request.data.keys():
                request.data.pop("label")
            request.data['data_center_id'] = request.data.get('data_center', '')
            request.data['location_zone_id'] = request.data.get('location_zone', '')
            request.data['location_cabinet_id'] = request.data.get('location_cabinet', '')
            request.data.pop('data_center')
            request.data.pop('location_zone')
            request.data.pop('location_cabinet')
            series = request.data.get('series', '')
            if series:
                request.data['series_id'] = series
                request.data.pop('series')
            vendor = request.data.get('vendor', None)
            if vendor:
                request.data['vendor_id'] = vendor
                request.data.pop('vendor')
            disk_vendor = request.data.get('disk_vendor', None)
            if disk_vendor:
                request.data['disk_vendor_id'] = disk_vendor
                request.data.pop('disk_vendor')
            request.data.pop('network')
            storage = Storage.objects.create(**request.data)
            for business in business_info:
                storage.belong_business.add(business)
            for label in labels:
                storage.label.add(label)
            list_ = []
            for network in device_network:
                netmask = network.get("netmask")
                mac = network.get('mac')
                ip = network.get('ip')
                broadcast = network.get('broadcast')
                type = network.get("type")
                if netmask or mac or ip or broadcast:
                    list_.append(Network(netmask=netmask, mac=mac, ip=ip,
                                     broadcast=broadcast, storage=storage, type=type))
            Network.objects.bulk_create(list_)
            serializer = StorageSerializer(storage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            result = {'msg': '主机名或设备名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        network_info = request.data.get("network", [])
        storage_id = request.data.get("id", None)
        storage_name = request.data.get('storage_name', '')
        storage_name_object = Storage.objects.filter(storage_name=storage_name, is_delete=0).first()
        if storage_name_object and storage_name_object.id != storage_id:
            result = {'msg': '设备名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)
        # 查询是否有同名hostname
        hostname = request.data.get('hostname', '')
        storage_hostname_object = Storage.objects.filter(hostname=hostname, is_delete=0).first()
        if storage_hostname_object and storage_hostname_object.id != storage_id:
            result = {'msg': '主机名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)
        storage = self.get_object()
        storage.series_id = request.data.get('series', '')
        storage.data_center_id = request.data.get('data_center', '')
        storage.location_zone_id = request.data.get('location_zone', '')
        storage.location_cabinet_id = request.data.get('location_cabinet', '')
        storage.vendor_id = request.data.get('vendor', '')
        storage.disk_vendor_id = request.data.get('disk_vendor', '')
        storage.asset_manager_id = request.data.get('asset_manager', '')
        storage.save()
        # 获得业务的名称
        belong_business_name = request.data.get("belong_business")
        business_obj = Business.objects.filter(name__in=belong_business_name).filter(is_delete=0).all()
        # 获得标签的名称
        labels_name = request.data.get('label')
        labels_obj = Tag.objects.filter(tag_name__in=labels_name).filter(is_delete=0).all()

        StorageBusiness.objects.filter(storage=storage_id).delete()
        StorageLabel.objects.filter(storage=storage_id).delete()
        for business in business_obj:
            storage.belong_business.add(business)
        for label in labels_obj:
            storage.label.add(label)
        list_ = []
        Network.objects.filter(storage=storage_id).delete()
        for network in network_info:
            netmask = network.get("netmask")
            mac = network.get('mac')
            ip = network.get('ip')
            broadcast = network.get('broadcast')
            type = network.get("type")
            if netmask or mac or ip or broadcast:
                list_.append(Network(netmask=netmask, mac=mac, ip=ip,
                                 broadcast=broadcast, storage=storage, type=type))
        Network.objects.bulk_create(list_)
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        # 定义条件查询参数
        search_dict = dict()
        is_monitor = request.query_params.get('is_monitor', None)
        if is_monitor:
            search_dict['is_monitor'] = is_monitor

        manage_address = request.query_params.get('manage_address', None)
        if manage_address:
            search_dict['manage_address__contains'] = manage_address
        storage_name = request.query_params.get("storage_name", None)
        if storage_name:
            search_dict['storage_name'] = storage_name
        hostname = request.query_params.get("hostname", None)
        if hostname:
            search_dict['hostname'] = hostname
        asset_manager = request.query_params.get("asset_manager", None)
        if asset_manager:
            search_dict['asset_manager'] = asset_manager
        vendor = request.query_params.get("vendor", None)
        if vendor:
            if vendor.isdecimal():
                search_dict['vendor_id'] = vendor
            else:
                vendor_ids = list(Vendor.objects.filter(vendor_name=vendor).values('id'))
                id_temp = [id.get('id', None) for id in vendor_ids]
                search_dict['vendor_id__in'] = id_temp
        sn = request.query_params.get("sn", None)
        if sn:
            search_dict['sn'] = sn
        search_dict['is_delete'] = 0
        storage_info = Storage.objects.get_queryset().filter(**search_dict).order_by('-update_time')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(storage_info, pre_page)
            result = paginator.page(current_page)
            data = self.get_serializer(result, many=True).data
            # 定义返回结果
            res = dict()
            res['total_page'] = paginator.num_pages
            res['current_page'] = current_page
            res['pre_page'] = pre_page
            res['total_count'] = paginator.count
            res['data'] = data
            return Response(res)
        else:
            return Response(self.get_serializer(storage_info, many=True).data)

    @action(detail=False, methods=['post'])
    def excel(self, request):
        """ 导入Excel数据，pk是所属项目的pk """
        excel_obj = request.FILES.get("file", "")
        filename = excel_obj.name
        if filename and '.' in filename and filename.rsplit('.', 1)[1] == "xls":
            excel_data = xlrd.open_workbook(filename=None, file_contents=excel_obj.read(), formatting_info=True)
        elif filename and '.' in filename and filename.rsplit('.', 1)[1] == 'xlsx':
            excel_data = xlrd.open_workbook(filename=None, file_contents=excel_obj.read())
        else:
            result = {'msg': '文件格式错误'}
            return Response(result, status=status.HTTP_412_PRECONDITION_FAILED)
        table = excel_data.sheets()[0]  # 打开第一张表
        nrows = table.nrows
        list_ = []
        storage_name_list = []
        hostname_list = []
        for row in range(1, nrows):
            res_dict = dict()
            storage_name = table.cell(row, 0).value
            chinese_res = CommonUtil.is_chinese(storage_name)
            if chinese_res:
                result = {'msg': '存储名称不能包含中文'}
                return Response(result, status=status.HTTP_409_CONFLICT)
            storage_info = Storage.objects.filter(
                storage_name=storage_name, is_delete=0).all()
            if len(storage_info) > 0 or storage_name in storage_name_list:
                result = {'msg': '存储:' + storage_name + ',已存在或excel中有重复数据'}
                return Response(result, status=status.HTTP_409_CONFLICT)
            storage_name_list.append(storage_name)
            res_dict['storage_name'] = storage_name
            hostname = table.cell(row, 1).value
            chinese_res = CommonUtil.is_chinese(hostname)
            if chinese_res:
                result = {'msg': '主机名不能包含中文'}
                return Response(result, status=status.HTTP_409_CONFLICT)
            storage_info = Storage.objects.filter(
                hostname=hostname, is_delete=0).all()
            if len(storage_info) > 0 or hostname in hostname_list:
                result = {'msg': '主机名:' + hostname + ',已存在或excel中有重复数据'}
                return Response(result, status=status.HTTP_409_CONFLICT)
            hostname_list.append(hostname)
            res_dict['hostname'] = hostname
            res_dict['sn'] = table.cell(row, 2).value
            res_dict['storage_model'] = table.cell(row, 3).value
            res_dict['manage_address'] = table.cell(row, 4).value
            res_dict['manage_username'] = table.cell(row, 5).value
            res_dict['manage_password'] = table.cell(row, 6).value
            res_dict['storage_start_unit'] = table.cell(row, 7).value
            res_dict['storage_unit'] = table.cell(row, 8).value
            res_dict['usage'] = table.cell(row, 9).value
            res_dict['disk_model'] = table.cell(row, 10).value
            res_dict['disk_capacity'] = table.cell(row, 11).value
            res_dict['controller_num'] = table.cell(row, 12).value
            res_dict['controller_system_version'] = table.cell(row, 13).value
            res_dict['host_port_type'] = table.cell(row, 14).value
            res_dict['host_port_num'] = table.cell(row, 15).value
            res_dict['extension_port_type'] = table.cell(row, 16).value
            res_dict['extension_port_num'] = table.cell(row, 17).value
            res_dict['extension_rack_type'] = table.cell(row, 18).value
            res_dict['extension_rack_num'] = table.cell(row, 19).value
            res_dict['controller_rack_disk_num'] = table.cell(row, 20).value
            res_dict['extension_rack_disk_num'] = table.cell(row, 21).value
            arrived_date = table.cell(row, 22).value
            expire_date = table.cell(row, 23).value
            arrived_ctype = table.cell(row, 22).ctype

            if arrived_ctype == 3:
                arrived_value = datetime.datetime(
                    *xlrd.xldate_as_tuple(arrived_date, 0))
                arrived_date = arrived_value.strftime('%Y-%d-%m')
            res_dict['arrived_date'] = arrived_date
            expire_ctype = table.cell(row, 23).ctype
            if expire_ctype == 3:
                expire_value = datetime.datetime(*xlrd.xldate_as_tuple(expire_date, 0))
                expire_date = expire_value.strftime('%Y-%d-%m')
            res_dict['expire_date'] = expire_date
            res_dict['is_monitor'] = "是"
            list_.append(Storage(**res_dict))
        Storage.objects.bulk_create(list_)
        result = {'msg': '插入成功'}
        return Response(result, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        storage = self.get_object()
        business_info = StorageBusiness.objects.filter(storage=storage).all()
        if len(business_info):
            result = {'msg': '该设备有关联业务，请先确定是否取消关联'}
            return Response(result)
        label_info = StorageLabel.objects.filter(storage=storage).all()
        if len(label_info):
            result = {'msg': '该设备有关联标签，请先确定是否取消关联'}
            return Response(result)
        storage.is_delete = 1
        storage.remove_time = datetime.datetime.now()
        StorageBusiness.objects.filter(storage=storage).all().delete()
        StorageLabel.objects.filter(storage=storage).all().delete()
        Network.objects.filter(storage=storage).update(storage="")
        storage.series_id = ''
        storage.data_center_id = ''
        storage.location_cabinet_id = ''
        storage.location_zone_id = ''
        storage.vendor_id = ''
        storage.disk_vendor_id = ''
        storage.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def storage(self, request):
        search_dict = dict()
        query = request.query_params.get('query', None)
        vendor = request.query_params.get('vendor', None)
        is_monitor = request.query_params.get('is_monitor', None)
        if vendor:
            vendor_info = Vendor.objects.filter(vendor_name=vendor).first()
            vendor_id = vendor_info.id if vendor_info else None
            search_dict['vendor_id'] = vendor_id
        if is_monitor:
            search_dict['is_monitor'] = is_monitor
        search_dict['is_delete'] = 0
        if query:
            search_dict['hostname__contains'] = query
            storage_info = Storage.objects.get_queryset().filter(**search_dict).order_by('-create_time')
            if not len(storage_info):
                search_dict['manage_ip__contains'] = search_dict.pop('hostname__contains')
                storage_info = Storage.objects.get_queryset().filter(**search_dict).order_by('-create_time')
            return Response(
                self.get_serializer(storage_info, many=True).data)
        return Response(status=status.HTTP_200_OK)
