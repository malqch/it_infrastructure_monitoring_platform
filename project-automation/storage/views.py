from rest_framework import viewsets, status
from sys_auth.views import MyAuthentication
from rest_framework.decorators import action
from django.core.cache import cache
import requests
import json
from rest_framework.response import Response
import logging
import re

logger = logging.getLogger('log')


class StorageViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]

    @staticmethod
    def verify_user(storage_env):
        manage_address = storage_env.get('manage_address', None)
        username = storage_env.get('manage_username', None)
        password = storage_env.get('manage_password', None)
        try:
            url = manage_address + '/deviceManager/rest/xxxxx/sessions'
            params = json.dumps({"username": username, "password": password, "scope": 0})
            headers = {"Content-Type": "application/json"}
            res = requests.post(url, params, headers=headers, verify=False)
            res_status = res.status_code
            res_json = res.json()
            res_headers = res.headers
            # 将认证信息存cache
            authInfo = {'session': res_headers.get('Set-Cookie', None),
                         'iBaseToken': res_json['data'].get('iBaseToken', None),
                         'deviceid': res_json['data'].get('deviceid', None)}
            cache.set(manage_address + username + 'AuthInfo', json.dumps(authInfo), 60)
            cache.expire(manage_address + username + 'AuthInfo', 900)
            return res_status, res_json, res_headers
        except Exception as e:
            logger.error(e)
            return None, {'data': {}}, {}

    def get_common_header(self, storage_env):
        try:
            auth_info = cache.get(storage_env.get('manage_address') + storage_env.get('manage_username') + 'AuthInfo')
        except Exception as e:
            auth_info = None
            logger.info("获取认证失败:{error}, 正在重新登录".format(error=e))
        if auth_info:
            auth_info = json.loads(auth_info)
            set_cookie = auth_info.get('session')
            iBaseToken = auth_info.get('iBaseToken')
            device_id = auth_info.get('deviceid')
        else:
            res_status, res_json, res_headers = self.verify_user(storage_env)
            set_cookie = res_headers.get('Set-Cookie', None)
            iBaseToken = res_json['data'].get('iBaseToken', None)
            device_id = res_json['data'].get('deviceid', None)
        session = ''
        if set_cookie:
            session = re.search('ismsession.*?;', set_cookie).group()
            session = session.replace(';', '')
        dict_ = {}
        dict_['deviceid'] = device_id
        dict_['headers'] = {"Content-Type": "application/json", "session": session,
                            "iBaseToken": iBaseToken}
        logger.info(dict_)
        return dict_

    @action(detail=False, methods=['POST'])
    def nextavailableid(self, request):
        """
        创建lun、lun组、host、host组、视图映射时查询可用的name
        """
        type_ = request.query_params.get('type', None)
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            url = storage_env.get('manage_address',
                                  None) + '/deviceManager/rest/' + header_dict[
                      'deviceid'] + '/nextavailableid/?TYPE=' + type_
            res_availableid = requests.get(url, headers=header_dict['headers'],
                                           verify=False)
            res_availableid_json = res_availableid.json()
            if res_availableid_json.get('error')['code'] == 0:
                return Response(res_availableid_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response(
                    {'msg': res_availableid_json.get('error')['description']},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def storagepool_list(self, request):
        """
        新增LUN时查询存储池信息
        """
        logger.info(request.data)
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            url = storage_env.get('manage_address', None) + '/deviceManager/rest/' + header_dict['deviceid'] + '/storagepool'
            res_storagepool = requests.get(url, headers=header_dict['headers'], verify=False)
            res_storagepool_json = res_storagepool.json()
            if res_storagepool_json['error']['code'] == 0:
                return Response(res_storagepool_json.get('data'), status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_storagepool_json.get('error')['description']},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def lun_list(self, request):
        """
        查询存储下lun的信息
        """
        logger.info(request.data)
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            SADD2LUNGROUP = request.query_params.get('ISADD2LUNGROUP', None)
            manage_address = request.data.get('manage_address', None)
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            if SADD2LUNGROUP:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/lun?ISADD2LUNGROUP={SADD2LUNGROUP}'
            else:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/lun'
            res_lun = requests.get(url, headers=headers, verify=False)
            res_lun_json = res_lun.json()
            logger.info(res_lun_json)
            if res_lun_json.get('error')['code'] == 0:
                return Response(res_lun_json, status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_lun_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def create_lun(self, request):
        """创建LUN"""
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        manage_address = request.data.get('manage_address', None)
        try:
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            url = f'{manage_address}/deviceManager/rest/{deviceid}/lun'
            # param = {"NAME": request.data.get('NAME', None), "DESCRIPTION": request.data.get('DESCRIPTION'),
            #          "PARENTID": request.data.get('PARENTID'), "PARENTTYPE": request.data.get('PARENTTYPE'),
            #          "USAGETYPE": request.data.get('USAGETYPE'), "SUBTYPE": request.data.get('SUBTYPE')}
            # res_lun = requests.post(url, json.dumps(param), headers=headers, verify=False)
            res_lun = requests.post(url, json.dumps(request.data), headers=headers, verify=False)
            res_lun_json = res_lun.json()
            logger.info(res_lun_json)
            if res_lun_json['error']['code'] == 0:
                return Response(res_lun_json, status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_lun_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def lun_group_list(self, request):
        """查询LUN组列表"""
        logger.info(request.data)
        ISADD2MAPPINGVIEW = request.query_params.get('ISADD2MAPPINGVIEW', None)
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            deviceid = header_dict.get('deviceid', None)
            manage_address = request.data.get('manage_address', None)
            headers = header_dict.get('headers', None)
            if ISADD2MAPPINGVIEW:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/lungroup?ISADD2MAPPINGVIEW={ISADD2MAPPINGVIEW}'
            else:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/lungroup'
            lun_group = requests.get(url, headers=headers, verify=False)
            lun_group_json = lun_group.json()
            logger.info(lun_group_json)
            if lun_group_json['error']['code'] == 0:
                return Response(lun_group_json, status=status.HTTP_200_OK)
            else:
                return Response({'msg': lun_group_json.get('error')['description']},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def create_lun_group(self, request):
        """创建LUN组"""
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        manage_address = request.data.get('manage_address', None)
        lun_group = request.data.get('lun_group', {})
        try:
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            url = manage_address + '/deviceManager/rest/' + deviceid + '/lungroup'
            res = requests.post(url, json.dumps(lun_group), headers=headers, verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def lun_group_associate(self, request):
        """LUN组添加关联的LUN"""
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        manage_address = request.data.get('manage_address', None)
        lun_associate = request.data.get('lun_associate', {})
        try:
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            url = manage_address + '/deviceManager/rest/' + deviceid + '/lungroup/associate'
            res = requests.post(url, json.dumps(lun_associate), headers=headers,
                                verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='host_list')
    def host_list(self, request):
        """获得主机列表"""
        logger.info(request.data)
        storage_env = request.data
        ISADD2HOSTGROUP = request.query_params.get('ISADD2HOSTGROUP', None)
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            manage_address = storage_env.get('manage_address', None)
            if ISADD2HOSTGROUP:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/host?filter=ISADD2HOSTGROUP::{ISADD2HOSTGROUP}'
            else:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/host'
            res = requests.get(url, headers=headers, verify=False)
            res_json = res.json()
            if res_json.get('error')['code'] == 0:
                return Response(res_json.get('data'), status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def host_group_list(self, request):
        """获得主机组列表"""
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        manage_address = request.data.get('manage_address', None)
        try:
            deviceid = header_dict.get('deviceid', None)
            url = f'{manage_address}/deviceManager/rest/{deviceid}/hostgroup'
            headers = header_dict.get('headers', None)
            lun_group = requests.get(url, headers=headers, verify=False)
            lun_group_json = lun_group.json()
            logger.info(lun_group_json)
            if lun_group_json['error']['code'] == 0:
                return Response(lun_group_json, status=status.HTTP_200_OK)
            else:
                return Response({'msg': lun_group_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='create_host')
    def create_host(self, request):
        """
        创建主机
        """
        logger.info(request.data)
        storage_env = request.data.get('storage_env')
        data = request.data.get('data')
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            url = storage_env.get('manage_address',
                                  None) + '/deviceManager/rest/' + header_dict[
                      'deviceid'] + '/host'
            res = requests.post(url, data=json.dumps(data),
                                headers=header_dict['headers'], verify=False)
            res_json = res.json()
            if res_json.get('data'):
                return Response(data=res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': e}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='create_host_group')
    def create_host_group(self, request):
        """创建主机组"""
        storage_env = request.data.get('storage_env')
        data = request.data.get('data')
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            deviceid = header_dict.get('deviceid', None)
            url = storage_env.get('manage_address',
                                  None) + '/deviceManager/rest/' + deviceid + '/hostgroup'
            headers = header_dict.get('headers', None)
            res = requests.post(url, json=data, headers=headers, verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(res_json, status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='host_group_associate')
    def host_group_associate(self, request):
        """主机组添加关联主机"""
        logger.info(request.data)
        storage_env = request.data.get('storage_env')
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        host_associate = request.data.get('data', None)
        try:
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            url = storage_env.get('manage_address',
                                  None) + '/deviceManager/rest/' + deviceid + '/hostgroup/associate'
            res = requests.post(url, json=host_associate, headers=headers,
                                verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def portlist(self, request):
        """查询四种类型的端口列表"""
        logger.info(request.data)
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        dict_ = {}
        try:
            manage_address = request.data.get('manage_address', None)
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            fc_port_url = f'{manage_address}/deviceManager/rest/{deviceid}/FC_PORT'
            fc_port_res = requests.get(fc_port_url, headers=headers, verify=False)
            fc_port_json = fc_port_res.json()
            dict_['FC_PORT'] = fc_port_json.get('data', [])
            eth_port_url = f'{manage_address}/deviceManager/rest/{deviceid}/ETH_PORT?LOGICTYPE=0'
            eth_port_res = requests.get(eth_port_url, headers=headers, verify=False)
            eth_port_json = eth_port_res.json()
            dict_['ETH_PORT'] = eth_port_json.get('data', [])
            fcoe_port_url = f'{manage_address}/deviceManager/rest/{deviceid}/FCoE_PORT'
            fcoe_port_res = requests.get(fcoe_port_url, headers=headers, verify=False)
            fcoe_port_json = fcoe_port_res.json()
            dict_['FCoE_PORT'] = fcoe_port_json.get('data', [])
            ib_port_url = f'{manage_address}/deviceManager/rest/{deviceid}/IB_PORT'
            ib_port_res = requests.get(ib_port_url, headers=headers,
                                       verify=False)
            ib_port_json = ib_port_res.json()
            dict_['IB_PORT'] = ib_port_json.get('data', [])
            return Response(dict_, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def create_port_group(self, request):
        """创建端口组"""
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        manage_address = request.data.get('manage_address', None)
        port_group = request.data.get('port_group', {})
        try:
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            url = manage_address + '/deviceManager/rest/' + deviceid + '/portgroup'
            res = requests.post(url, json.dumps(port_group), headers=headers,
                                verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def port_group_associate(self, request):
        """端口组添加关联端口"""
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        manage_address = request.data.get('manage_address', None)
        port_associate = request.data.get('port_associate', {})
        try:
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            url = f'{manage_address}/deviceManager/rest/{deviceid}/port/associate/portgroup'
            res = requests.post(url, json.dumps(port_associate),
                                headers=headers,
                                verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def port_group_list(self, request):
        """获得端口组列表"""
        logger.info(request.data)
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            manage_address = request.data.get('manage_address')
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            url = f'{manage_address}/deviceManager/rest/{deviceid}/portgroup'
            lun_group = requests.get(url, headers=headers, verify=False)
            lun_group_json = lun_group.json()
            logger.info(lun_group_json)
            if lun_group_json.get('error')['code'] == 0:
                return Response(lun_group_json, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'msg': lun_group_json.get('error')['description']},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def create_mapping_view(self, request):
        """创建映射视图"""
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        manage_address = request.data.get('manage_address', None)
        mapping_view = request.data.get('mapping_view', {})
        try:
            headers = header_dict.get('headers', None)
            deviceid = header_dict.get('deviceid', None)
            url = manage_address + '/deviceManager/rest/' + deviceid + '/mappingview'
            res = requests.post(url, json.dumps(mapping_view), headers=headers,
                                verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def mapping_view_associate(self, request):
        """视图映射添加LUN组、端口组、主机组"""
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        manage_address = request.data.get('manage_address', None)
        mapping_associate = request.data.get('mapping_associate', {})
        HOSTLUNID = request.data.get('HOSTLUNID', 0)
        try:
            if HOSTLUNID and mapping_associate.get('mapping_associate') and \
                    mapping_associate.get('mapping_associate').get('ASSOCIATEOBJTYPE', None) == 14:
                mapping_associate['HOSTLUNID'] = HOSTLUNID
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            url = manage_address + '/deviceManager/rest/' + deviceid + '/MAPPINGVIEW/CREATE_ASSOCIATE'
            res = requests.put(url, json.dumps(mapping_associate),
                               headers=headers, verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def mappingviewlist(self, request):
        """查询视图映射的列表"""
        logger.info(request.data)
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            manage_address = storage_env.get('manage_address', None)
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            url = f'{manage_address}/deviceManager/rest/{deviceid}/mappingview'
            res = requests.get(url, headers=headers, verify=False)
            res_json = res.json()
            logger.info(res_json)
            if res_json.get('error')['code'] == 0:
                return Response(res_json.get('data'), status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def associate_mappingview(self, request):
        """查询视图映射对应的LUN组、端口组、主机组"""
        logger.info(request.data)
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            manage_address = request.data.get('manage_address')
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            type_ = request.query_params.get('TYPE', None)
            associateobjtype = request.query_params.get('ASSOCIATEOBJTYPE', None)
            associateobbjid = request.query_params.get('ASSOCIATEOBJID', None)
            url = ''
            if int(type_) == 256:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/lungroup/associate/mappingview?' \
                  f'TYPE={type_}&ASSOCIATEOBJTYPE={associateobjtype}&ASSOCIATEOBJID={associateobbjid}'
            if int(type_) == 14:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/hostgroup/associate/mappingview?' \
                      f'TYPE={type_}&ASSOCIATEOBJTYPE={associateobjtype}&ASSOCIATEOBJID={associateobbjid}'
            if int(type_) == 257:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/portgroup/associate/mappingview?' \
                      f'TYPE={type_}&ASSOCIATEOBJTYPE={associateobjtype}&ASSOCIATEOBJID={associateobbjid}'
            res = requests.get(url, headers=headers, verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(data=res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': e}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def associate_group(self, request):
        """查询组对应的数据"""
        logger.info(request.data)
        storage_env = request.data
        if not storage_env:
            res = {'msg': '未发现存储环境！'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        header_dict = self.get_common_header(storage_env)
        try:
            manage_address = request.data.get('manage_address')
            deviceid = header_dict.get('deviceid', None)
            headers = header_dict.get('headers', None)
            type_ = request.query_params.get('TYPE', None)
            associateobjtype = request.query_params.get('ASSOCIATEOBJTYPE',
                                                        None)
            associateobbjid = request.query_params.get('ASSOCIATEOBJID', None)
            url = ''
            if int(type_) == 11:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/lun/associate?' \
                      f'TYPE={type_}&ASSOCIATEOBJTYPE={associateobjtype}&ASSOCIATEOBJID={associateobbjid}'
            if int(type_) == 21:
                url = f'{manage_address}/deviceManager/rest/{deviceid}/host/associate?' \
                      f'TYPE={type_}&ASSOCIATEOBJTYPE={associateobjtype}&ASSOCIATEOBJID={associateobbjid}'
            if not int(type_):
                fc_url = f'{manage_address}/deviceManager/rest/{deviceid}/fc_port/associate?TYPE=212&ASSOCIATEOBJTYPE={associateobjtype}&ASSOCIATEOBJID={associateobbjid}'
                eth_url = f'{manage_address}/deviceManager/rest/{deviceid}/eth_port/associate?TYPE=213&ASSOCIATEOBJTYPE={associateobjtype}&ASSOCIATEOBJID={associateobbjid}'
                fcoe_url = f'{manage_address}/deviceManager/rest/{deviceid}/fcoe_port/associate?TYPE=252&ASSOCIATEOBJTYPE={associateobjtype}&ASSOCIATEOBJID={associateobbjid}'
                ib_url = f"{manage_address}/deviceManager/rest/{deviceid}/ib_port/associate/portgroup?TYPE=16500&ASSOCIATEOBJTYPE={associateobjtype}&ASSOCIATEOBJID={associateobbjid}"
                res_fc = requests.get(fc_url, headers=headers, verify=False)
                fc_port = res_fc.json().get('data', [])
                res_eth = requests.get(eth_url, headers=headers, verify=False)
                eth_port = res_eth.json().get('data', [])
                res_fcoe = requests.get(fcoe_url, headers=headers, verify=False)
                fcoe_port = res_fcoe.json().get('data', [])
                res_ib = requests.get(ib_url, headers=headers, verify=False)
                ib_port = res_ib.json().get('data', [])
                fc_port.extend(eth_port)
                fc_port.extend(fcoe_port)
                fc_port.extend(ib_port)
                return Response(data=fc_port, status=status.HTTP_200_OK)
            res = requests.get(url, headers=headers, verify=False)
            res_json = res.json()
            if res_json['error']['code'] == 0:
                return Response(data=res_json.get('data'),
                                status=status.HTTP_200_OK)
            else:
                return Response({'msg': res_json.get('error')['description']},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e)
            return Response({'msg': "登录存储失败"}, status=status.HTTP_400_BAD_REQUEST)



