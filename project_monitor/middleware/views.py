
from django.core.paginator import Paginator
from django.db.models import Count
from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from databases.models import Databases
from middleware.models import Middleware, MiddlewareItem
from middleware.serializers import MiddlewareSerializer, MiddlewareItemSerializer
from django_redis import get_redis_connection
from project_monitor import settings
import datetime
import logging
import requests
import json

logger = logging.getLogger('log')


class MiddlewareViewSet(viewsets.ModelViewSet):
    queryset = Middleware.objects.all()
    serializer_class = MiddlewareSerializer

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        # 查询条件
        search_dict = dict()
        middleware_name = request.query_params.get('name', None)
        middleware_type = request.query_params.get('middleware_type', None)
        is_monitor = request.query_params.get('is_monitor', None)
        if middleware_name:
            search_dict['name'] = middleware_name
        if middleware_type:
            search_dict['middleware_type'] = middleware_type
        if is_monitor:
            search_dict['is_monitor'] = is_monitor

        search_dict['is_delete'] = False
        # 查询数据
        middleware_list = Middleware.objects.get_queryset().filter(**search_dict).order_by('id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(middleware_list, pre_page)
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
            return Response(self.get_serializer(middleware_list, many=True).data)

    @action(detail=False, methods=['put'])
    def delete(self, request):
        db_id = request.data.get('ids', None)
        db = Middleware.objects.filter(id__in=db_id).update(is_delete=1, remove_time=datetime.datetime.now())
        return Response(db)

    @action(detail=False, methods=['get'], url_path="tag")
    def get_tag(self, request, *args, **kwargs):
        middleware_type = request.query_params.get('server_type', None)
        middleware_info = Middleware.objects.filter(middleware_type=middleware_type).all()
        tag_info = []
        if middleware_info:
            for middleware in middleware_info:
                tag = middleware_type + '_' + middleware.ip_address + '_' + str(middleware.port)
                device_name = middleware.name
                device_ip = middleware.ip_address
                tag_info.append({"tag": tag, "device_name": device_name, "device_ip": device_ip})
            return Response(data=tag_info, status=status.HTTP_200_OK)
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
        middleware_name = request.query_params.get('middleware_name', None)
        if middleware_name is None:
            return Response(status=400, data={"detail": "参数错误！"})
        conn = get_redis_connection("default")
        res = conn.hgetall(middleware_name)
        data = dict()
        for k, v in res.items():
            try:
                value = json.loads(str(v, encoding="utf-8"))
            except Exception as e:
                value = str(v, encoding="utf-8")
            data[k.decode('utf-8')] = value
        if res is None:
            return Response(data={"detail": "未查询到数据"})
        else:
            return Response(data)

    @action(methods=['get'], detail=False, url_path='history')
    def get_history_monitor(self, request, *args, **kwargs):
        """
        查询opentsdb中的监控数据
        :param request: start=2020/07/14-00:00:00&end=2020/07/14-00:00:00&m=sum:hwAvgDuty1min
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

    @action(detail=False, methods=['GET'])
    def search(self, request):
        query = request.query_params.get('query', None)
        middleware_type = request.query_params.get('middleware_type', None)
        is_monitor = request.query_params.get('is_monitor', None)
        if query:
            middleware_info = Middleware.objects.get_queryset().filter(is_delete=0, port__contains=query,
                                                                       is_monitor=is_monitor,
                                                                       middleware_type__contains=middleware_type)
            if not len(middleware_info):
                middleware_info = Middleware.objects.get_queryset().filter(is_delete=0, ip_address__contains=query,
                                                                           is_monitor=is_monitor,
                                                                           middleware_type__contains=middleware_type)
            return Response(
                self.get_serializer(middleware_info, many=True).data)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='count')
    def get_middleware_and_database_count(self, request):
        """
        统计数据库\中间件的数量
        :return:
        """
        result = {"middleware_count": [], "database_count": []}
        middleware = Middleware.objects.filter(is_delete=0).aggregate(middleware_count=Count('id'))
        result['middleware_count'].append({"name":"middleware", "value": middleware['middleware_count']})
        database = Databases.objects.filter(is_delete=0).aggregate(database_count=Count('id'))
        result['database_count'].append({"name":"database", "value": database['database_count']})
        return Response(data=result, status=status.HTTP_200_OK)



class MiddlewareItemViewSet(viewsets.ModelViewSet):
    queryset = MiddlewareItem.objects.all()
    serializer_class = MiddlewareItemSerializer

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        # 查询条件
        search_dict = dict()
        item_name = request.query_params.get('item_name', None)
        if item_name:
            search_dict['item_name'] = item_name

        # 查询数据
        item_list = MiddlewareItem.objects.get_queryset().filter(**search_dict).order_by('id')

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

    @action(detail=True, methods=['POST'])
    def get_middleware_available(self, request):
        """
        获取可用于告警规则的中间件监控项
        :return:
        """
        middleware_type = request.data['middleware_type']
        middleware = MiddlewareItem.objects.filter(middleware_type=middleware_type).all()
        if middleware:
            middleware = model_to_dict(middleware)
            return Response(middleware, status=status.HTTP_200_OK)
