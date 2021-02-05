import json
import hashlib
import requests
import urllib3
import logging
from django.core.cache import cache
from huaweiyun.helper.http import HttpHelper
from conf import *

logger = logging.getLogger('log')
urllib3.disable_warnings()

class HuaweiyunConnectionMng(object):

    def login_huawei_fusion_compute(self, huawei_env):
        try:
            url = huawei_env.get('hw_address') + LOGIN_URI
            passwd_sha = hashlib.sha256(huawei_env.get('hw_password').encode('utf-8')).hexdigest()
            headers = {
                "Accept-Language": "zh_CN",
                "X-ENCRIPT-ALGORITHM": "0",
                "X-Auth-UserType": "0",
                "X-Auth-User": huawei_env.get('hw_username'),
                "X-Auth-Key": passwd_sha,
                "Content-Type": "application/json; charset=UTF-8",
                "Accept": "application/json;version=v6.3;charset=UTF-8"
            }
            res = requests.post(url=url, headers=headers, verify=False, timeout=60)
            result = res.json()
            res_headers = res.headers
            result['token'] = res_headers['X-Auth-Token']
            # 将token存cache
            cache.set(huawei_env.get('Host') + huawei_env.get('hw_address') + huawei_env.get('hw_username') + 'token', res_headers['X-Auth-Token'], 60)
            cache.expire(huawei_env.get('Host') + huawei_env.get('hw_address') + huawei_env.get('hw_username') + 'token', 600)
            return result
        except Exception as e:
            logger.info("华为云登录失败:{error}！".format(error=e))

    def common_headers(self, huawei_env):
        try:
            token = cache.get(huawei_env.get('Host') + huawei_env.get('hw_address') + huawei_env.get('hw_username') + 'token')
        except Exception as e:
            token = None
            logger.info("token获取失败:{error}, 正在重新登录".format(error=e))
        if token:
            token = token
        else:
            info = self.login_huawei_fusion_compute(huawei_env)
            if info:
                token = info['token']
        if token:
            headers = {
                "X-Auth-Token": token,
                "Content-Type": "application/json; charset=UTF-8",
                "Accept": "application/json;version=v6.3;charset=UTF-8"
            }
        else:
            headers = {}
        return headers

class HWSite(object):

    @staticmethod
    def get_fusion_compute_sites(huawei_env):
        """
        查询站点信息
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

class HWCluster(object):

    @staticmethod
    def get_fusion_compute_clusters(huawei_env, site_id='3CE206C5'):
        """
        查询集群信息
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/clusters'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

class HWHost(object):
    @staticmethod
    def get_fusion_compute_hosts(huawei_env, scope=None, site_id='3CE206C5'):
        """
        查询主机信息
        :return:
        """
        if scope:
            url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/hosts?scope=' + scope
        else:
            url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/hosts'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

class HWVms(object):

    @staticmethod
    def get_fusion_compute_vms(huawei_env, template, name, site_id='3CE206C5'):
        """
        查询虚拟机信息
        :param request:
        :return:
        """
        # hw_sites = HWSite.get_fusion_compute_sites(huawei_env)
        # site_uri_list = hw_sites['sites'][0]['uri'].split('/')
        # site_id = site_uri_list[-1]
        if name:
            url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms?detail=2&isTemplate=' + template + '&name=' + name
        # url = 'https://172.16.1.95:7443/service/sites/3CE206C5/vms?detail=2&isTemplate=false&' \
        #       'queryFlag=normal&orderField=name&order=DESC&limit=15&offset=0&noCache=1598507550177'
        else:
            url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms?detail=2&isTemplate=' + template
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

    @staticmethod
    def create_fusion_compute_vms(huawei_env, data, site_id='3CE206C5'):
        """
        创建虚拟机
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.post(url, headers, json.dumps(data))
        return code, res

    @staticmethod
    def clone_fusion_compute_vms(huawei_env, vms_id, data, site_id='3CE206C5'):
        """
        模板创建虚拟机
        :param request:
        :return:
        """
        if data.get('vmSize') and data['vmSize']>1:
            url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms/' + vms_id + '/action/multi-clone'
        else:
            url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms/' + vms_id + '/action/clone'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.post(url, headers, json.dumps(data))
        return code, res

    @staticmethod
    def delete_fusion_compute_vms(huawei_env, vms_id, site_id='3CE206C5'):
        """
        删除虚拟机
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms/' + vms_id + '?isFormat=0&holdTime=0'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.delete(url, headers)
        return code, res

    @staticmethod
    def stop_fusion_compute_vms(huawei_env, vms_id, data, site_id='3CE206C5'):
        """
        停止虚拟机
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms/' + vms_id + '/action/stop'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.post(url, headers, json.dumps(data))
        return code, res

    @staticmethod
    def start_fusion_compute_vms(huawei_env, vms_id, site_id='3CE206C5'):
        """
        开启虚拟机
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms/' + vms_id + '/action/start'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.post(url, headers)
        return code, res

    @staticmethod
    def get_fusion_compute_os_versions(huawei_env, site_id='3CE206C5'):
        """
        查询虚拟机操作系统信息
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms/osversions'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

class HWDatastore(object):

    @staticmethod
    def get_fusion_compute_datastore(huawei_env, site_id='3CE206C5'):
        """
        查询数据存储信息
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/datastores'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

class HWDvSwitch(object):

    @staticmethod
    def get_fusion_compute_dv_switch(huawei_env, site_id='3CE206C5'):
        """
        查询分布式交换机
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/dvswitchs'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

    @staticmethod
    def get_fusion_compute_port_group(huawei_env, port_group_num, site_id='3CE206C5'):
        """
        查询交换机下端口组
        :param site_id:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/dvswitchs/' + port_group_num + '/portgroups'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

class HWVfdFile(object):

    @staticmethod
    def get_fusion_compute_vfd_file(huawei_env, site_id='3CE206C5'):
        """
        查询软驱
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms/action/queryVfdFiles'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

class HWVncKeyboard(object):

    @staticmethod
    def get_fusion_compute_vnc_keyboard(huawei_env, site_id='3CE206C5'):
        """
        查询键盘配置
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/vms/vncKeymapSettings'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

class HWNetwork(object):

    @staticmethod
    def get_fusion_compute_network(huawei_env, site_id='3CE206C5'):
        """
        查询虚拟机信息
        :param request:
        :return:
        """
        # hw_sites = HWSite.get_fusion_compute_sites()
        # site_uri_list = hw_sites['sites'][0]['uri'].split('/')
        # site_id = site_uri_list[-1]
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/dvswitchs'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res

class HWSecurityGroup(object):

    @staticmethod
    def get_fusion_compute_security_group(huawei_env, site_id='3CE206C5'):
        """
        查询安全组信息
        :param request:
        :return:
        """
        url = huawei_env.get('hw_address') + SITE_URI + '/' + site_id + '/securitygroups'
        headers = HuaweiyunConnectionMng().common_headers(huawei_env)
        code, res = HttpHelper.get(url, headers)
        return code, res