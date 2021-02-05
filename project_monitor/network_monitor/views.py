import logging
from datetime import datetime
from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.core.paginator import Paginator
from rest_framework.response import Response
from network_monitor.models import NetworkMonitor, Series
from asset_relation.models import Device, DeviceModel, Storage
from network_monitor.serializers import NetworkMonitorSerializer, SeriesSerializer
from django_redis import get_redis_connection
from format import format_result
import requests
from project_monitor import settings
import time


logger = logging.getLogger('log')


class NetworkMonitorViewSet(viewsets.ModelViewSet):
    queryset = NetworkMonitor.objects.all()
    serializer_class = NetworkMonitorSerializer

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
        indicator_name = request.query_params.get('indicator_name')
        indicator_code = request.query_params.get('indicator_code')
        indicator_oid = request.query_params.get('indicator_oid')
        series_name = request.query_params.get('series_name')
        is_delete = request.query_params.get('is_delete')
        if indicator_name:
            search_dict['indicator_name'] = indicator_name
        if indicator_code:
            search_dict['indicator_code'] = indicator_code
        if is_delete:
            search_dict['is_delete'] = is_delete
        if series_name:
            series = Series.objects.filter(series_name=series_name).first()
            print(series,1111111111111111111111)
            if series:
                search_dict['series_id'] = series.id
            else:
                search_dict['series_id'] = ''

        # 查询数据
        if indicator_oid:
            server_list = NetworkMonitor.objects.get_queryset().filter(**search_dict, indicator_oid__contains=indicator_oid).order_by('-gmt_create')
        else:
            server_list = NetworkMonitor.objects.get_queryset().filter(**search_dict).order_by('-gmt_create')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(server_list, pre_page)
            result = paginator.page(current_page)
            data = self.get_serializer(result, many=True).data
            # 定义返回结果
            res = dict()
            res['total_page'] = paginator.num_pages
            res['current_page'] = current_page
            res['pre_page'] = pre_page
            res['total_count'] = paginator.count
            res['data'] = data
            for network in res['data']:
                series_id = network['series_id']
                series = Series.objects.filter(id=series_id).first()
                if series:
                    network['series_name'] = series.series_name
                else:
                    network['series_name'] = ''
            return Response(res)
        else:
            return Response(self.get_serializer(server_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        network_monitor = NetworkMonitor.objects.get(id=id)
        network_monitor.is_delete = True
        network_monitor.remove_time = datetime.now()
        network_monitor.save()
        result = model_to_dict(network_monitor)
        return Response(result, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        #network_monitor = NetworkMonitor.objects.filter(indicator_name=request.data.get('indicator_name')).all()
        #if len(network_monitor) == 0:
        networkmonitor = NetworkMonitor()
        if 'indicator_name' in request.data.keys():
            networkmonitor.indicator_name = request.data['indicator_name']
        if 'indicator_code' in request.data.keys():
            networkmonitor.indicator_code = request.data['indicator_code']
        if 'indicator_oid' in request.data.keys():
            networkmonitor.indicator_oid = request.data['indicator_oid']
        if 'series_id' in request.data.keys():
            networkmonitor.series_id = request.data['series_id']
        if 'indicator_type' in request.data.keys():
            networkmonitor.indicator_type = request.data['indicator_type']
        if 'is_active' in request.data.keys():
            networkmonitor.is_active = request.data['is_active']
        if 'collect_type' in request.data.keys():
            networkmonitor.collect_type = request.data['collect_type']
        networkmonitor.gmt_create = datetime.now()
        networkmonitor.save()
        result = model_to_dict(networkmonitor)
        return Response(result, status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        id = int(kwargs['pk'])
        networkmonitor = NetworkMonitor.objects.filter(id=id).first()
        if 'indicator_name' in request.data.keys():
            networkmonitor.indicator_name = request.data['indicator_name']
        if 'indicator_code' in request.data.keys():
            networkmonitor.indicator_code = request.data['indicator_code']
        if 'indicator_oid' in request.data.keys():
            networkmonitor.indicator_oid = request.data['indicator_oid']
        if 'series_id' in request.data.keys():
            networkmonitor.series_id = request.data['series_id']
        if 'indicator_type' in request.data.keys():
            networkmonitor.indicator_type = request.data['indicator_type']
        if 'is_active' in request.data.keys():
            networkmonitor.is_active = request.data['is_active']
        if 'collect_type' in request.data.keys():
            networkmonitor.collect_type = request.data['collect_type']
        networkmonitor.save()
        result = model_to_dict(networkmonitor)
        return Response(data=result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='indicator')
    def get_network_monitor_available(self, request):
        """
        获取可用于告警规则的网络设备和存储的监控项
        :return:
        """
        device_type = request.query_params.get('device_type')

        if device_type == '存储':
            series_id_info = Storage.objects.filter(is_delete=0).all()
        else:
            if device_type == '交换机':
                device_type = 'Switch'
            elif device_type == '防火墙':
                device_type = 'FW'
            elif device_type == '路由器':
                device_type = 'Router'
            elif device_type == '负载均衡':
                device_type = 'LB'
            series_id_info = DeviceModel.objects.filter(type=device_type).all()

        series_id_list = []
        if series_id_info:
            for series_id in series_id_info:
                series_id_list.append(series_id.series_id)
            network_monitor = NetworkMonitor.objects.values('indicator_name','indicator_code').distinct().\
                filter(series_id__in=series_id_list, is_active=1, is_delete=0)
            return Response(data=network_monitor, status=status.HTTP_200_OK)
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path="monitor")
    def get_monitor(self, request, *args, **kwargs):
        """
        查询redis数据库中的实时数据信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        network_name = request.query_params.get('network_name', None)
        if network_name is None:
            return Response(status=400, data={"detail": "参数错误！"})
        conn = get_redis_connection("default")
        res = conn.hgetall(network_name)
        if res is None:
            return Response(data={"detail": "未查询到数据"})
        else:
            data = format_result(res)
            return Response(data)

    @action(methods=['get'], detail=False, url_path='history')
    def get_history_monitor(self, request, *args, **kwargs):
        """
        查询opentsdb中的数据库监控数据
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


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

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
        source_id = request.query_params.get('source_id')
        vendor_id = request.query_params.get('vendor_id')
        series_name = request.query_params.get('series_name')
        if source_id:
            search_dict['source_id'] = source_id
        if vendor_id:
            search_dict['vendor_id'] = vendor_id
        if series_name:
            search_dict['series_name'] = series_name
        # 查询数据
        series_list = Series.objects.get_queryset().filter(**search_dict).order_by('id')

        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(series_list, pre_page)
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
            return Response(self.get_serializer(series_list, many=True).data)

    @action(detail=True, methods=['GET'])
    def get_series(self):
        """
        获取可用于告警规则的服务器监控项
        :return:
        """
        series = Series.objects.filter()
        if series:
            series = model_to_dict(series)
            return Response(series, status=status.HTTP_200_OK)






