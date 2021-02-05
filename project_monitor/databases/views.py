from django.core.paginator import Paginator
from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_redis import get_redis_connection
from rest_framework.decorators import action
from databases.models import Databases, DBItem
from databases.serializers import DatabaseSerializer, DBItemSerializer
from project_monitor import settings
from format import format_result
import datetime
import logging
import requests


logger = logging.getLogger('log')


class DatabaseViewSet(viewsets.ModelViewSet):
    queryset = Databases.objects.all()
    serializer_class = DatabaseSerializer

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
        name = request.query_params.get('name', None)
        db_type = request.query_params.get('db_type', None)
        is_monitor = request.query_params.get('is_monitor', None)
        if name:
            search_dict['name'] = name
        if db_type:
            search_dict['db_type'] = db_type
        if is_monitor:
            search_dict['is_monitor'] = is_monitor
        # 查询数据
        db_list = Databases.objects.get_queryset().filter(**search_dict, is_delete=0).order_by('id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(db_list, pre_page)
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
            return Response(self.get_serializer(db_list, many=True).data)

    @action(detail=False, methods=['put'])
    def delete(self, request):
        """
        逻辑删除数据库中的资源信息
        :param request:
        :return:
        """
        db_id = request.data.get('ids', None)
        db = Databases.objects.filter(id__in=db_id).update(is_delete=1, remove_time=datetime.datetime.now())
        return Response(db)

    @action(detail=False, methods=['get'], url_path="tag")
    def get_tag(self, request, *args, **kwargs):
        db_type = request.query_params.get('server_type', None)
        database_info = Databases.objects.filter(db_type=db_type).all()
        tag_info = []
        if database_info:
            for database in database_info:
                tag = db_type + '_' + database.ip_address + '_' + database.sid
                device_ip = database.ip_address
                device_name = database.name
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
        db_name = request.query_params.get('db_name', None)
        if db_name is None:
            return Response(status=400, data={"detail": "参数错误！"})
        conn = get_redis_connection("default")
        res = conn.hgetall(db_name)
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
        db_type = request.query_params.get('db_type', None)
        is_monitor = request.query_params.get('is_monitor', None)
        if query is not None:
            db_info = Databases.objects.get_queryset().filter(is_delete=0, sid__contains=query, is_monitor=is_monitor,
                                                              db_type__contains=db_type)
            if not len(db_info):
                db_info = Databases.objects.get_queryset().filter(is_delete=0, ip_address__contains=query,
                                                                  is_monitor=is_monitor, db_type__contains=db_type)
            return Response(
                self.get_serializer(db_info, many=True).data)
        return Response(status=status.HTTP_200_OK)


class DBItemViewSet(viewsets.ModelViewSet):
    queryset = DBItem.objects.all()
    serializer_class = DBItemSerializer

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
        item_list = DBItem.objects.get_queryset().filter(**search_dict).order_by('id')
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
    def get_database_available(self, request):
        """
        获取可用于告警规则的中间件监控项
        :return:
        """
        db_type = request.data['db_type']
        if db_type:
            db_item = DBItem.objects.filter(db_type=db_type).all()
            if db_item:
                db_item = model_to_dict(db_item)
                return Response(db_item, status=status.HTTP_200_OK)





