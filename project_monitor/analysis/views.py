import time
import logging
import requests
from rest_framework import viewsets
from project_monitor import settings
from analysis.models import ServerAnalysis
from rest_framework.decorators import action
from rest_framework.response import Response
from analysis.serializers import ServerAnalysisSerializer


logger = logging.getLogger('log')


class ServerAnalysisViewSet(viewsets.ModelViewSet):
    queryset = ServerAnalysis.objects.all()
    serializer_class = ServerAnalysisSerializer

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
        indicator_code = request.query_params.get('type', None)
        num = int(request.query_params.get('num', 3))
        if indicator_code:
            search_dict['indicator_code'] = indicator_code
        # 查询数据
        server_list = ServerAnalysis.objects.get_queryset().filter(**search_dict).order_by("-insert_time", "-indicator_value")[:num]
        return Response(self.get_serializer(server_list, many=True).data)

    @action(methods=['get'], detail=False, url_path='history')
    def get_history_monitor(self, request, *args, **kwargs):
        """
        查询opentsdb中的数据库监控数据
        :param request: m=cpu_percent
        :param args:
        :param kwargs:
        :return:
        """
        # 查询条件
        search_dict = dict()
        indicator_code = request.query_params.get('m', None)
        end = int(time.time() * 1000)
        start = int(end - 1000 * 60 * 10)
        result = []
        num = int(request.query_params.get('num', 3))
        if indicator_code:
            search_dict['indicator_code'] = indicator_code
        # 查询数据
        server_list = ServerAnalysis.objects.get_queryset().filter(**search_dict).order_by("-insert_time", "-indicator_value")[:num]
        try:
            for server in server_list:
                r = requests.get(settings.OPENTSDB_URL + "query?start=" + str(start) + "&end=" + str(end) + "&m=sum:"
                                 + indicator_code + '{logicIp=' + server.host_ip + '}', timeout=3)
                if len(r.json()) > 0 and r.status_code == 200:
                    dps = r.json()[0]['dps']
                    res = dict()
                    res['name'] = server.host_ip
                    res['data'] = dps
                    result.append(res)
            return Response(result)
        except Exception as e:
            logger.error(e)
            return Response(data={"detail": "发生异常！"}, status=500)
