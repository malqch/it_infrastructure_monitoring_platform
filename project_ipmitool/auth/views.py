import logging
import requests
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import conf

logger = logging.getLogger('log')


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        对客户端提供的token信息进行验证
        :param request:
        :return: HTTP Response
        """
        url = conf.AUTH
        token = request.headers.get("token")
        if token is not None:
            headers = {'token': token}
        else:
            username = request.headers.get("username")
            password = request.headers.get("password")
            headers = {'username': username, 'password': password}
        r = requests.post(url, None, headers=headers)
        logger.info(r.status_code)
        if r.status_code != 200:
            raise exceptions.AuthenticationFailed('用户认证失败')

    def authenticate_header(self, request):
        pass
