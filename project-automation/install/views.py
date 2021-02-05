import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from install.models import PxeServerOs, PxeServer, JobCheck, JobInstall, Port
from install.serializers import PxeServerSerializer, PxeServerOsSerializer, \
    JobCheckSerializer, JobInstallSerializer, PmPortSerializer
import datetime
from django.core.paginator import Paginator
import os
import xlrd
import urllib.request
import urllib.parse
import conf
import json
from django.forms.models import model_to_dict
from sys_auth.views import MyAuthentication
from django.db.models import Max
from concurrent import futures
import time

logger = logging.getLogger('log')
basedir = os.path.abspath(os.path.dirname(__file__))


class PxeServerViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = PxeServer.objects.all()
    serializer_class = PxeServerSerializer

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
        pxe_name = request.query_params.get('pxe_name', None)
        if pxe_name:
            search_dict['pxe_name'] = pxe_name
        pxe_server_ip = request.query_params.get('pxe_server_ip', None)
        if pxe_server_ip:
            search_dict['pxe_server_ip'] = pxe_server_ip
        ifenable = request.query_params.get("ifenable", None)
        if ifenable:
            search_dict['ifenable'] = ifenable
        search_dict['is_delete'] = 0
        pxe_server_info = PxeServer.objects.get_queryset().filter(
            **search_dict).order_by('-create_time')
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(pxe_server_info, pre_page)
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
            return Response(
                self.get_serializer(pxe_server_info, many=True).data)

    def create(self, request, *args, **kwargs):
        pxe_name = request.data.get("pxe_name", None)
        pxe_server_ip = request.data.get("pxe_server_ip", None)
        pxe_name_info = PxeServer.objects.filter(pxe_name=pxe_name,
                                                 is_delete=0).all()
        pxe_ip_info = PxeServer.objects.filter(pxe_server_ip=pxe_server_ip,
                                               is_delete=0).all()
        if len(pxe_name_info) == 0 and len(pxe_ip_info) == 0:
            return super().create(request, *args, **kwargs)
        else:
            result = {'msg': '资源已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        pxe_name = request.data.get("pxe_name", None)
        pxe_server_ip = request.data.get("pxe_server_ip", None)
        pxe_id = request.data.get('id', None)
        pxe_name_info = PxeServer.objects.filter(pxe_name=pxe_name,
                                                 is_delete=0).first()
        pxe_ip_info = PxeServer.objects.filter(pxe_server_ip=pxe_server_ip,
                                               is_delete=0).first()
        if (pxe_name_info and pxe_id != pxe_name_info.id) or (pxe_ip_info and
                                                              pxe_id != pxe_ip_info.id):
            result = {'msg': '名称或ip有重复'}
            return Response(result, status=status.HTTP_409_CONFLICT)
        else:
            return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pxe_server = self.get_object()
        pxe_server.is_delete = 1
        pxe_server.remove_time = datetime.datetime.now()
        pxe_server.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST'])
    def upload_excel(self, request):
        headers = request.headers
        excel_obj = request.data.get("file", "")
        pxe_server_id = request.data.get("pxe_server_id", None)
        os_id = request.data.get("os_id", None)
        usage = request.data.get("usage", None)
        filename = request.data.get("file_name", None)
        logger.info(request.data)
        if filename and '.' in filename and filename.rsplit('.', 1)[
            1] == "xls":
            excel_data = xlrd.open_workbook(filename=None,
                                            file_contents=excel_obj.read(),
                                            formatting_info=True)
        elif filename and '.' in filename and filename.rsplit('.', 1)[
            1] == 'xlsx':
            excel_data = xlrd.open_workbook(filename=None,
                                            file_contents=excel_obj.read())
        else:
            result = {'msg': '文件格式错误'}
            return Response(result, status=status.HTTP_412_PRECONDITION_FAILED)
        pxe_info = PxeServer.objects.get(id=pxe_server_id)
        logger.info(pxe_info)
        os_info = {}
        if os_id:
            os_info = PxeServerOs.objects.get(id=os_id)
            os_info = model_to_dict(os_info,
                                    exclude=["is_delete", "create_time",
                                             "remove_time", 'ks_content'])
            logger.info(os_info)
        res_list, hostname_list = self.analytical_field(excel_data, pxe_server_id, pxe_info, os_id, os_info)
        if hostname_list:
            logger.info(hostname_list)
            type_ = "服务器"
            params = json.dumps(
                {"hostname_list": hostname_list, "device_type": type_})
            params = bytes(params, 'utf8')
            try:
                url = conf.ASSET_URL + "device/hostname_list/"
                logger.info(url)
                headers = {"token": headers.get("Token"),
                    'content-type': 'application/json'}
                logger.info(headers)
                req = urllib.request.Request(url, data=params, headers=headers, method="POST")
                response = urllib.request.urlopen(req)
                device_infos = json.loads(response.read())
                logger.info(device_infos)
                # 装机
                if device_infos and os_id:
                    for res in res_list:
                        port_info = {}
                        # 查询最新的数据
                        job_check_obj = JobCheck.objects.filter(
                            hostname=res.get("hostname")).last()
                        if job_check_obj:
                            job_check_status = job_check_obj.status
                            if job_check_status != "FAILURE":
                                save_time = job_check_obj.create_time
                                now_time = datetime.datetime.now()
                                time_ = (now_time - save_time).days
                                if time_ > 29:
                                    port_info['status'] = 10002  # 端口检查过期
                                    res.update(port_info)
                                    continue
                                ports = job_check_obj.job_check.all()
                                logger.info(ports)
                                if 0 == len(ports):
                                    port_info['status'] = 10001  # 正在端口检查
                                    res.update(port_info)
                                    continue
                                port_list = []
                                for port in ports:
                                    port_list.append(model_to_dict(port))
                                port_info['port'] = port_list
                                port_info['status'] = 10000
                                res.update(port_info)
                            else:
                                port_info['status'] = 10003  # 端口检查失败
                                res.update(port_info)
                        else:
                            port_info['status'] = 10004  # 未端口检查
                            res.update(port_info)
                        for i, device in enumerate(device_infos):
                            if device.get("hostname") == res.get("hostname"):
                                res.update(device)
                                if usage:
                                    res['usage'] = usage
                                device_infos.pop(i)
                                break
                # 端口检查
                if device_infos:
                    for res in res_list:
                        for i, device in enumerate(device_infos):
                            if device.get("hostname") == res.get("hostname"):
                                res.update(device)
                                device_infos.pop(i)
                                break
                logger.info(res_list)
            except Exception as e:
                logger.error(e)
        return Response(res_list)

    @staticmethod
    def analytical_field(excel_data, pxe_server_id, pxe_info, os_id, os_info):
        table = excel_data.sheets()[0]  # 打开第一张表
        nrows = table.nrows
        res_list = []
        hostname_list = list()
        for row in range(1, nrows):
            res_dict = dict()
            if 1 == table.ncols:
                res_dict['hostname'] = table.cell(row, 0).value
            else:
                res_dict['ip'] = table.cell(row, 0).value
                res_dict['hostname'] = table.cell(row, 1).value
                res_dict['device_netmask'] = table.cell(row, 2).value
                res_dict['device_gateway'] = table.cell(row, 3).value
            if pxe_server_id and pxe_info:
                res_dict['pxe_server_ip'] = pxe_info.pxe_server_ip
                res_dict['ipmi_server_ip'] = pxe_info.ipmi_server_ip
            if res_dict['hostname']:
                hostname_list.append(res_dict['hostname'])
            if os_id and os_info:
                res_dict.update(os_info)
            res_list.append(res_dict)
        return res_list, hostname_list


class PxeServerOsViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = PxeServerOs.objects.all()
    serializer_class = PxeServerOsSerializer

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
        pxe_server_ip = request.query_params.get("pxe_server_id", None)
        if pxe_server_ip:
            search_dict['pxe_server_id'] = pxe_server_ip
        else:
            result = {'msg': "参数不完整"}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        ifenable = request.query_params.get("ifenable", None)
        if ifenable:
            search_dict['ifenable'] = ifenable
        search_dict['is_delete'] = 0
        pxe_server_os_info = PxeServerOs.objects.get_queryset().filter(
            **search_dict).order_by('-create_time')
        return Response(
            self.get_serializer(pxe_server_os_info, many=True).data)

    def create(self, request, *args, **kwargs):
        os_name = request.data.get("os_name", None)
        pxe_server_id = request.data.get("pxe_server_id", None)
        pxe_name_info = PxeServerOs.objects.filter(os_name=os_name,
                                                   pxe_server_id=pxe_server_id,
                                                   is_delete=0).all()
        if len(pxe_name_info) == 0:
            return super().create(request, *args, **kwargs)
        else:
            result = {'msg': '资源已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        os_name = request.data.get("os_name", None)
        pxe_server_id = request.data.get("pxe_server_id", None)
        os_id = request.data.get('id', None)
        pxe_os_info = PxeServerOs.objects.filter(os_name=os_name,
                                                 pxe_server_id=pxe_server_id,
                                                 is_delete=0).first()

        if os_name and pxe_os_info and os_id != pxe_os_info.id:
            result = {'msg': '名称或ip有重复'}
            return Response(result, status=status.HTTP_409_CONFLICT)
        else:
            return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        os_info = self.get_object()
        os_info.is_delete = 1
        os_info.remove_time = datetime.datetime.now()
        os_info.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST'])
    def allpxeos(self, request):
        data = request.data
        for os in data:
            pxe_server_id = os.get('pxe_server_id')
            profile_ks_content_list = os.get("profile_ks_content_list")
            for profile_ks_content in profile_ks_content_list:
                profile = profile_ks_content.get("profile")
                if not profile:
                    continue
                profile = profile.replace(" ", "")
                ks_content = profile_ks_content.get("ks_content")
                PxeServerOs.objects.update_or_create(profile=profile,
                                                     pxe_server_id=pxe_server_id,
                                                     is_delete=0,
                                                     defaults={
                                                         "pxe_server_id": pxe_server_id,
                                                         "profile": profile,
                                                         "ks_content": ks_content})
        return Response({'msg': "添加成功"}, status=status.HTTP_201_CREATED)


class JobCheckViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = JobCheck.objects.all()
    serializer_class = JobCheckSerializer

    def create(self, request):
        headers = request.headers
        headers = {"token": headers.get("Token"),
                   'Content-Type': 'application/json'}
        headers.update({'Content-Type': 'application/json'})
        data_list = request.data
        list_ = []
        list_info = []
        for data in data_list:
            dict_ = {}
            dict_['device_name'] = data.get("device_name", None)
            dict_['hostname'] = data.get("hostname", None)
            dict_['sn'] = data.get("device_sn", None)
            dict_['status'] = "REBOOTING"
            dict_['usage'] = data.get("usage", None)
            dict_['location'] = data.get("location_zone", None)
            dict_['console_ip'] = data.get("manage_address", None)
            dict_['console_user'] = data.get("manage_username", None)
            dict_['console_password'] = data.get("manage_password", None)
            dict_['ipmi_server_ip'] = data.get("ipmi_server_ip", None)
            dict_['pxe_server_ip'] = data.get("pxe_server_ip", None)
            list_.append(JobCheck(**dict_))
            list_info.append(dict_)
        JobCheck.objects.bulk_create(list_)
        logger.info(list_info)
        executor = futures.ThreadPoolExecutor(max_workers=30)
        for data in list_info:
            try:
                logger.info(" 开始异步执行")
                executor.submit(self.ipmitool, data, headers)
            except Exception as e:
                logger.error(e)
        return Response({"msg": '正在重启,请查看日志'})

    @staticmethod
    def ipmitool(data, headers):
        try:
            ipmi_url = f"http://{data['ipmi_server_ip']}:8002/ipmitool/api/ipmi/"
            logger.info("ipmitool_url: " + ipmi_url)
            params = json.dumps(data)
            params = bytes(params, 'utf8')
            req = urllib.request.Request(ipmi_url, data=params, headers=headers,
                                         method="POST")
            response = urllib.request.urlopen(req)
            ipmi_infos = response.read()
            ipmi_infos = json.loads(ipmi_infos)
            logger.info(ipmi_infos)
        except Exception as e:
            logger.error(e)

    def list(self, request, *args, **kwargs):
        search_dict = dict()
        sn = request.query_params.get('sn', None)
        if sn:
            search_dict['sn'] = sn
        device_name = request.query_params.get('device_name', None)
        if device_name:
            search_dict['device_name'] = device_name
        hostname = request.query_params.get('hostname', None)
        if hostname:
            search_dict['hostname'] = hostname
        status = request.query_params.get('status', None)
        if status:
            search_dict['status'] = status
        pxe_server_ip = request.query_params.get('pxe_server_ip', None)
        if pxe_server_ip:
            search_dict['pxe_server_ip'] = pxe_server_ip

        date = (
            (datetime.datetime.now() - datetime.timedelta(minutes=30)).strftime(
                "%Y-%m-%d %H:%M:%S"))
        JobCheck.objects.filter(status="REBOOTING", update_time__lt=date
                                ).update(status='FAILURE')
        job_check_info = JobCheck.objects.get_queryset().filter(**search_dict
                                                                ).order_by(
            '-update_time')
        logger.info(job_check_info)

        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(job_check_info, pre_page)
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
            return Response(
                self.get_serializer(job_check_info, many=True).data)


class JobInstallViewSet(viewsets.ModelViewSet):
    # authentication_classes = [MyAuthentication, ]
    queryset = JobInstall.objects.all()
    serializer_class = JobInstallSerializer

    def list(self, request, *args, **kwargs):
        search_dict = dict()
        sn = request.query_params.get('sn', None)
        if sn:
            search_dict['sn'] = sn
        device_name = request.query_params.get('device_name', None)
        if device_name:
            search_dict['device_name'] = device_name
        hostname = request.query_params.get('hostname', None)
        if hostname:
            search_dict['hostname'] = hostname
        status = request.query_params.get('status', None)
        if status:
            search_dict['status'] = status
        pxe_server_ip = request.query_params.get('pxe_server_ip', None)
        if pxe_server_ip:
            search_dict['pxe_server_ip'] = pxe_server_ip
        # 超过1个小时装机的默认失败
        date = (
            (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime(
                "%Y-%m-%d %H:%M:%S"))
        JobInstall.objects.filter(install=None, status="INSTALLING",
                                  update_time__lt=date).update(install=1)
        job_install_info = JobInstall.objects.get_queryset().filter(
            **search_dict
            ).order_by('-update_time')
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(job_install_info, pre_page)
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
            return Response(
                self.get_serializer(job_install_info, many=True).data)

    def create(self, request, *args, **kwargs):
        headers = request.headers
        headers = {"token": headers.get("Token"),
                   'Content-Type': 'application/json'}
        headers.update({'Content-Type': 'application/json'})
        data_list = request.data
        logger.info(data_list)
        # 保存job install
        job_install_list = self.save_job_install(data_list)
        executor = futures.ThreadPoolExecutor(max_workers=30)
        for install_info in job_install_list:
            try:
                logger.info(" 开始异步执行")
                executor.submit(self.pm_install, install_info, headers)
            except Exception as e:
                logger.error(e)
        return Response({"msg": '正在装机，请查看日志'})

    @staticmethod
    def save_job_install(data_list):
        list_ = []
        list_info = []
        for data in data_list:
            dict_ = {}
            dict_['device_name'] = data.get("device_name", None)
            dict_['sn'] = data.get('device_sn', None)
            dict_['status'] = "WAITING"
            dict_['ip'] = data.get('ip', None)
            dict_['gateway'] = data.get('device_gateway', None)
            dict_['netmask'] = data.get('device_netmask', None)
            dict_['hostname'] = data.get('hostname', None)
            dict_['usage'] = data.get('usage', None)
            dict_['location'] = data.get('location_zone', None)
            dict_['type'] = data.get("type", None)
            dict_['console_ip'] = data.get("manage_address", None)
            dict_['console_user'] = data.get('manage_username', None)
            dict_['console_password'] = data.get('manage_password', None)
            dict_['ipmi_server_ip'] = data.get('ipmi_server_ip', None)
            dict_['os_name'] = data.get('os_name', None)
            dict_['os_version'] = data.get('os_version', None)
            dict_['ks_name'] = data.get("ks_name", None)
            dict_['profile'] = data.get('profile', None)
            dict_['pxe_server_ip'] = data.get('pxe_server_ip', None)
            dict_['mac'] = data.get('mac', [])
            dict_['ifname'] = data.get('ifname', [])
            list_.append(JobInstall(**dict_))
            list_info.append(dict_)
        JobInstall.objects.bulk_create(list_)
        return list_info

    def pm_install(self, install_info, headers):
        # 检查sn
        job_install = JobInstall.objects.filter(
            sn=install_info.get('sn')).last()
        check_sn_res = self.check_sn(install_info, headers)
        if check_sn_res.get('check_result') == 1:
            # 绑定mac地址
            bind_mac_res = self.bind_mac(install_info, headers)
            if len(bind_mac_res):
                job_install.status = 'INSTALLING'
                job_install.save()
                self.reboot_machine(install_info, headers)
                return Response({"msg": "服务器正在重启"})
            else:
                job_install.status = "MACERROR"
                job_install.install = 1
                job_install.save()
                logger.error({"msg": "绑定mac失败"})
                return Response({"msg": "绑定mac失败"})
        else:
            job_install.status = check_sn_res.get('msg')
            job_install.install = 1
            job_install.save()
            logger.error({"msg": "资源检查失败"})
            return Response({"msg": "资源检查失败"})

    @staticmethod
    def check_sn(install_info, headers):
        """
        检查sn
        :param install_info:
        :param headers:
        :return:
        """
        logger.info(f"检查sn:{install_info.get('sn')}")
        check_sn_res = {}
        try:
            check_url = f"http://{install_info.get('ipmi_server_ip')}:8002/ipmitool/api/checksn/" \
                        f"?sn={install_info.get('sn')}&console_ip={install_info.get('console_ip')}&" \
                        f"console_user={install_info.get('console_user')}&console_password={install_info.get('console_password')}"
            logger.info("check_url" + check_url)
            req = urllib.request.Request(check_url, headers=headers)
            response = urllib.request.urlopen(req)
            check_sn_res = json.loads(response.read())
            logger.info(check_sn_res)
        except Exception as e:
            logger.error(e)
        finally:
            return check_sn_res

    @staticmethod
    def bind_mac(install_info, headers):
        res = []
        try:
            logger.info(install_info.get('mac'))
            for mac in install_info.get('mac'):
                bind_url = f"http://{install_info.get('pxe_server_ip')}:8001/pxeserver/api/addsystem/"
                logger.info(bind_url)
                bind_param = {'mac': mac,
                              'ks_name': install_info.get('ks_name'),
                              'profile': install_info.get('profile')}
                params = json.dumps(bind_param)
                params = bytes(params, 'utf8')
                req = urllib.request.Request(bind_url, data=params,
                                             headers=headers, method="POST")
                response = urllib.request.urlopen(req)
                data = json.loads(response.read())
                logger.info(response)
                if data and 10000 == int(data.get('status')):
                    res.append(data)
        except Exception as e:
            logger.error(e)
        finally:
            logger.info(res)
            return res

    @staticmethod
    def reboot_machine(install_info, headers):
        try:
            os_url = f"http://{install_info.get('ipmi_server_ip')}:8002/ipmitool/api/ipmi/"
            params = json.dumps(install_info)
            params = bytes(params, 'utf8')
            req = urllib.request.Request(os_url, data=params, headers=headers,
                                         method="POST")
            response = urllib.request.urlopen(req)
            os_infos = response.read()
            os_infos = json.loads(os_infos)
            logger.info(os_infos)
        except Exception as e:
            logger.error(e)

    @action(detail=False, methods=['GET'])
    def call_snip(self, request):
        sn = request.query_params.get('sn', None)
        ip = request.query_params.get('ip', None)
        job_install = JobInstall.objects.filter(sn=sn, status="INSTALLING").order_by('-update_time').first()
        logger.info(job_install)
        if not job_install:
            return Response({"msg": "私网ip保存失败"})
        if not ip:
            job_install.install_ip = ip
            job_install.status = "IPNOTFOUND"
            job_install.install = 1
            job_install.save()
            return Response({"msg": "私网ip未获得"})
        job_install.install_ip = ip
        job_install.status = "COMPLETE"
        job_install.save()
        logger.info("删除绑定的mac")
        self.removemac_cobbler(job_install)
        try:
            logger.info("准备配置hostname和ip")
            executor = futures.ThreadPoolExecutor(max_workers=1)
            executor.submit(self.config_ip, sn, ip)
        except Exception as e:
            logger.error(e)
            return Response({"msg": "执行错误"})
        finally:
            return Response({"msg": "执行成功"})

    def config_ip(self, sn, ip):
        num_ = 0
        job_install = JobInstall.objects.filter(sn=sn,
                                                status="COMPLETE").order_by(
            '-update_time').first()
        # 检查ping的结果
        logger.info("开始执行check_ping")
        while num_ <= 20:
            logger.info(num_)
            time.sleep(60)
            check_ping = self.check_ping(job_install, ip)
            logger.info(check_ping)
            if check_ping.get("status") and 10000 == int(
                    check_ping.get('status')):
                logger.info("ping成功")
                break
            if num_ == 20:
                job_install.status = "BOOTERROR"
                job_install.install = 1
                job_install.save()
                logger.error("物理机重启失败")
                return Response({"msg": "物理机重启失败"})
            num_ += 1
        # time.sleep(50)
        logger.info("开始修改ip和hostname")
        ping_check = self.modify_ip(job_install, ip)
        if ping_check.get("status") and 10000 == int(ping_check.get('status')):
            job_install.status = "SUCCESS"
            job_install.install = 0
            job_install.save()
            logger.info("装机成功")
            return Response({"msg": "装机成功"})
        else:
            job_install.status = "IPCONFIGERROR"
            job_install.install = 1
            job_install.save()
            logger.error("配置ip失败")
            return Response({"msg": "配置ip失败"})

    @staticmethod
    def removemac_cobbler(job_install):
        macs = job_install.mac
        pxe_server_ip = job_install.pxe_server_ip
        remove_mac_url = f"http://{pxe_server_ip}:8001/pxeserver/api/removemac/"
        try:
            logger.info("remove_mac_url:" + remove_mac_url)
            headers = {'Content-Type': 'application/json'}
            params = json.dumps(macs)
            params = bytes(params, 'utf8')
            req = urllib.request.Request(remove_mac_url, data=params,
                                         headers=headers, method="POST")
            response = urllib.request.urlopen(req)
            data = json.loads(response.read())
            logger.info(data)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def check_ping(job_install, ip):
        check_ping_res = {}
        try:
            pxe_server_ip = job_install.pxe_server_ip
            check_ping_url = f"http://{pxe_server_ip}:8001/pxeserver/api/checkping/?ip={ip}"
            logger.info('check_ping_res:' + check_ping_url)
            req = urllib.request.Request(check_ping_url)
            response = urllib.request.urlopen(req)
            check_ping_res = json.loads(response.read())
            logger.info(check_ping_res)
        except Exception as e:
            logger.error(e)
        finally:
            return check_ping_res

    @staticmethod
    def modify_ip(job_install, ip):
        data = {}
        try:
            param = dict()
            param['ip'] = job_install.ip
            param['hostname'] = job_install.hostname
            param['gateway'] = job_install.gateway
            param['netmask'] = job_install.netmask
            param['mac'] = job_install.mac
            pxe_server_ip = job_install.pxe_server_ip
            modify_url = f"http://{pxe_server_ip}:8001/pxeserver/api/configip/?ip={ip}"
            logger.info("modify_url:" + modify_url)
            headers = {'Content-Type': 'application/json'}
            params = json.dumps(param)
            params = bytes(params, 'utf8')
            req = urllib.request.Request(modify_url, data=params,
                                         headers=headers, method="POST")
            response = urllib.request.urlopen(req)
            data = json.loads(response.read())
            logger.info(data)
        except Exception as e:
            logger.error(e)
        finally:
            return data


class PmPortViewSet(viewsets.ModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PmPortSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        logger.info(data)
        sn = data.get("sn", None)
        job_check = JobCheck.objects.filter(sn=sn.strip()).order_by("-update_time").first()
        logger.info(job_check)
        if job_check:
            if job_check.status == "COMPLETE":
                return Response({"msg": "端口信息已保存"})
            job_check.status = "COMPLETE"
            job_check.save()
            port_list = []
            if data.get('nics'):
                for info in data['nics']:
                    switch = info.get("switch")
                    port = info.get("port")
                    vlan = info.get("vlan")
                    mac = info.get("mac")
                    ifname = info.get("ifname")
                    port_list.append(Port(switch=switch, port=port, vlan=vlan,
                                          mac=mac, ifname=ifname,
                                          job_check=job_check))
                Port.objects.bulk_create(port_list)
            return Response({"msg": "端口检查结果保存成功"})
        else:
            return Response({"msg": "端口检查失败"})