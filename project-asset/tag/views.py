import logging
from datetime import datetime

from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.decorators import action

from auth.views import MyAuthentication
from django.core.paginator import Paginator
from rest_framework.response import Response
from tag.models import Tag
from tag.serializers import TagSerializer

logger = logging.getLogger('log')


class TagViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

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
        tag_name = request.query_params.get('tag_name')
        is_delete = request.query_params.get('is_delete')
        if tag_name:
            search_dict['tag_name'] = tag_name
        search_dict['is_delete'] = 0
        # 查询数据
        tag_list = Tag.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(tag_list, pre_page)
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
            return Response(self.get_serializer(tag_list, many=True).data)

    def create(self, request, *args, **kwargs):
        tag_info = Tag.objects.filter(tag_name=request.data.get('tag_name'), is_delete=0).all()
        if len(tag_info) == 0:
            tag = Tag()
            if 'tag_name' in request.data.keys():
                tag.tag_name = request.data['tag_name']
            if 'tag_remark' in request.data.keys():
                tag.tag_remark = request.data['tag_remark']
            tag.create_time = datetime.now()
            tag.update_time = datetime.now()
            tag.save()
            result = model_to_dict(tag)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            result = {'msg': '标签名称已存在'}
            return Response(data=result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        logger.info(request.data)
        tag_info = Tag.objects.filter(tag_name=request.data.get('tag_name'), is_delete=0).first()
        tag_id = int(kwargs['pk'])
        # 数据库中不存在同名的数据中心
        if tag_info and tag_info.id != tag_id:
            result = '{"msg":"资源已存在"}'
            return Response(data=result, status=status.HTTP_409_CONFLICT)
        tag = Tag.objects.filter(id=tag_id).first()
        tag.update_time = datetime.now()
        tag.save()
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['POST'])
    def devicetag(self, request):
        label = request.data.get("label")
        tag = Tag.objects.get_queryset().filter(id__in=label, is_delete=0)
        return Response(self.get_serializer(tag, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        tag = self.get_object()
        device = tag.device_set.all()
        if len(device):
            return Response({'msg': "该标签下有关联服务器"}, status=status.HTTP_409_CONFLICT)
        virtual = tag.virtualserver_set.all()
        if len(virtual):
            return Response({'msg': "该标签下有关联虚拟服务器"}, status=status.HTTP_409_CONFLICT)
        network = tag.devicemodel_set.all()
        if len(network):
            return Response({'msg': '该标签下有关联网络设备'}, status=status.HTTP_409_CONFLICT)
        storage = tag.storage_set.all()
        if len(storage):
            return Response({'msg': '该标签下有关联存储设备'}, status=status.HTTP_409_CONFLICT)
        tag.is_delete = True
        tag.remove_time = datetime.now()
        tag.save()
        result = model_to_dict(tag)
        return Response(result, status=status.HTTP_200_OK)
