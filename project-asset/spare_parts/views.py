import logging
from datetime import datetime

from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.decorators import action

from auth.views import MyAuthentication
from django.core.paginator import Paginator
from rest_framework.response import Response
from spare_parts.models import Disk, Hba, Hca, Nic, Ssd
from spare_parts.serializers import DiskSerializer, HbaSerializer, HcaSerializer, NicSerializer, SsdSerializer

logger = logging.getLogger('log')


class DiskViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer

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
        disk_status = request.query_params.get('disk_status')
        disk_sn = request.query_params.get('disk_sn')
        disk_vendor = request.query_params.get('disk_vendor')
        disk_host = request.query_params.get('disk_host')
        if disk_status:
            search_dict['disk_status'] = disk_status
        if disk_sn:
            search_dict['disk_sn'] = disk_sn
        if disk_vendor:
            search_dict['disk_vendor'] = disk_vendor

        search_dict['is_delete'] = 0
        # 查询数据
        disk_list = Disk.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        if disk_host:
            disk_list = Disk.objects.get_queryset().filter(disk_host__contains=disk_host, **search_dict).order_by('-create_time')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(disk_list, pre_page)
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
            return Response(self.get_serializer(disk_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        disk = Disk.objects.get(id=id)
        disk.is_delete = True
        disk.remove_time = datetime.now()
        disk.save()
        result = model_to_dict(disk)
        return Response(result, status=status.HTTP_200_OK)


class HbaViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Hba.objects.all()
    serializer_class = HbaSerializer

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
        hba_status = request.query_params.get('hba_status')
        hba_sn = request.query_params.get('hba_sn')
        hba_vendor = request.query_params.get('hba_vendor')
        hba_host = request.query_params.get('hba_host')
        if hba_status:
            search_dict['hba_status'] = hba_status
        if hba_sn:
            search_dict['hba_sn'] = hba_sn
        if hba_vendor:
            search_dict['hba_vendor'] = hba_vendor
        search_dict['is_delete'] = 0

        # 查询数据
        hba_list = Hba.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        if hba_host:
            hba_list = Hba.objects.get_queryset().filter(hba_host__contains=hba_host, **search_dict).order_by(
                '-create_time')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(hba_list, pre_page)
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
            return Response(self.get_serializer(hba_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        hba = Hba.objects.get(id=id)
        hba.is_delete = True
        hba.remove_time = datetime.now()
        hba.save()
        result = model_to_dict(hba)
        return Response(result, status=status.HTTP_200_OK)


class HcaViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Hca.objects.all()
    serializer_class = HcaSerializer

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
        hca_status = request.query_params.get('hca_status')
        hca_sn = request.query_params.get('hca_sn')
        hca_vendor = request.query_params.get('hca_vendor')
        hca_host = request.query_params.get('hca_host')
        if hca_status:
            search_dict['hca_status'] = hca_status
        if hca_sn:
            search_dict['hca_sn'] = hca_sn
        if hca_vendor:
            search_dict['hca_vendor'] = hca_vendor
        search_dict['is_delete'] = 0
        # 查询数据
        hca_list = Hca.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        if hca_host:
            hca_list = Hca.objects.get_queryset().filter(hca_host__contains=hca_host, **search_dict).order_by(
                '-create_time')

        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(hca_list, pre_page)
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
            return Response(self.get_serializer(hca_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        hca = Hca.objects.get(id=id)
        hca.is_delete = True
        hca.remove_time = datetime.now()
        hca.save()
        result = model_to_dict(hca)
        return Response(result, status=status.HTTP_200_OK)


class NicViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Nic.objects.all()
    serializer_class = NicSerializer

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
        nic_status = request.query_params.get('nic_status')
        nic_sn = request.query_params.get('nic_sn')
        nic_vendor = request.query_params.get('nic_vendor')
        nic_host = request.query_params.get('nic_host')
        if nic_status:
            search_dict['nic_status'] = nic_status
        if nic_sn:
            search_dict['nic_sn'] = nic_sn
        if nic_vendor:
            search_dict['nic_vendor'] = nic_vendor
        search_dict['is_delete'] = 0
        # 查询数据
        nic_list = Nic.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        if nic_host:
            nic_list = Nic.objects.get_queryset().filter(nic_host__contains=nic_host, **search_dict).order_by(
                '-create_time')

        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(nic_list, pre_page)
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
            return Response(self.get_serializer(nic_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        nic = Nic.objects.get(id=id)
        nic.is_delete = True
        nic.remove_time = datetime.now()
        nic.save()
        result = model_to_dict(nic)
        return Response(result, status=status.HTTP_200_OK)


class SsdViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Ssd.objects.all()
    serializer_class = SsdSerializer

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
        ssd_status = request.query_params.get('ssd_status')
        ssd_sn = request.query_params.get('ssd_sn')
        ssd_vendor = request.query_params.get('ssd_vendor')
        ssd_host = request.query_params.get('ssd_host')
        if ssd_status:
            search_dict['ssd_status'] = ssd_status
        if ssd_sn:
            search_dict['ssd_sn'] = ssd_sn
        if ssd_vendor:
            search_dict['ssd_vendor'] = ssd_vendor
        search_dict['is_delete'] = 0
        # 查询数据
        ssd_list = Ssd.objects.get_queryset().filter(**search_dict).order_by('-create_time')
        if ssd_host:
            ssd_list = Ssd.objects.get_queryset().filter(ssd_host__contains=ssd_host, **search_dict).order_by(
                '-create_time')

        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(ssd_list, pre_page)
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
            return Response(self.get_serializer(ssd_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        ssd = Ssd.objects.get(id=id)
        ssd.is_delete = True
        ssd.remove_time = datetime.now()
        ssd.save()
        result = model_to_dict(ssd)
        return Response(result, status=status.HTTP_200_OK)
