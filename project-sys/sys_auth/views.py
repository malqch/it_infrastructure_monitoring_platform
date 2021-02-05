import time
import hashlib
import logging
import datetime
import traceback
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.decorators import action
from sys_auth.models import User, Role, Menu, Token, RoleUser
from rest_framework.authentication import BaseAuthentication
from sys_auth.serializers import UserSerializer, RoleSerializer, MenuSerializer

logger = logging.getLogger('log')


def make_token(user):
    ctime = str(time.time())
    hash = hashlib.md5(user.encode("utf-8"))
    hash.update(ctime.encode("utf-8"))
    return hash.hexdigest()


class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        对客户端提供的token信息进行验证
        :param request:
        :return: HTTP Response
        """
        token = request.headers.get("token")
        if token is not None:
            """ 验证 token """
            token_obj = Token.objects.filter(token=token).first()
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
            obj = User.objects.filter(username=user, is_delete=0).first()

            if not obj:
                """ 未能查询到用户信息，则返回给客户端响应的提示信息 """
                raise exceptions.NotAuthenticated('未查询到用户信息！')
            else:
                password = User.objects.filter(username=user, is_delete=0).values("password")[0]["password"]
                res = check_password(pwd, password)
                if not res:
                    raise exceptions.NotAuthenticated('密码错误！')
        return

    def authenticate_header(self, request):
        pass


class AuthView(APIView):
    @staticmethod
    def post(request):
        """
        用户第一次登陆，验证用户名和密码信息
        :param request:
        :return: HTTP Response
        """
        ret = {'msg': "登录成功", 'token': None}
        try:
            token = request.headers.get("token")
            # 如果存在token，验证token信息
            if token is not None:
                token_obj = Token.objects.filter(token=token).first()
                if not token_obj:
                    """ 未查询到token信息 """
                    ret = {"msg": "用户认证失败"}
                    return Response(ret, status.HTTP_401_UNAUTHORIZED)

                if token_obj.expire_time.strftime("%Y-%m-%d %H:%M:%S") < datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
                    """ token信息过期"""
                    ret = {"msg": "登录超时, 请重新登录"}
                    return Response(ret, status.HTTP_401_UNAUTHORIZED)
                ret['token'] = token
                return Response(ret, status.HTTP_200_OK)
            else:
                user = request.headers.get("username")
                pwd = request.headers.get("password")
                obj = User.objects.filter(username=user, is_delete=0).first()

                if not obj:
                    """ 未能查询到用户信息，则返回给客户端响应的提示信息 """
                    ret = {"msg": "用户不存在！"}
                    return Response(ret, status.HTTP_401_UNAUTHORIZED)
                else:
                    password = User.objects.filter(username=user, is_delete=0).values("password")[0]["password"]
                    res = check_password(pwd, password)
                    if not res:
                        ret = {"msg": "密码错误！"}
                        return Response(ret, status.HTTP_401_UNAUTHORIZED)

                """ 查询到用户信息，则生成token信息、设置过期时间并保存至数据库中 """
                token = make_token(user)
                expire_time = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
                Token.objects.update_or_create(user=obj, defaults={"token": token, "expire_time": expire_time})

                """ 返回登陆成功 HTTP Response """
                ret['token'] = token
                return Response(ret, status.HTTP_200_OK)
        except exceptions as e:
            logger.error(traceback.format_exc(e))
            ret['msg'] = "请求异常"
            return JsonResponse(ret, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        # 查询条件
        user_name = request.query_params.get('username', None)
        # 查询数据
        if user_name:
            user_list = User.objects.get_queryset().filter(username__icontains=user_name, is_delete=0).order_by('id')
        else:
            user_list = User.objects.get_queryset().filter(is_delete=0).order_by('id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(user_list, pre_page)
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
            return Response(self.get_serializer(user_list, many=True).data)

    def create(self, request, *args, **kwargs):
        users = User.objects.filter(username=request.data.get('username'), is_delete=0).all()
        if len(users) == 0:
            user_form = request.data
            user_form['password'] = make_password(user_form.get('password'))
            return super().create(request, *args, user_form)
        else:
            result = {'msg': '资源已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    @action(detail=False, methods=['put'])
    def change_pwd(self, request):
        user_name = request.data.get('username')
        old_password = request.data.get('old_pwd')
        new_password = request.data.get('new_pwd')
        user = User.objects.get(username=user_name)
        if user:
            if check_password(old_password, user.password):
                user.password = make_password(new_password)
                user.save()
                result = {'msg': '密码修改成功'}
                return Response(result, status=status.HTTP_200_OK)
            else:
                result = {'msg': '原密码错误!'}
                return Response(result, status=status.HTTP_401_UNAUTHORIZED)
        else:
            result = {'msg': '用户不存在'}
            return Response(result, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def reset_pwd(self, request, pk):
        User.objects.filter(id=pk).update(password=make_password('123456'))
        result = {'msg': '密码重置成功'}
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def role(self, request):
        """
        根据用户名查询角色与权限信息
        :param request:
        :return:
        """
        user_name = request.query_params.get('username', None)
        application = request.query_params.get('application', None)
        menu_type = request.query_params.get('type', None)
        # 根据用户名查询角色与权限信息
        user_info = User.objects.filter(username=user_name, is_delete=0).first()
        serializer = UserSerializer(user_info)
        # 查询对应系统下的菜单栏
        role_list = serializer.data['roles']
        menus_list = []
        for i in role_list:
            menus_list.extend(i['menus'])
        # 多个角色菜单栏去重
        menus = [dict(t) for t in set([tuple(m.items()) for m in menus_list])]
        # 查询对应系统下的菜单栏
        data = sorted(filter(lambda info: info['application'] == application and
                                          info['menu_type']==menu_type and info['is_delete']==0, menus), key=lambda y: y['id'])
        res = dict()
        if menu_type=='button':
            data = [i['perms'] for i in data]
        res['data'] = data
        return Response(data)

    @action(detail=True, methods=['put'], url_path='assign_user')
    def assign_user(self, request, pk):
        """
        给用户分配角色
        :param request:
        :param pk:
        :return:
        """
        role_ids = request.data.get("roles")
        user = self.get_object()
        user.roles.set(role_ids)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def delete(self, request):
        users_id = request.data.get('ids', None)
        users = User.objects.filter(id__in=users_id).update(is_delete=1, remove_time=datetime.datetime.now())
        return Response(users)


class RoleViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        """
        系统内添加角色信息，如果存在相同名称的角色，则不允许添加
        :param request: {'name':'test', 'remark':'test'}
        :param args:
        :param kwargs:
        :return: HTTP Response
        """
        roles = Role.objects.filter(name=request.data.get('name'), is_delete=0).all()
        if len(roles) == 0:
            return super().create(request, *args, **kwargs)
        else:
            result = {'msg': '资源已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    @action(detail=False, methods=['get'])
    def user(self, request):
        """
        查询指定角色下的用户与权限信息
        :param request:
        :return: HTTP Response
        """
        # 根据用户名查询用户信息
        user_name = request.query_params.get('username', None)
        pid = int(request.query_params.get('pid', None))
        user_info = User.objects.filter(username=user_name).first()
        # 根据用户id查询角色信息
        role_info = RoleUser.objects.filter(user_id=user_info.id).first()
        pk = role_info.role_id
        # 查询角色对应下的权限信息
        role = Role.objects.filter(id=pk).first()
        serializer = RoleSerializer(role)
        # 查询对应系统下的菜单栏
        menu_list = serializer.data['menus']
        for info in menu_list[:]:
            if info['p_id'] != pid:
                menu_list.remove(info)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='assign_user')
    def assign_user(self, request, pk):
        """
        给用户分配角色
        :param request:
        :param pk:
        :return:
        """
        user_ids = request.data.get("users")
        role = self.get_object()
        users = User.objects.filter(id__in=user_ids).all()
        for user in users:
            role.users.add(user)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    @action(detail=True)
    def menu(self, request, pk):
        """
        查询指定角色下的权限信息
        :param request:
        :param pk: 指定的角色信息
        :return: HTTP Response
        """
        role = self.get_object()
        menu_data = sorted(filter(lambda m: m['is_delete'] == 0, RoleSerializer(role).data['menus']), key=lambda s: s['id'])
        return Response(menu_data)

    @action(detail=True)
    def to_menu(self, request, pk):
        """
        查询指定角色下待分配的权限信息
        :param request:
        :param pk: 指定的角色信息
        :return: HTTP Response
        """
        # 查询所有菜单栏
        menus = Menu.objects.get_queryset().filter(is_delete=0).all()
        menus_serializer = MenuSerializer(menus, many=True).data
        # 查询角色下的菜单栏信息
        # role_info = Role.objects.filter(id=role_id, is_delete=0).first()
        role_info = self.get_object()
        role_serializer = RoleSerializer(role_info)
        role_menu = role_serializer.data['menus']
        # 取两者的差集
        menu_res = [i for i in menus_serializer if i not in role_menu]
        # 取待分配菜单及其父菜单数据
        menu_ids = [x['id'] for x in menu_res]
        for j in menu_res:
            if j['p_id'] not in menu_ids:
                menu_res.extend(filter(lambda m: m['id'] == j['p_id'],  menus_serializer))
                menu_ids.append(j['p_id'])
        menus_data = sorted(menu_res, key=lambda s: s['id'])
        return Response(menus_data)

    @action(detail=True, methods=['put'], url_path='assign_menu')
    def assign_menu(self, request, pk):
        """
        给菜单栏赋权限
        :param request:
        :param pk:
        :return:
        """
        # 查询所有菜单栏
        menus = Menu.objects.get_queryset().filter(is_delete=0).all()
        menus_serializer = MenuSerializer(menus, many=True).data
        # 查询需要附权的菜单栏
        menu_ids = request.data.get("menus")
        role_menu = Menu.objects.get_queryset().filter(id__in=menu_ids, is_delete=0).all()
        role_menu_serializer = MenuSerializer(role_menu, many=True).data
        # 附权子菜单及其父菜单
        for x in role_menu_serializer:
            if x['p_id'] not in menu_ids and x['p_id'] != 0:
                role_menu_serializer.extend(filter(lambda m: m['id'] == x['p_id'], menus_serializer))
                menu_ids.append(x['p_id'])
        # 附权
        role = self.get_object()
        role_menu_new = Menu.objects.get_queryset().filter(id__in=menu_ids, is_delete=0).all()
        for menu in role_menu_new:
            role.menus.add(menu)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='remove_menu')
    def remove_menu(self, request, pk):
        """
        取消菜单栏权限
        :param request:
        :param pk:
        :return:
        """
        menu_ids = request.data.get("menus")
        role = self.get_object()
        menus = Menu.objects.filter(id__in=menu_ids).all()
        for menu in menus:
            role.menus.remove(menu)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        # 查询条件
        name = request.query_params.get('name', None)
        # 查询数据
        if name:
            role_list = Role.objects.get_queryset().filter(name__icontains=name, is_delete=0).order_by('id')
        else:
            role_list = Role.objects.get_queryset().filter(is_delete=0).order_by('id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(role_list, pre_page)
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
            return Response(self.get_serializer(role_list, many=True).data)

    @action(detail=False, methods=['put'])
    def delete(self, request):
        roles_id = request.data.get('ids', None)
        roles = Role.objects.filter(id__in=roles_id).update(is_delete=1, remove_time=datetime.datetime.now())
        return Response(roles)


class MenuViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def create(self, request, *args, **kwargs):
        """
        系统内添加菜单栏,
        :param request:
        :param args:
        :param kwargs:
        :return: HTTP Response
        """
        form_data = request.data
        menus = Menu.objects.filter(name=form_data.get('name'), menu_type=form_data.get('menu_type'),
                                    application=form_data.get('application'), is_delete=0).all()
        if len(menus) == 0:
            if form_data.get('menu_type') == 'dir':
                form_data['p_id'] = 0
            else:
                prev_menu = form_data.get('prev_menu')
                app = form_data.get('application')
                menu = Menu.objects.get(name=prev_menu, application=app, is_delete=0)
                form_data['p_id'] = menu.id
            return super().create(request, *args, form_data)
        else:
            result = {'msg': '资源已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

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
        pid = request.query_params.get('p_id', None)
        menu_type = request.query_params.get('type', None)
        # 查询数据
        if pid:
            search_dict['p_id'] = pid
        if menu_type:
            search_dict['menu_type'] = menu_type
        menu_list = Menu.objects.get_queryset().filter(**search_dict, is_delete=0).order_by('id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(menu_list, pre_page)
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
            return Response(self.get_serializer(menu_list, many=True).data)

    @action(detail=False)
    def app_list(self, request):
        menus = Menu.objects.get_queryset().filter(is_delete=0).all()
        menus_serializer = MenuSerializer(menus, many=True).data
        app_list = list()
        for menu in menus_serializer:
            if menu['application'] not in app_list:
               app_list.append(menu['application'])
        return Response(app_list)

    @action(detail=False, methods=['put'])
    def delete(self, request):
        menus_id = request.data.get('ids', None)
        menus = Menu.objects.filter(id__in=menus_id).update(is_delete=1, remove_time=datetime.datetime.now())
        return Response(menus)
