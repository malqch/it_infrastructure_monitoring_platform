import logging
import datetime
import requests
from rest_framework import exceptions
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import BaseAuthentication
import conf
from sys_auth.models import Token, User

logger = logging.getLogger('log')


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        对客户端提供的token或用户信息进行验证
        :param request:
        :return: HTTP Response
        """
        token = request.headers.get("token")
        if token is not None:
            """ 验证 token """
            token_obj = Token.objects.using('sys').filter(token=token).first()
            if not token_obj:
                """ 未查询到token信息 """
                raise exceptions.NotAuthenticated('用户认证失败')
            if token_obj.expire_time.strftime('%Y-%m-%d %H:%M:%S') < \
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                """ token信息过期"""
                raise exceptions.NotAuthenticated('token过期')
        else:
            """ 验证用户名密码 """
            user = request.headers.get("username")
            pwd = request.headers.get("password")
            obj = User.objects.using('sys').filter(username=user, is_delete=0).first()

            if not obj:
                """ 未能查询到用户信息，则返回给客户端响应的提示信息 """
                raise exceptions.NotAuthenticated('未查询到用户信息！')
            else:
                password = User.objects.using('sys').filter(username=user, is_delete=0).values("password")[0]["password"]
                res = check_password(pwd, password)
                if not res:
                    raise exceptions.NotAuthenticated('密码错误！')
        return
        # url = conf.AUTH
        # token = request.headers.get("token")
        # if token is not None:
        #     headers = {'token': token}
        # else:
        #     username = request.headers.get("username")
        #     password = request.headers.get("password")
        #     headers = {'username': username, 'password': password}
        # r = requests.post(url, None, headers=headers)
        # logger.info(r.status_code)
        # if r.status_code != 200:
        #     raise exceptions.AuthenticationFailed('用户认证失败')

    def authenticate_header(self, request):
        pass
