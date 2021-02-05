from rest_framework import viewsets, status
from django.core.paginator import Paginator
from sys_auth.views import MyAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime
import json
from huaweiyun.helper.huaweiyun import *
from huaweiyun.models import HuaweiyunManager
from huaweiyun.serializers import HuaweiyunManagerSerializer


class HuaweiyunViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = HuaweiyunManager.objects.all()
    serializer_class = HuaweiyunManagerSerializer

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        huaweiyun_list = HuaweiyunManager.objects.get_queryset().order_by('id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(huaweiyun_list, pre_page)
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
            return Response(self.get_serializer(huaweiyun_list, many=True).data)

    def create(self, request, *args, **kwargs):
        huaweiyuns = HuaweiyunManager.objects.filter(hw_address=request.data.get('address'), hw_username=request.data.get('username')).all()
        if len(huaweiyuns) == 0:
            return super().create(request, *args, **kwargs)
        else:
            result = {'msg': '资源已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        request.data['update_time'] = datetime.datetime.now()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def format_tree_data(self, data):
        new_value = list()
        for info in data:
            temp = {'label': info.pop('name'), 'urn': info.pop('urn')}
            new_value.append(temp)
        return new_value

    def get_huawei_env(self, request):
        huawei_env = request.headers.get('env')
        if not huawei_env:
            return False
        huawei_env = json.loads(huawei_env)
        huawei_env['Host'] = request.headers.get('Host')
        return huawei_env

    @action(methods=['get'], detail=False, url_path='sites')
    def get_sites(self, request):
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWSite.get_fusion_compute_sites(huawei_env)
        if status_code == 500:
            return Response(res, status=status_code)
        else:
            res['sites'] = self.format_tree_data(res['sites'])
            return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='clusters')
    def get_clusters(self, request):
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWCluster.get_fusion_compute_clusters(huawei_env)
        if status_code == 500:
            return Response(res, status=status_code)
        else:
            res['clusters'] = self.format_tree_data(res['clusters'])
            return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='hosts')
    def get_cluster_host(self, request):
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        scope = request.query_params.get('scope')
        status_code, res = HWHost.get_fusion_compute_hosts(huawei_env, scope)
        if status_code == 500:
            return Response(res, status=status_code)
        else:
            res['hosts'] = self.format_tree_data(res['hosts'])
            return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='vms')
    def get_vms(self, request):
        """
        查询虚拟机信息
        :param request:
        :return:
        """
        template = request.query_params.get('Template')
        name = request.query_params.get('name')
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWVms.get_fusion_compute_vms(huawei_env, template, name)
        return Response(res, status=status_code)

    @action(methods=['post'], detail=False, url_path='create_vms')
    def create_vms(self, request):
        """
        创建虚拟机
        :param request:
        :return:
        """
        vms_info = request.data
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWVms.create_fusion_compute_vms(huawei_env, vms_info)
        return Response(res, status=status_code)

    @action(methods=['post'], detail=False, url_path='clone_vms')
    def clone_vms(self, request):
        """
        克隆虚拟机
        :param request:
        :return:
        """
        vms_id = request.query_params.get('id')
        vms_info = request.data
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWVms.clone_fusion_compute_vms(huawei_env, vms_id, vms_info)
        return Response(res, status=status_code)

    @action(methods=['delete'], detail=False, url_path='delete_vms')
    def delete_vms(self, request):
        """
        删除虚拟机
        :param request:
        :return:
        """
        vms_id = request.query_params.get('id')
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWVms.delete_fusion_compute_vms(huawei_env, vms_id)
        return Response(res, status=status_code)

    @action(methods=['post'], detail=False, url_path='stop_vms')
    def stop_vms(self, request):
        """
        停止虚拟机
        :param request:
        :return:
        """
        vms_id = request.query_params.get('id')
        data = request.data
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWVms.stop_fusion_compute_vms(huawei_env, vms_id, data)
        return Response(res.json(), status=status_code)

    @action(methods=['post'], detail=False, url_path='start_vms')
    def start_vms(self, request):
        """
        开启虚拟机
        :param request:
        :return:
        """
        vms_id = request.query_params.get('id')
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWVms.start_fusion_compute_vms(huawei_env, vms_id)
        return Response(res.json(), status=status_code)

    @action(methods=['get'], detail=False, url_path='vms/osversions')
    def get_os_version(self, request):
        """
        查询虚拟机操作系统信息
        :param request:
        :return:
        """
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWVms.get_fusion_compute_os_versions(huawei_env)
        if status_code == 500:
            return Response(res, status=status_code)
        else:
            for key, value in res.items():
                value_lis = list()
                for os in value:
                    value_lis.append({'os_version': os['versionDes'], 'os_id': os['id']})
                res[key] = value_lis
            return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='datastores')
    def get_datastore(self, request):
        """
        查询数据存储信息
        :param request:
        :return:
        """
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWDatastore.get_fusion_compute_datastore(huawei_env)
        return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='dvswitch')
    def get_dv_switch(self, request):
        """
        查询分布式交换机信息
        :param request:
        :return:
        """
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWDvSwitch.get_fusion_compute_dv_switch(huawei_env)
        return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='portgroups')
    def get_port_group(self, request):
        """
        查询端口组信息
        :param request:
        :return:
        """
        port_group_num = request.query_params.get('portGroupNum')
        huawei_env = huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWDvSwitch.get_fusion_compute_port_group(huawei_env, port_group_num)
        return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='queryVfdFiles')
    def get_vfd_file(self, request):
        """
        查询软驱信息
        :param request:
        :return:
        """
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWVfdFile.get_fusion_compute_vfd_file(huawei_env)
        if status_code == 500:
            return Response(res, status=status_code)
        else:
            res['VfdFiles'].insert(0, '自动匹配')
            res['VfdFiles'].insert(1, '不挂载')
            return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='vncKeymapSettings')
    def get_key_board(self, request):
        """
        查询键盘配置信息
        :param request:
        :return:
        """
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWVncKeyboard.get_fusion_compute_vnc_keyboard(huawei_env)
        if status_code == 500:
            return Response(res, status=status_code)
        else:
            for setting in res['vmVncKeymapSettings']:
                if setting['vncKeymapDes'] == 'English (US)':
                    setting['vncKeymapDesCh'] = '英语（美国）'
                elif setting['vncKeymapDes'] == 'French':
                    setting['vncKeymapDesCh'] = '法语'
                elif setting['vncKeymapDes'] == 'German':
                    setting['vncKeymapDesCh'] = '德语'
                elif setting['vncKeymapDes'] == 'Italian':
                    setting['vncKeymapDesCh'] = '意大利语'
                elif setting['vncKeymapDes'] == 'Russian':
                    setting['vncKeymapDesCh'] = '俄语'
                elif setting['vncKeymapDes'] == 'Spanish':
                    setting['vncKeymapDesCh'] = '西班牙语'
            return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='network')
    def get_network(self, request):
        """
        查询网络信息
        :param request:
        :return:
        """
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWNetwork.get_fusion_compute_network(huawei_env)
        return Response(res, status=status_code)

    @action(methods=['get'], detail=False, url_path='securitygroups')
    def get_security_group(self, request):
        """
        查询安全组信息
        :param request:
        :return:
        """
        huawei_env = self.get_huawei_env(request)
        if not huawei_env:
            res = {'msg': '未发现华为私有云环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        status_code, res = HWSecurityGroup.get_fusion_compute_security_group(huawei_env)
        return Response(res, status=status_code)


