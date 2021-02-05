import logging
from datetime import datetime
from django.core.paginator import Paginator
from django.forms import model_to_dict
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from data_center.models import Datacenter, Room, Rack
from data_center.serializers import DatacenterSerializer, RoomSerializer, RackSerializer
from auth.views import MyAuthentication


logger = logging.getLogger('log')


class DatacenterViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Datacenter.objects.all()
    serializer_class = DatacenterSerializer

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
        dc_address = request.query_params.get('dc_address')
        if dc_address:
            search_dict['dc_address'] = dc_address
        dc_name = request.query_params.get('dc_name')
        if dc_name:
            search_dict['dc_name'] = dc_name
        search_dict['is_delete'] = 0

        # 查询数据
        dc_list = Datacenter.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(dc_list, pre_page)
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
            return Response(self.get_serializer(dc_list, many=True).data)

    def create(self, request, *args, **kwargs):
        datacenter_info = Datacenter.objects.filter(dc_name=request.data.get('dc_name'), is_delete=0).all()
        if len(datacenter_info) == 0:
            datacenter = Datacenter()
            if 'dc_name' in request.data.keys():
                datacenter.dc_name = request.data['dc_name']
            if 'dc_address' in request.data.keys():
                datacenter.dc_address = request.data['dc_address']
            if 'remark' in request.data.keys():
                datacenter.remark = request.data['remark']
            datacenter.create_time = datetime.now()
            datacenter.update_time = datetime.now()
            datacenter.save()
            result = model_to_dict(datacenter)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            result = {'msg': '资源已存在'}
            return Response(data=result, status=status.HTTP_205_RESET_CONTENT)

    def update(self, request, *args, **kwargs):
        datacenter_info = Datacenter.objects.filter(dc_name=request.data.get('dc_name'), is_delete=0).first()
        # datacenter = Datacenter()
        # 数据库中不存在同名的数据中心
        dc_id = int(kwargs['pk'])
        # 数据库中不存在同名的数据中心
        if datacenter_info and datacenter_info.id != dc_id:
            result = '{"msg":"资源已存在"}'
            return Response(data=result, status=status.HTTP_409_CONFLICT)
        datacenter = Datacenter.objects.filter(id=dc_id).first()
        datacenter.update_time = datetime.now()
        datacenter.save()
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        datacenter = self.get_object()
        network = datacenter.devicemodel_set.all()
        if len(network):
            return Response({'msg': "该数据中心下有关联网络设备"})
        device = datacenter.device_set.all()
        if len(device):
            return Response({'msg': "该数据中心下有关联服务器"})
        storage = datacenter.storage_set.all()
        if len(storage):
            return Response({'msg': '该数据中心下有关联存储设备'})
        datacenter.is_delete = 1
        datacenter.remove_time = datetime.now()
        datacenter.save()
        dc_id = datacenter.id
        room_info = Room.objects.filter(datacenter_id=dc_id).all()
        for room in room_info:
            room.datacenter = None
            room.save()
        result = model_to_dict(datacenter)
        return Response(result, status=status.HTTP_200_OK)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

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
        room_name = request.query_params.get('room_name')
        if room_name:
            search_dict['room_name'] = room_name
        room_address = request.query_params.get('room_address')
        if room_address:
            search_dict['room_address'] = room_address
        # dc_id = request.query_params.get('dc_id')
        # if dc_id:
            # datacenter = Datacenter.objects.filter(dc_name=dc_name).first()
            # if datacenter:
            #     datacenter_id = datacenter.id
            # search_dict['datacenter_id'] = dc_id
            # else:
            #     return Response(status=status.HTTP_204_NO_CONTENT)
        search_dict['is_delete'] = 0
        dc_name = request.query_params.get('dc_name')
        if dc_name:
            datacenter = Datacenter.objects.filter(dc_name=dc_name).first()
            search_dict['datacenter_id'] = datacenter.id
        # 查询数据
        dc_list = Room.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(dc_list, pre_page)
            result = paginator.page(current_page)
            data = self.get_serializer(result, many=True).data
            # 定义返回结果
            res = dict()
            res['total_page'] = paginator.num_pages
            res['current_page'] = current_page
            res['pre_page'] = pre_page
            res['total_count'] = paginator.count
            res['data'] = data
            for one_data in data:
                if 'datacenter' in one_data.keys() and one_data['datacenter'] != None:
                    one_data['dc_name'] = one_data['datacenter']['dc_name']
            return Response(res)
        else:
            return Response(self.get_serializer(dc_list, many=True).data)

    @action(detail=False, methods=['GET'])
    def room(self, request):
        dc_id = request.query_params.get('id')
        if dc_id:
            dc = Datacenter.objects.filter(id=dc_id).first()
            room_info = dc.room_set.all()
            return Response(self.get_serializer(room_info, many=True).data)
        dc_name = request.query_params.get("dc_name")
        if dc_name:
            dc = Datacenter.objects.filter(dc_name=dc_name).first()
            room_info = dc.room_set.all()
            return Response(self.get_serializer(room_info, many=True).data)
        else:
            result = {'msg': '缺少参数'}
            return Response(data=result, status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 查询是否有同名的机房
        room_info = Room.objects.filter(room_name=request.data.get('room_name'), is_delete=0).all()
        if len(room_info) == 0:
            room = Room()
            room.room_name = request.data['room_name']
            if 'remark' in request.data.keys():
                room.remark = request.data['remark']
            if 'room_address' in request.data.keys():
                room.room_address = request.data['room_address']
            if 'datacenter_id' in request.data.keys():
                datacenter_id = request.data['datacenter_id']
                datacenter = Datacenter.objects.filter(id=datacenter_id).first()
                room.datacenter = datacenter
            room.create_time = datetime.now()
            room.update_time =datetime.now()
            room.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            result = {"msg": "资源已存在"}
            return Response(data=result, status = status.HTTP_205_RESET_CONTENT)

    def update(self, request, *args, **kwargs):
        logger.info(request.data)
        room_info = Room.objects.filter(room_name=request.data.get('room_name'), is_delete=0).first()
        room_id = int(kwargs['pk'])
        # 数据库中不存在同名的数据中心
        if room_info and room_info.id != room_id:
            result = '{"msg":"资源已存在"}'
            return Response(data=result, status=status.HTTP_409_CONFLICT)
        room = Room.objects.filter(id=room_id).first()
        room.room_name = request.data.get('room_name')
        datacenter_id = request.data.get('datacenter_id')
        remark = request.data.get('remark')
        room_address = request.data.get('room_address')
        if datacenter_id:
            room.datacenter_id = datacenter_id
        if remark:
            room.remark = remark
        if room_address:
            room.room_address = room_address
        room.update_time = datetime.now()
        room.save()
        room = model_to_dict(room)
        return Response(room, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        room = self.get_object()
        device = room.device_set.all()
        if len(device):
            return Response({'msg': "该机房下有关联设备"})
        room.is_delete = True
        room.remove_time = datetime.now()
        room.datacenter = None
        room.save()
        room_id = room.id
        rack_info = Rack.objects.filter(room_id=room_id).all()
        for rack in rack_info:
            rack.room = None
            rack.save()
        result = model_to_dict(room)
        return Response(result, status=status.HTTP_200_OK)


class RackViewSet(viewsets.ModelViewSet):
    queryset = Rack.objects.all()
    serializer_class = RackSerializer

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
        id = request.query_params.get('id')
        if id:
            search_dict['id'] = id
        rack_name = request.query_params.get('rack_name')
        if rack_name:
            search_dict['rack_name'] = rack_name
        rack_address = request.query_params.get('rack_address')
        if rack_address:
            search_dict['rack_address'] = rack_address
        room_name = request.query_params.get('room_name')
        if room_name:
            room = Room.objects.filter(room_name=room_name).first()
            if room:
                room_id = room.id
                search_dict['room_id'] = room_id
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        search_dict['is_delete'] = 0

        # 查询数据
        rack_list = Rack.objects.get_queryset().filter(**search_dict).order_by('-create_time','-id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(rack_list, pre_page)
            result = paginator.page(current_page)
            data = self.get_serializer(result, many=True).data
            # 定义返回结果
            res = dict()
            res['total_page'] = paginator.num_pages
            res['current_page'] = current_page
            res['pre_page'] = pre_page
            res['total_count'] = paginator.count
            res['data'] = data
            for one_data in data:
                one_data['room_name'] = None
                one_data['dc_name'] = None
                if one_data['room']:
                    one_data['room_name'] = one_data['room']['room_name']
                    if one_data['room']['datacenter']:
                        one_data['dc_name'] = one_data['room']['datacenter']['dc_name']
            return Response(res)
        else:
            return Response(self.get_serializer(rack_list, many=True).data)

    @action(detail=False, methods=['GET'])
    def rack(self, request):
        room_id = request.query_params.get('room_id')
        if room_id:
            room = Room.objects.filter(id=room_id).first()
            rack_info = room.rack_set.all()
            return Response(self.get_serializer(rack_info, many=True).data)
        room_name = request.query_params.get("room_name")
        if room_name:
            room = Room.objects.filter(room_name=room_name).first()
            rack_info = room.rack_set.all()
            return Response(self.get_serializer(rack_info, many=True).data)
        else:
            result = {'msg': '缺少参数'}
            return Response(data=result, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        rack = self.get_object()
        device = rack.device_set.all()
        if len(device):
            return Response({'msg': "该机柜下有关联设备"})
        rack.is_delete = True
        rack.remove_time = datetime.now()
        rack.room = None
        rack.save()
        result = model_to_dict(rack)
        return Response(result, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 查询是否有同名的机房
        rack_info = Rack.objects.filter(rack_name=request.data.get('rack_name'), is_delete=0).all()
        if len(rack_info) == 0:
            rack = Rack()
            rack.rack_name = request.data['rack_name']
            if 'rack_address' in request.data.keys():
                rack.rack_address = request.data['rack_address']
            if 'remark' in request.data.keys():
                rack.remark = request.data['remark']
            if 'room_name' in request.data.keys():
                room_name = request.data['room_name']
                room = Room.objects.filter(room_name=room_name).first()
                rack.room = room
            rack.create_time = datetime.now()
            rack.update_time = datetime.now()
            rack.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            result = {'msg': '资源已存在'}
            return Response(data=result, status=status.HTTP_205_RESET_CONTENT)

    def update(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 查询是否有同名的机房
        logger.info(request.data)
        rack_info = Rack.objects.filter(rack_name=request.data.get('rack_name'), is_delete=0).first()
        rack_id = int(kwargs['pk'])
        # 数据库中不存在同名的数据中心
        if rack_info and rack_info.id != rack_id:
            result = '{"msg":"资源已存在"}'
            return Response(data=result, status=status.HTTP_409_CONFLICT)
        rack_obj = Rack.objects.filter(id=rack_id, is_delete=0).first()
        room_name = request.data.get('room_name', None)
        if rack_obj:
            if room_name:
                room = Room.objects.filter(room_name=room_name).first()
                rack_obj.room = room
            rack_obj.update_time = datetime.now()
            rack_obj.save()
        return super().update(request, *args, **kwargs)
