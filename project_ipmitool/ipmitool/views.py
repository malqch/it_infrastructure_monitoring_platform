import logging
from rest_framework.views import APIView
import subprocess
from django.http import FileResponse, StreamingHttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
import os
from auth.views import MyAuthentication


logger = logging.getLogger('log')
basedir = os.path.abspath(os.path.dirname(__file__))


class IpmitoolView(APIView):
    @staticmethod
    def post(request):
        data = request.data
        logger.info(data)
        console_ip = data.get('console_ip', None)
        console_user = data.get('console_user', None)
        console_password = data.get('console_password', None)
        if console_ip and console_user and console_password:
            cmd1 = f"ipmitool -H {console_ip} -I lanplus -U {console_user} -P {console_password} chassis bootdev pxe"
            result_1 = os.system(
                cmd1.format(ip=console_ip, user=console_user,
                            passwd=console_password) + "> /dev/null 2>&1")
            cmd2 = f"ipmitool -H {console_ip} -I lanplus -U {console_user} -P {console_password} chassis power reset"
            result_2 = os.system(
                cmd2.format(ip=console_ip, user=console_user,
                            passwd=console_password) + "> /dev/null 2>&1")
            if result_1 == 0 and result_2 == 0:
                return Response({'msg': '重启成功'})
            else:
                return Response({'msg': '重启失败'})
        else:
            return Response({"msg": '请求参数不正确'})


class CheckSnView(APIView):
    @staticmethod
    def get(request):
        sn = request.query_params.get("sn", None)
        console_ip = request.query_params.get("console_ip", None)
        console_user = request.query_params.get('console_user', None)
        console_pwd = request.query_params.get('console_password', None)
        logger.info(console_ip)
        logger.info(sn)
        cmd = f"ping -c 3 {console_ip}|grep '0 received'|wc -l"
        logger.info('cmd: ' + cmd)
        result0 = os.popen(cmd)
        outcome = result0.readline().strip('\n').strip()
        logger.info(outcome)
        if outcome == '0':
            try:
                result = os.popen(f"ipmitool -H {console_ip} -I lanplus -U {console_user} -P {console_pwd} fru list|grep 'Product Serial' ")
                logger.info(result)
                console_sn = result.readline().strip('\n').split(':')[1].strip()
                cmdb_sn = sn
                if console_sn == cmdb_sn:
                    logger.info("sn一致")
                    return Response({'msg':'sn一致', 'check_result': 1})
                else:
                    logger.error("SNERROR")
                    return Response({"msg": "SNERROR", 'check_result': 0})
            except Exception:
                logger.error("IPMIINFOERROR")
                return Response({"msg": "IPMIINFOERROR", 'check_result': 2})
        # elif outcome == '1':
        #     return Response({"msg": "CONNECTERROR", 'check_result': 0})
        else:
            logger.error("CONNECTERROR")
            return Response({"msg": "CONNECTERROR", 'check_result': 0})
