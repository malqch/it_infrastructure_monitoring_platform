import logging
from datetime import datetime
import requests
from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.decorators import action
from project_monitor import settings
from django.core.paginator import Paginator
from rest_framework.response import Response
from server_monitor.models import ServerMonitor
from server_monitor.serializers import ServerMonitorSerializer
from format import format_result
from django_redis import get_redis_connection

logger = logging.getLogger('log')


class ServerMonitorViewSet(viewsets.ModelViewSet):
    queryset = ServerMonitor.objects.all()
    serializer_class = ServerMonitorSerializer

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
        monitor_type = request.query_params.get('monitor_type')
        specific_type = request.query_params.get('specific_type')
        indicator = request.query_params.get('indicator')
        indicator_name = request.query_params.get('indicator_name')
        is_delete = request.query_params.get('is_delete')
        if monitor_type:
            search_dict['monitor_type'] = monitor_type
        if specific_type:
            search_dict['specific_type'] = specific_type
        if indicator:
            search_dict['indicator'] = indicator
        if indicator_name:
            search_dict['indicator_name'] = indicator_name
        if is_delete:
            search_dict['is_delete'] = is_delete
        # 查询数据
        server_list = ServerMonitor.objects.get_queryset().filter(**search_dict).order_by('-create_time')

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
            return Response(res)
        else:
            return Response(self.get_serializer(server_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        server_monitor = ServerMonitor.objects.get(id=id)
        server_monitor.is_delete = True
        server_monitor.remove_time = datetime.now()
        server_monitor.save()
        result = model_to_dict(server_monitor)
        return Response(result, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        server_monitor = ServerMonitor.objects.filter(indicator_name=request.data.get('indicator_name')).all()
        if len(server_monitor) == 0:
            servermonitor = ServerMonitor()
            if 'monitor_type' in request.data.keys():
                servermonitor.monitor_type = request.data['monitor_type']
            if 'specific_type' in request.data.keys():
                servermonitor.specific_type = request.data['specific_type']
            if 'indicator' in request.data.keys():
                servermonitor.indicator = request.data['indicator']
            if 'remark' in request.data.keys():
                servermonitor.remark = request.data['remark']
            servermonitor.create_time = datetime.now()
            servermonitor.save()
            result = model_to_dict(servermonitor)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            result = {'msg': '资源已存在'}
            return Response(data=result, status=status.HTTP_205_RESET_CONTENT)

    def update(self, request, *args, **kwargs):
        server_monitor = ServerMonitor.objects.filter(indicator_name=request.data.get('indicator_name')).all()
        # datacenter = Datacenter()
        # 数据库中不存在同名的数据中心
        if len(server_monitor) == 0:
            id = int(kwargs['pk'])
            servermonitor = ServerMonitor.objects.filter(id=id).first()
            servermonitor.indicator_name = request.data['indicator_name']
            if 'monitor_type' in request.data.keys():
                servermonitor.monitor_type = request.data['monitor_type']
            if 'specific_type' in request.data.keys():
                servermonitor.specific_type = request.data['specific_type']
            if 'indicator' in request.data.keys():
                servermonitor.indicator = request.data['indicator']
            if 'indicator_name' in request.data.keys():
                servermonitor.indicator_name = request.data['indicator_name']
            if 'remark' in request.data.keys():
                servermonitor.remark = request.data['remark']
            if 'is_available' in request.data.keys():
                servermonitor.is_available = request.data['is_available']
            servermonitor.save()
            result = model_to_dict(servermonitor)
            return Response(data=result, status=status.HTTP_200_OK)
        else: # 数据库中存在同名的数据中心
            for servermonitor in server_monitor:
                id = int(kwargs['pk'])
                if servermonitor.id == id:
                    request.data.pop('indicator_name')
                    if 'monitor_type' in request.data.keys():
                        servermonitor.monitor_type = request.data['monitor_type']
                    if 'specific_type' in request.data.keys():
                        servermonitor.specific_type = request.data['specific_type']
                    if 'indicator' in request.data.keys():
                        servermonitor.indicator = request.data['indicator']
                    if 'is_available' in request.data.keys():
                        servermonitor.is_available = request.data['is_available']
                    servermonitor.save()
                    result = model_to_dict(servermonitor)
                    return Response(data=result, status=status.HTTP_200_OK)
                else:
                    result = '{"msg":"资源已存在"}'
                    return Response(data=result, status=status.HTTP_205_RESET_CONTENT)

    @action(detail=False, methods=['GET'])
    def get_indicator(self, request, *args, **kwargs):
        """
        获取可用于告警规则的服务器监控项
        :return:
        """
        search_dict = {}
        search_dict['is_delete'] = 0
        search_dict['is_available'] = '可用'
        specific_type = request.query_params.get('specific_type')
        monitor_type = request.query_params.get('monitor_type')
        if monitor_type:
            search_dict['monitor_type'] = monitor_type
        if specific_type:
            if specific_type == 'WEBLOGIC':
                specific_type = 'webLogic'
            elif specific_type == 'RABBITMQ':
                specific_type = 'rabbitMQ'
            else:
                specific_type = specific_type.lower()
            search_dict['specific_type'] = specific_type

        server_monitor = ServerMonitor.objects.filter(**search_dict).all()
        if server_monitor:
            server_list = []
            for server in server_monitor:
                server = model_to_dict(server)
                server_list.append(server)
                # server_monitor = model_to_dict(server_monitor)
            return Response(server_list, status=status.HTTP_200_OK)
        else:
            return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def get_specific(self, request, *args, **kwargs):
        """
        获取可用于告警规则的服务器监控项
        :return:
        """
        search_dict = {}
        search_dict['is_delete'] = 0
        monitor_type = request.query_params.get('monitor_type')
        if monitor_type:
            search_dict['monitor_type'] = monitor_type
        server_monitor = ServerMonitor.objects.filter(**search_dict).values('specific_type').distinct()
        if server_monitor:
            server_list = []
            for server in server_monitor:
                # server = model_to_dict(server)
                server_list.append(server['specific_type'])
                # server_monitor = model_to_dict(server_monitor)
            print(server_list)
            return Response(server_list, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='history')
    def get_history_monitor(self, request, *args, **kwargs):
        """
        查询opentsdb中的数据库监控数据
        :param request: start_time=2020/07/14-00:00:00&end_time=2020/07/14-00:00:00&metric=sum:hwAvgDuty1min
        :param args:
        :param kwargs:
        :return:
        """
        metric = request.query_params.get('m', None)
        start = request.query_params.get('start', None)
        end = request.query_params.get('end', None)
        try:
            r = requests.get(settings.OPENTSDB_URL + "query?start=" + start + "&end=" + end + "&m=" + metric, timeout=3)
        except Exception as e:
            logger.error(e)
            return Response(data={"detail": "发生异常！"}, status=500)
        if len(r.json()) > 0 and r.status_code == 200:
            dps = r.json()[0]['dps']
            return Response(dps)
        else:
            return Response(data={"detail": "未查询到数据！"})

    @action(methods=['get'], detail=False, url_path="monitor")
    def get_monitor(self, request, *args, **kwargs):
        """
        查询redis数据库中的实时数据信
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        server_name = request.query_params.get('server_name')
        if server_name is None:
            return Response(data={"detail": "参数不正确！"}, status=400 )
        conn = get_redis_connection("default")
        res = conn.hgetall(server_name)
        if res is None:
            return Response(data={"detail": "未查询到数据"})
        else:
            data = format_result(res)
            return Response(data)

