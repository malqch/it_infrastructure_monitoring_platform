import json
import logging
from datetime import datetime

from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.decorators import action

from django.core.paginator import Paginator
from rest_framework.response import Response
from asset_relation.models import Tag, Staff, Business, Device, DeviceLabel, DeviceBusiness, VirtualServerLabel, \
    VirtualServer, VirtualServerBusiness, DeviceModelLabel, DeviceModelBusiness, DeviceModel, Storage, StorageLabel, StorageBusiness
from asset_relation.serializers import TagSerializer, DeviceSerializer, StaffSerializer, BusinessSerializer, \
    DeviceModelSerializer, VirtualServerSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class DeviceModelViewSet(viewsets.ModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer


class VirtualServerViewSet(viewsets.ModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = VirtualServerSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def format_tag(device_type, device, device_dict):
        if device_type == '服务器':
            tag = "SERVER_" + device.device_ip + '_' + device.hostname
        elif device_type == 'FW':
            if device.hostname:
                tag = "FIREWALL_" + device.ipaddr + '_' + device.hostname
            else:
                tag = "FIREWALL_" + device.ipaddr + '_' + device.name
        elif device_type == "Router":
            if device.hostname:
                tag = "ROUTER_" + device.ipaddr + '_' + device.hostname
            else:
                tag = "ROUTER_" + device.ipaddr + '_' + device.name

        elif device_type == "LB":
            if device.hostname:
                tag = "LOADBALANCE_" + device.ipaddr + '_' + device.hostname
            else:
                tag = "LOADBALANCE_" + device.ipaddr + '_' + device.name
        elif device_type == "Switch":
            if device.hostname:
                tag = "SWITCH_" + device.ipaddr + '_' + device.hostname
            else:
                tag = "SWITCH_" + device.ipaddr + '_' + device.name
        elif device_type == '虚拟服务器':
            tag = "SERVER_" + device.virtual_ip + '_' + device.hostname
        elif device_type == '存储':
            tag = "STORAGE_" + device.manage_ip
        else:
            tag = None
        device_dict['tag'] = tag
        if device_type == '虚拟服务器':
            device_dict['device_ip'] = device.virtual_ip
            device_dict['device_name'] = device.hostname
        elif device_type == '服务器':
            device_name = device.device_name
            device_dict['device_name'] = device_name
            device_dict['device_ip'] = device.device_ip
        elif device_type == '存储':
            device_name = device.storage_name
            device_dict['device_name'] = device_name
            device_dict['device_ip'] = device.manage_ip
        else:
            device_name = device.name
            device_dict['device_name'] = device_name
            device_dict['device_ip'] = device.ipaddr
        return device_dict

    @action(methods=['get'], detail=False, url_path='device_info')
    def get_device_info(self, request):
        device_type = request.query_params.get('device_type')
        tag_id = request.query_params.get('tag_id', None)
        business_id = request.query_params.get('business_id', None)
        if device_type and tag_id and business_id:
            if device_type != '虚拟服务器':
                if device_type == '服务器':
                    tag_device = DeviceLabel.objects.filter(label_id=tag_id).all()
                    business_device = DeviceBusiness.objects.filter(business_id=business_id).all()
                elif device_type == '存储':
                    tag_device = StorageLabel.objects.filter(label_id=tag_id).all()
                    business_device = StorageBusiness.objects.filter(business_id=business_id).all()
                else:
                    tag_device = DeviceModelLabel.objects.filter(label_id=tag_id).all()
                    business_device = DeviceModelBusiness.objects.filter(business_id=business_id).all()

            else:
                tag_device = VirtualServerLabel.objects.filter(label_id=tag_id).all()
                business_device = VirtualServerBusiness.objects.filter(business_id=business_id).all()
            device_id_list = []
            if tag_device and business_device:
                device_id_list1 = []
                for tag in tag_device:
                    if device_type == '虚拟服务器':
                        device_id = tag.virtual_server_id
                    elif device_type == '服务器':
                        device_id = tag.device_id
                    elif device_type == '存储':
                        device_id = tag.storage_id
                    else:
                        device_id = tag.network_id
                    device_id_list1.append(device_id)
                device_id_list2 = []
                for business in business_device:
                    if device_type == '虚拟服务器':
                        device_id = business.virtual_server_id
                    elif device_type == '服务器':
                        device_id = business.device_id
                    elif device_type == '存储':
                        device_id = business.storage_id
                    else:
                        device_id = business.network_id
                    device_id_list2.append(device_id)
                device_id_list1 = set(device_id_list1)
                device_id_list2 = set(device_id_list2)
                device_id_list = list(device_id_list1.intersection(device_id_list2))
            device_info = []
            if device_id_list:
                for device_id in device_id_list:
                    device_dict = {}
                    device_status = '使用'
                    if device_type == '虚拟服务器':
                        device = VirtualServer.objects.filter(id=device_id,
                                                              status=device_status).first()
                    elif device_type == '服务器':
                        device = Device.objects.filter(device_type=device_type, id=device_id,
                                                       device_status=device_status).first()
                    elif device_type == '存储':
                        device = Storage.objects.filter(id=device_id, is_delete=0).first()
                        print(444444)
                    else:
                        if device_type == '交换机':
                            device_type = 'Switch'
                        elif device_type == '防火墙':
                            device_type = 'FW'
                        elif device_type == '路由器':
                            device_type = 'Router'
                        elif device_type == '负载均衡':
                            device_type = 'LB'
                        else:
                            pass
                        device = DeviceModel.objects.filter(type=device_type, id=device_id).first()
                    if device:
                        device_dict = DeviceViewSet.format_tag(device_type, device, device_dict)
                        device_info.append(device_dict)
            return Response(data=device_info, status=status.HTTP_200_OK)

        elif device_type and not tag_id and business_id:
            if device_type == '虚拟服务器':
                business_device = VirtualServerBusiness.objects.filter(business_id=business_id).all()
            elif device_type == '服务器':
                business_device = DeviceBusiness.objects.filter(business_id=business_id).all()
            elif device_type == '存储':
                business_device = StorageBusiness.objects.filter(business_id=business_id).all()
            else:
                business_device = DeviceModelBusiness.objects.filter(business_id=business_id).all()
            device_info = []
            if business_device:
                device_id_list = []
                for business in business_device:
                    if device_type == '虚拟服务器':
                        device_id = business.virtual_server_id
                    elif device_type == '服务器':
                        device_id = business.device_id
                    elif device_type == '存储':
                        device_id = business.storage_id
                    else:
                        device_id = business.network_id
                    device_id_list.append(device_id)
                if device_id_list:
                    for device_id in device_id_list:
                        device_dict = {}
                        device_status = '使用'
                        if device_type == '虚拟服务器':
                            device = VirtualServer.objects.filter(id=device_id,
                                                                  status=device_status).first()
                        elif device_type == '服务器':
                            device = Device.objects.filter(device_type=device_type, id=device_id,
                                                        device_status=device_status).first()
                        elif device_type == '存储':
                            device = Storage.objects.filter(id=device_id, is_delete=0).first()
                        else:
                            if device_type == '交换机':
                                device_type = 'Switch'
                            elif device_type == '防火墙':
                                device_type = 'FW'
                            elif device_type == '路由器':
                                device_type = 'Router'
                            elif device_type == '负载均衡':
                                device_type = 'LB'
                            else:
                                pass
                            device = DeviceModel.objects.filter(type=device_type, id=device_id,
                                                                status=0).first()
                        if device:
                            device_dict = DeviceViewSet.format_tag(device_type, device, device_dict)
                            device_info.append(device_dict)
            return Response(data=device_info, status=status.HTTP_200_OK)
        elif device_type and tag_id and not business_id:
            if device_type == '虚拟服务器':
                tag_device = VirtualServerLabel.objects.filter(label_id=tag_id).all()
            elif device_type == '服务器':
                tag_device = DeviceLabel.objects.filter(label_id=tag_id).all()
            elif device_type == '存储':
                tag_device = StorageLabel.objects.filter(label_id=tag_id).all()
                print(3333)
            else:
                tag_device = DeviceModelLabel.objects.filter(label_id=tag_id).all()
            device_info = []
            if tag_device:
                device_id_list = []
                for tag in tag_device:
                    if device_type == '虚拟服务器':
                        device_id = tag.virtual_server_id
                    elif device_type == '服务器':
                        device_id = tag.device_id
                    elif device_type == '存储':
                        device_id = tag.storage_id
                    else:
                        device_id = tag.network_id
                    device_id_list.append(device_id)
                if device_id_list:
                    for device_id in device_id_list:
                        device_dict = {}
                        device_status = '使用'
                        if device_type == '虚拟服务器':
                            device = VirtualServer.objects.filter(id=device_id, status=device_status).first()
                        elif device_type == '服务器':
                            device = Device.objects.filter(device_type=device_type, id=device_id,
                                                           device_status=device_status).first()
                        elif device_type == '存储':
                            device = Storage.objects.filter(id=device_id, is_delete=0).first()
                            print(22222)
                        else:
                            if device_type == '交换机':
                                device_type = 'Switch'
                            elif device_type == '防火墙':
                                device_type = 'FW'
                            elif device_type == '路由器':
                                device_type = 'Router'
                            elif device_type == '负载均衡':
                                device_type = 'LB'
                            else:
                                pass
                            device = DeviceModel.objects.filter(type=device_type, id=device_id).first()
                        if device:
                            one_device_dict = DeviceViewSet.format_tag(device_type, device, device_dict)
                            device_info.append(one_device_dict)
            return Response(data=device_info, status=status.HTTP_200_OK)
        elif device_type and not tag_id and not business_id:
            if device_type == '虚拟服务器':
                device_info = VirtualServer.objects.filter(is_delete=0).all()
            elif device_type == '服务器':
                device_info = Device.objects.filter(device_type=device_type, is_delete=0).all()
            elif device_type == '存储':
                device_info = Storage.objects.filter(is_delete=0).all()
                print(111111)
            else:
                if device_type == '交换机':
                    device_type = 'Switch'
                elif device_type == '防火墙':
                    device_type = 'FW'
                elif device_type == '路由器':
                    device_type = 'Router'
                elif device_type == '负载均衡':
                    device_type = 'LB'
                else:
                    pass
                device_info = DeviceModel.objects.filter(type=device_type, status=0).all()
            device_list = []
            if device_info:
                for device in device_info:
                    device_dict = {}
                    device_dict = DeviceViewSet.format_tag(device_type, device, device_dict)
                    device_list.append(device_dict)
            return Response(data=device_list, status=status.HTTP_200_OK)
        else:
            return Response(data=None, status=status.HTTP_200_OK)



