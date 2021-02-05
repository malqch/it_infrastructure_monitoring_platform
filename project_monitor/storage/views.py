import time
from django.core.paginator import Paginator
from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from storage.models import StorageItem
from storage.serializers import StorageItemSerializer
import logging
import requests
from project_monitor import settings
from format import format_result
from django_redis import get_redis_connection


logger = logging.getLogger('log')


class StorageItemViewSet(viewsets.ModelViewSet):
    queryset = StorageItem.objects.all()
    serializer_class = StorageItemSerializer

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        # 查询条件
        item_name = request.query_params.get('item_name', None)
        # 查询数据
        if item_name:
            item_list = StorageItem.objects.get_queryset().filter(item_name__icontains=item_name).order_by('id')
        else:
            item_list = StorageItem.objects.get_queryset().order_by('id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(item_list, pre_page)
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
            return Response(self.get_serializer(item_list, many=True).data)

    @action(detail=False, methods=['get'], url_path='storage')
    def get_storage_available(self, request):
        """
        获取可用于告警规则的存储监控项
        :return:
        """
        storage_type = request.query_params.get('storage_type')
        if storage_type:
            storage_item = StorageItem.objects.filter(storage_type=storage_type).all()
            if storage_item:
                return Response(data=storage_item.values(), status=status.HTTP_200_OK)
        else:
            storage_item = StorageItem.objects.all()
            return Response(data=storage_item.values(), status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path="monitor")
    def get_monitor(self, request, *args, **kwargs):
        """
        查询redis存储设备中的实时数据信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        storage_name = request.query_params.get('storage_name', None)
        if storage_name is None:
            return Response(status=400, data={"detail": "参数错误！"})
        conn = get_redis_connection("default")
        res = conn.hgetall(storage_name)
        if res is None:
            return Response(data={"detail": "未查询到数据"})
        else:
            data = format_result(res)
            return Response(data)

    @action(methods=['get'], detail=False, url_path='history')
    def get_history_monitor(self, request, *args, **kwargs):
        """
        查询opentsdb中的存储设备监控数据
        :param request: start=2020/07/14-00:00:00&end=2020/07/14-00:00:00&m=sum:hwAvgDuty1min
        :param args:
        :param kwargs:
        :return:
        """
        metrics_param = request.query_params.get('m', None)
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        logic_ip = request.query_params.get('logic_ip', None)
        metrics = metrics_param.split(',')
        result = dict()
        try:
            for metric in metrics:
                time.sleep(0.001)
                r = requests.get(settings.OPENTSDB_URL + "query?start=" + start + "&end=" + end + "&m=sum:2m-avg-zero:"
                                 + metric + '{logicIp=' + logic_ip + '}', timeout=8)
                if len(r.json()) > 0 and r.status_code == 200:
                    dps = r.json()[0]['dps']
                    result[metric] = dps.values()
                    result['time'] = dps.keys()
            return Response(result)
        except Exception as e:
            logger.error(e)
            return Response(data={"detail": "发生异常！"}, status=500)


    @action(methods=['get'], detail=False, url_path='type')
    def get_storage_type(self, request):
        storage_info = StorageItem.objects.values('storage_type').distinct().all()
        print(storage_info,123)
        # storage_info = model_to_dict(storage_info)
        return Response(data=storage_info, status=status.HTTP_200_OK)





