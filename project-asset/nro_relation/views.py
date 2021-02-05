import uuid
import random
from rest_framework import viewsets, status
from django.core.paginator import Paginator
from rest_framework.decorators import action
from rest_framework.response import Response

from logic_resource.models import Business
from nro_relation.models import DeviceModel, DeviceModelLabel, DeviceModelBusiness
from nro_relation.serializers import DeviceModelSerializer
from tag.models import Tag


class DeviceViewSet2(viewsets.ModelViewSet):
    queryset = DeviceModel.objects.all()
    serializer_class = DeviceModelSerializer

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
        type_ = request.query_params.get('type')
        name = request.query_params.get('name')
        ipaddr = request.query_params.get('ipaddr')
        is_monitor = request.query_params.get('is_monitor')
        if is_monitor:
            search_dict['is_monitor'] = is_monitor
        if name:
            search_dict['name'] = name
        if ipaddr:
            search_dict['ipaddr'] = ipaddr
        asset_manager = request.query_params.get("asset_manager", None)
        if asset_manager:
            search_dict['asset_manager'] = asset_manager
        # search_dict['is_delete'] = 0
        if type_:
            type_ = type_.split(',')
            device_list = DeviceModel.objects.get_queryset().filter(type__in=type_, **search_dict).order_by(
                "-createtime")
        else:
            device_list = DeviceModel.objects.get_queryset().filter(**search_dict).order_by('-createtime')
        # 查询数据

        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(device_list, pre_page)
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
            return Response(self.get_serializer(device_list, many=True).data)

    def create(self, request, *args, **kwargs):
        # 查询是否有同名device_name
        device_info = DeviceModel.objects.filter(name=request.data.get('name')).all()
        if len(device_info) == 0:
            request.data['id'] = str(uuid.uuid4())
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
            request.data['random_id'] = random.randint(1, 20)
            device = DeviceModel.objects.create(**request.data)
            for business in business_info:
                device.belong_business.add(business)
            for label in labels:
                device.label.add(label)
            serializer = DeviceModelSerializer(device)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            result = {'msg': '主机名或设备名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        # 查询是否有同名device_name
        device_id = request.data.get("id", None)
        device_name = request.data.get('name', '')
        device_name_object = DeviceModel.objects.filter(name=device_name).first()
        if device_name_object and device_name_object.id != device_id:
            result = {'msg': '设备名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)
        device = self.get_object()
        device.series_id = request.data.get('series', '')
        device.data_center_id = request.data.get('data_center', '')
        device.location_zone_id = request.data.get('location_zone', '')
        device.location_cabinet_id = request.data.get('location_cabinet', '')
        device.asset_manager_id = request.data.get('asset_manager', '')
        device.save()
        # 获得业务的名称
        belong_business_name = request.data.get("belong_business")
        business_obj = Business.objects.filter(name__in=belong_business_name).filter(is_delete=0).all()
        # 获得标签的名称
        labels_name = request.data.get('label')
        labels_obj = Tag.objects.filter(tag_name__in=labels_name).filter(is_delete=0).all()

        DeviceModelBusiness.objects.filter(network_id=device_id).delete()
        DeviceModelLabel.objects.filter(network_id=device_id).delete()
        for business in business_obj:
            device.belong_business.add(business)
        for label in labels_obj:
            device.label.add(label)
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def network(self, request):
        query = request.query_params.get('query', None)
        device_type = request.query_params.get('device_type', None)
        is_monitor = request.query_params.get('is_monitor', None)
        if query:
            device_info = DeviceModel.objects.get_queryset().filter(
             type=device_type, is_monitor=is_monitor, hostname__contains=query).order_by('-createtime')
            if not len(device_info):
                device_info = DeviceModel.objects.get_queryset().filter(
                type=device_type, is_monitor=is_monitor, ipaddr__contains=query).order_by(
                    '-createtime')
        else:
            device_info = DeviceModel.objects.get_queryset().filter(type=device_type).order_by('-createtime')
        return Response(
                self.get_serializer(device_info, many=True).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PUT"])
    def delete(self, request, *args, **kwargs):
        id = kwargs['pk']
        datacenter = DeviceModel.objects.filter(id=id).first()
        if datacenter.data_center:
            return Response({'msg': "该网络设备绑定了数据中心"})
        business = DeviceModelBusiness.objects.filter(network_id=id).all()
        if len(business):
            return Response({'msg': "该网络设备绑定了业务"})
        tag = DeviceModelLabel.objects.filter(network_id=id).all()
        if len(tag):
            return Response({'msg': "该网络设备绑定了标签"})
        result = DeviceModel.objects.filter(id=id).delete()
        return Response(data=result, status=status.HTTP_204_NO_CONTENT)