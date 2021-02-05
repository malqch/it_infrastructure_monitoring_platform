import logging
from rest_framework.views import APIView
from rest_framework.response import Response
import os
import urllib.request
import conf
import json


logger = logging.getLogger('log')
basedir = os.path.abspath(os.path.dirname(__file__))


class CallMacView(APIView):
    @staticmethod
    def post(request):
        data = request.data
        print(data, 11111)
        logger.info(data)
        try:
            call_url = conf.AUTOMATION_URL + 'pm_port/'
            headers = {'Content-Type': 'application/json'}
            params = json.dumps(data)
            params = bytes(params, 'utf8')
            req = urllib.request.Request(call_url, data=params,
                                         headers=headers, method="POST")
            response = urllib.request.urlopen(req)
            data = json.loads(response.read())
            logger.info(data)
            return Response({"msg": "请求成功"})
        except Exception as e:
            logger.error(e)
            return Response({"msg": "请求失败"})
