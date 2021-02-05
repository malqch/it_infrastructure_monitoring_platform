from rest_framework import viewsets, status
from sys_auth.views import MyAuthentication
from rest_framework.decorators import action
import requests
import json
from rest_framework.response import Response
import logging
import re

logger = logging.getLogger('log')


class HostViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]

    @action(detail=False, methods=['POST'])
    def authorization_user(self, request):
        logger.info(request.data)
        dict_ = {}
        res_status, res_json, res_headers = self.verify_user(request.data)
        dict_['deviceid'] = res_json['data'].get('deviceid', None)
        set_cookie = res_headers.get('Set-Cookie', '')
        session = re.search('ismsession.*?;', set_cookie).group()
        session = session.replace(';', '')
        dict_['headers'] = {"Content-Type": "application/json", "session": session}
        logger.info(dict_)
        return Response(dict_)

    @staticmethod
    def verify_user(data):
        manage_address = data.get('manage_address', None)
        username = data.get('manage_username', None)
        password = data.get('manage_password', None)
        try:
            url = manage_address + '/deviceManager/rest/xxxxx/sessions'
            params = json.dumps({"username": username, "password": password, "scope": 0})
            headers = {"Content-Type": "application/json"}
            res = requests.post(url, params, headers=headers, verify=False)
            res_status = res.status_code
            res_json = res.json()
            res_headers = res.headers
            return res_status, res_json, res_headers
        except Exception as e:
            logger.error(e)
            return None, None, None

    @action(detail=False, methods=['POST'], url_path='host_list')
    def host_list(self, request):
        logger.info(request.data)
        manage_address = request.data.get('manage_address', None)
        res_status, res_json, res_headers = self.verify_user(request.data)
        if res_json.get('data'):
            try:
                deviceid = res_json['data'].get('deviceid', None)
                url = manage_address + '/deviceManager/rest/' + deviceid + '/host'
                set_cookie = res_headers.get('Set-Cookie', '')
                session = re.search('ismsession.*?;', set_cookie).group()
                session = session.replace(';', '')
                headers = {"Content-Type": "application/json", "session": session}
                res_host = requests.get(url, headers=headers, verify=False)
                res_host_status = res_host.status_code
                res_host_json = res_host.json()
                if res_host_status == 200:
                    return Response(data=res_host_json.get('data'),
                                status=status.HTTP_200_OK)
                else:
                    return Response({'msg': res_host_json.get('error')})
            except Exception as e:
                logger.error(e)
                return Response({'msg': "请求报错"})
        else:
            return Response({'msg': res_json.get('error')}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['POST'], url_path='host_creation')
    def create_host(self, request):
        """
        创建主机
        """
        logger.info(request.data)
        manage_address = request.data.get('manage_address', None)
        res_status, res_json, res_headers = self.verify_user(request.data)
        if res_json.get('data'):
            try:
                deviceid = res_json['data'].get('deviceid', None)
                url = manage_address + '/deviceManager/rest/' + deviceid + '/host'
                set_cookie = res_headers.get('Set-Cookie', '')
                session = re.search('ismsession.*?;', set_cookie).group()
                session = session.replace(';', '')
                headers = {"Content-Type": "application/json", "session": session, 'iBaseToken': res_json['data']['iBaseToken']}
                res_host = requests.post(url, data= json.dumps(request.data['data']), headers=headers,
                                        verify=False)
                res_host_status = res_host.status_code
                res_host_json = res_host.json()
                if res_host_status == 200:
                    return Response(data=res_host_json.get('data'),
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'msg': res_host_json.get('error')})
            except Exception as e:
                logger.error(e)
                return Response({'msg': "请求报错"})

        else:
            return Response({'msg': res_json.get('error')}, status=status.HTTP_400_BAD_REQUEST)




