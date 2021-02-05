import json
import logging
from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from django.db.models import Count
from project_monitor.settings import SMTP_HOST, MAIL_USER, MAIL_PASS, MAIL_SENDER
from email.mime.text import MIMEText
from email.header import Header

from django.db.models import Sum
from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.decorators import action

from django.core.paginator import Paginator
from rest_framework.response import Response
from alarm.models import AlarmSeverity, AlarmStrategy, AlarmRule, AlarmDetail
from alarm.serializers import AlarmSeveritySerializer, AlarmStrategySerializer, AlarmRuleSerializer, \
    AlarmDetailSerializer


logger = logging.getLogger('log')


class AlarmSeverityViewSet(viewsets.ModelViewSet):
    queryset = AlarmSeverity.objects.all()
    serializer_class = AlarmSeveritySerializer

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
        grade_name = request.query_params.get('grade_name')
        is_delete = request.query_params.get('is_delete')
        if grade_name:
            search_dict['grade_name'] = grade_name
        if is_delete:
            search_dict['is_delete'] = is_delete
        # 查询数据
        alarm_list = AlarmSeverity.objects.get_queryset().filter(**search_dict).order_by('id')

        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(alarm_list, pre_page)
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
            return Response(self.get_serializer(alarm_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        alarm_severity = AlarmSeverity.objects.get(id=id)
        alarm_severity.is_delete = True
        alarm_severity.remove_time = datetime.now()
        alarm_severity.save()
        result = model_to_dict(alarm_severity)
        return Response(result, status=status.HTTP_200_OK)


class AlarmStrategyViewSet(viewsets.ModelViewSet):
    queryset = AlarmStrategy.objects.all()
    serializer_class = AlarmStrategySerializer

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
        strategy_name = request.query_params.get('strategy')
        is_delete = request.query_params.get('is_delete')
        if strategy_name:
            search_dict['strategy_name'] = strategy_name
        if is_delete:
            search_dict['is_delete'] = is_delete
        # 查询数据
        alarm_list = AlarmStrategy.objects.get_queryset().filter(**search_dict).order_by('id')

        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(alarm_list, pre_page)
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
            return Response(self.get_serializer(alarm_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        alarm_strategy = AlarmStrategy.objects.get(id=id)
        alarm_strategy.is_delete = True
        alarm_strategy.remove_time = datetime.now()
        alarm_strategy.save()
        result = model_to_dict(alarm_strategy)
        return Response(result, status=status.HTTP_200_OK)


class AlarmRuleViewSet(viewsets.ModelViewSet):
    queryset = AlarmRule.objects.all()
    serializer_class = AlarmRuleSerializer

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
        rule_name = request.query_params.get('rule_name')
        alarm_object = request.query_params.get('alarm_object')
        device_name = request.query_params.get('device_name')
        device_ip = request.query_params.get('device_ip')
        is_delete = request.query_params.get('is_delete')
        if rule_name:
            search_dict['rule_name'] = rule_name
        if device_name:
            search_dict['device_name'] = device_name
        if is_delete:
            search_dict['is_delete'] = is_delete
        # 查询数据
        if device_ip:
            rule_list = AlarmRule.objects.get_queryset().filter(tag__contains=device_ip, **search_dict).order_by('-create_time')
        else:
            rule_list = AlarmRule.objects.get_queryset().filter(**search_dict).order_by('-create_time')

        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(rule_list, pre_page)
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
            return Response(self.get_serializer(rule_list, many=True).data)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        alarm_rule = AlarmRule.objects.get(id=id)
        alarm_rule.is_delete = True
        alarm_rule.remove_time = datetime.now()
        alarm_rule.save()
        result = model_to_dict(alarm_rule)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def get_one_rule(self, request, pk):
        id = int(pk)
        alarm_rule = AlarmRule.objects.get(id=id)
        alarm_rule.rule_detail = json.loads(alarm_rule.rule_detail)
        result = model_to_dict(alarm_rule)
        return Response(result, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        alarm_rule_info = AlarmRule.objects.filter(rule_name=request.data.get('rule_name'), is_delete=0).all()
        if len(alarm_rule_info) == 0:
            if 'tag' in request.data.keys() and request.data.get('tag'):
                tag_info = request.data['tag']
                for tag in tag_info:
                    alarm_rule = AlarmRule()
                    alarm_rule.tag = tag['tag']
                    alarm_rule.device_name = tag['device_name']
                    if 'rule_name' in request.data.keys():
                        alarm_rule.rule_name = request.data['rule_name']
                    if 'alarm_object' in request.data.keys():
                        alarm_rule.alarm_object = request.data['alarm_object']
                    if 'server_type' in request.data.keys():
                        alarm_rule.server_type = request.data['server_type']
                    if 'rule_detail' in request.data.keys():
                        alarm_rule.rule_detail = json.dumps(request.data['rule_detail'])
                    alarm_rule.create_time = datetime.now()
                    alarm_rule.save()
                return Response(data="创建成功", status=status.HTTP_201_CREATED)
            return Response(data="无关联资源", status=status.HTTP_204_NO_CONTENT)
        else:
            result = {'msg': '资源名称已存在'}
            return Response(data=result, status=status.HTTP_205_RESET_CONTENT)

    def update(self, request, *args, **kwargs):
        alarm_rule = AlarmRule.objects.filter(rule_name=request.data.get('rule_name')).all()
        if len(alarm_rule) == 0:
            id = int(kwargs['pk'])
            alarm_rule = AlarmRule.objects.filter(id=id).first()
            alarm_rule.rule_name = request.data['rule_name']
            if 'rule_detail' in request.data.keys():
                alarm_rule.rule_detail = json.dumps(request.data['rule_detail'])
            alarm_rule.update_time = datetime.now()
            alarm_rule.save()
            result = model_to_dict(alarm_rule)
            return Response(data=result, status=status.HTTP_200_OK)
        else: # 数据库中存在同名的
            id = int(kwargs['pk'])
            the_alarm_rule = AlarmRule.objects.filter(id=id).first()
            for one_alarm_rule in alarm_rule:
                if one_alarm_rule.id == id:
                    request.data.pop('rule_name')
                    if 'rule_detail' in request.data.keys():
                        one_alarm_rule.rule_detail = json.dumps(request.data['rule_detail'])
                    one_alarm_rule.update_time = datetime.now()
                    one_alarm_rule.save()
                    one_alarm_rule = model_to_dict(one_alarm_rule)
                    return Response(data=one_alarm_rule, status=status.HTTP_200_OK)
                if the_alarm_rule.tag == one_alarm_rule.tag:
                    result = "名称重复"
                    return Response(data=result, status=status.HTTP_205_RESET_CONTENT)
            the_alarm_rule.rule_name = request.data.get('rule_name')
            the_alarm_rule.rule_detail = json.dumps(request.data['rule_detail'])
            the_alarm_rule.update_time = datetime.now()
            the_alarm_rule.save()
            the_alarm_rule = model_to_dict(the_alarm_rule)
            return Response(data=the_alarm_rule, status=status.HTTP_200_OK)


class AlarmDetailViewSet(viewsets.ModelViewSet):
    queryset = AlarmDetail.objects.all()
    serializer_class = AlarmDetailSerializer

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
        alarm_level = request.query_params.get('alarm_level')
        server_type = request.query_params.get('server_type')
        indicator_name = request.query_params.get('indicator_name')
        alarm_status = request.query_params.get('alarm_status')
        alarm_ip = request.query_params.get('alarm_ip')
        alarm_last_time1 = request.query_params.get('alarm_last_time1',None)
        alarm_last_time2 = request.query_params.get('alarm_last_time2',None)
        if alarm_level and len(alarm_level) == 1:
            search_dict['alarm_level'] = alarm_level
        if indicator_name:
            search_dict['indicator_name'] = indicator_name
        if alarm_status:
            search_dict['alarm_status'] = alarm_status
        if server_type:
            search_dict['server_type'] = server_type
        if alarm_ip:
            search_dict['alarm_ip'] = alarm_ip
        # 查询数据
        alarm_list = AlarmDetail.objects.get_queryset().filter(**search_dict).order_by('-alarm_last_time')
        if alarm_last_time1 and alarm_last_time2 and alarm_last_time1 != 'null' and alarm_last_time2 != 'null':
            alarm_list = AlarmDetail.objects.filter(alarm_last_time__gt=alarm_last_time1, alarm_last_time__lt=
                alarm_last_time2, **search_dict ).order_by('-alarm_last_time')
            if len(alarm_level) >= 1:
                alarm_level = alarm_level.split(',')
                alarm_list = AlarmDetail.objects.filter(alarm_level__in=alarm_level,
                                                        alarm_last_time__gt=alarm_last_time1,
                                                        alarm_last_time__lt=alarm_last_time2, **search_dict).order_by(
                    '-alarm_last_time')
        elif alarm_last_time1 and alarm_last_time1 != 'null' and (alarm_last_time2=='null' or not alarm_last_time2):
            alarm_list = AlarmDetail.objects.filter(alarm_last_time__gt=alarm_last_time1,  **search_dict ).order_by(
                '-alarm_last_time')
            if len(alarm_level) >= 1:
                alarm_level = alarm_level.split(',')
                alarm_list = AlarmDetail.objects.filter(alarm_level__in=alarm_level,
                                                        alarm_last_time__gt=alarm_last_time1, **search_dict).order_by(
                    '-alarm_last_time')
        elif alarm_last_time2 and alarm_last_time2 != 'null' and (alarm_last_time1=='null' or not alarm_last_time1):
            alarm_list = AlarmDetail.objects.filter(alarm_last_time__lt=alarm_last_time2, **search_dict ).order_by(
                '-alarm_last_time')
            if len(alarm_level) >= 1:
                alarm_level = alarm_level.split(',')
                alarm_list = AlarmDetail.objects.filter(alarm_level__in=alarm_level,
                                                        alarm_last_time__lt=alarm_last_time2, **search_dict).order_by(
                    '-alarm_last_time')
        elif (alarm_last_time1 == 'null' or not alarm_last_time1) and (alarm_last_time2 == 'null' or not alarm_last_time2):
            if len(alarm_level) >= 1:
                alarm_level = alarm_level.split(',')
                alarm_list = AlarmDetail.objects.filter(alarm_level__in=alarm_level, **search_dict).order_by(
                    '-alarm_last_time')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(alarm_list, pre_page)
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
            return Response(self.get_serializer(alarm_list, many=True).data)

    @action(detail=False, methods=['GET'], url_path='alarm_count')
    def get_alarm_count(self, requests, *args, **kwargs):
        result = {"total_count": [], "remain_count": [], "level_count": [],
                  "object_count": [], "tag_count": [], "business_count": []}
        total_count = AlarmDetail.objects.aggregate(total=Sum('alarm_count'))
        remain_count = AlarmDetail.objects.filter(alarm_status__in=['告警中', '告警升级', '处理中']).aggregate(total=Sum('alarm_count'))
        level_counts = AlarmDetail.objects.filter(alarm_status__in=['告警中', '告警升级', '处理中']).values('alarm_level').annotate(total=Sum('alarm_count')).values('alarm_level', 'total')
        if not remain_count['total']:
            remain_count['total'] = 0
        if not total_count['total']:
            total_count['total'] = 0
        result['level_count'] = [{"name":5, "value":0}, {"name":4, "value":0}, {"name":3, "value":0},
                                 {"name":2, "value":0}, {"name":1, "value":0}]
        for level_count in level_counts:
            for one in result['level_count']:
                if one['name'] == level_count['alarm_level']:
                    one['value'] = level_count['total']
            # result['level_count'].append({"name": level_count['alarm_level'], "value":level_count['total']})
        result['total_count'].append({"name":"告警总数","value": total_count['total']})
        result['remain_count'].append({"name":"未处理总数", "value": remain_count['total']})
        result['object_count'] = AlarmDetailViewSet.get_server_type_alarm_count()
        result['tag_count'] = AlarmDetailViewSet.get_tag_alarm_count()
        result['business_count'] = AlarmDetailViewSet.get_business_alarm_count()
        result['remain_alarm_detail'] = AlarmDetailViewSet.get_remain_alarm_detail()
        logging.info(result)
        return Response(data=result,status=status.HTTP_200_OK)

    # @staticmethod
    # def get_level_alarm_count():
    #     alarm_level_list = [1,2,3,4,5]
    #     result = []
    #     for alarm_level in alarm_level_list:
    #         level_counts = AlarmDetail.objects.filter(alarm_level=alarm_level).annotate(total=Sum('alarm_count'))
    #         levelcount = 0
    #         for level_count in level_counts:
    #             if level_count.alarm_count:
    #                 levelcount += level_count.alarm_count
    #         result.append({"name": alarm_level, "value": levelcount})
    #     return result

    @staticmethod
    def get_server_type_alarm_count():
        server_types = ['SERVER', 'MYSQL', 'ORACLE', 'DM', 'REDIS', 'WEBSPHERE', 'ROUTER', 'SWITCH', 'FIREWALL', 'LOADBALANCE', 'STORAGE']
        result = []
        for server_type in server_types:
            object_counts = AlarmDetail.objects.filter(server_type=server_type).annotate(total=Sum('alarm_count'))
            objectcount = 0
            for object_count in object_counts:
                if object_count.alarm_count:
                    objectcount += object_count.alarm_count
            result.append({"name": server_type, "value": objectcount})
        return result

    @staticmethod
    def get_tag_alarm_count():
        from asset_relation.models import Tag
        result = []
        tag_list = Tag.objects.all()
        for tag in tag_list:
            tag_id = tag.id
            from asset_relation.models import DeviceLabel, VirtualServerLabel, DeviceModelLabel, StorageLabel
            device_list = []
            devices = DeviceLabel.objects.filter(label_id=tag_id).all()
            for device in devices:
                device_list.append(device.device_id)
            from asset_relation.models import Device, VirtualServer, DeviceModel, Storage
            device_info = Device.objects.filter(id__in=device_list).all()
            # 每个标签下服务器的告警数量统计
            server_tagcount = 0
            for device in device_info:
                tag_counts = AlarmDetail.objects.filter(alarm_ip=device.device_ip).annotate(total=Sum('alarm_count'))
                for tag_count in tag_counts:
                    if tag_count.alarm_count:
                        server_tagcount += tag_count.alarm_count
            virtual_server_list = []
            virtual_server_info = VirtualServerLabel.objects.filter(label_id=tag_id).all()
            for virtual_server in virtual_server_info:
                virtual_server_list.append(virtual_server.virtual_server_id)
            virtual_servers = VirtualServer.objects.filter(id__in=virtual_server_list).all()
            # 每个标签下虚拟服务器的告警数量统计
            virtual_tagcount = 0
            for virtual_server in virtual_servers:
                tag_counts = AlarmDetail.objects.filter(alarm_ip=virtual_server.virtual_ip).annotate(total=Sum('alarm_count'))
                for tag_count in tag_counts:
                    if tag_count.alarm_count:
                        virtual_tagcount += tag_count.alarm_count

            network_list = []
            network_info = DeviceModelLabel.objects.filter(label_id=tag_id).all()
            for network in network_info:
                network_list.append(network.network_id)
            networks = DeviceModel.objects.filter(id__in=network_list).all()
            # 每个业务下网络设备的告警数量统计
            network_tagcount = 0
            for network in networks:
                tag_counts = AlarmDetail.objects.filter(alarm_ip=network.ipaddr).annotate(
                    total=Sum('alarm_count'))
                for tag_count in tag_counts:
                    if tag_count.alarm_count:
                        network_tagcount += tag_count.alarm_count
            storage_list = []
            storage_info = StorageLabel.objects.filter(label_id=tag_id).all()
            for storage in storage_info:
                storage_list.append(storage.storage_id)
            storages = Storage.objects.filter(id__in=storage_list).all()
            # 每个业务下存储设备的告警数量统计
            storage_tagcount = 0
            for storage in storages:
                tag_counts = AlarmDetail.objects.filter(alarm_ip=storage.manage_ip).annotate(
                    total=Sum('alarm_count'))
                for tag_count in tag_counts:
                    if tag_count.alarm_count:
                        storage_tagcount += tag_count.alarm_count
            result.append({"name": tag.tag_name, "value": server_tagcount + virtual_tagcount + network_tagcount +
                                                          storage_tagcount})
        return result

    @staticmethod
    def get_business_alarm_count():
        from asset_relation.models import Business
        result = []
        business_list = Business.objects.all()
        for business in business_list:
            business_id = business.id
            from asset_relation.models import DeviceBusiness, VirtualServerBusiness, DeviceModelBusiness, StorageBusiness
            device_list = []
            devices = DeviceBusiness.objects.filter(business_id=business_id).all()
            for device in devices:
                device_list.append(device.device_id)
            from asset_relation.models import Device, VirtualServer, DeviceModel, Storage
            device_info = Device.objects.filter(id__in=device_list).all()
            server_businesscount = 0
            # 每个业务下服务器告警数量统计
            for device in device_info:
                business_counts = AlarmDetail.objects.filter(alarm_ip=device.device_ip).annotate(
                    total=Sum('alarm_count'))
                for business_count in business_counts:
                    if business_count.alarm_count:
                        server_businesscount += business_count.alarm_count
            virtual_server_list = []
            virtual_server_info = VirtualServerBusiness.objects.filter(business_id=business_id).all()
            for virtual_server in virtual_server_info:
                virtual_server_list.append(virtual_server.virtual_server_id)
            virtual_servers = VirtualServer.objects.filter(id__in=virtual_server_list).all()
            # 每个业务下虚拟服务器的告警数量统计
            virtual_businesscount = 0
            for virtual_server in virtual_servers:
                business_counts = AlarmDetail.objects.filter(alarm_ip=virtual_server.virtual_ip).annotate(
                    total=Sum('alarm_count'))
                for business_count in business_counts:
                    if business_count.alarm_count:
                        virtual_businesscount += business_count.alarm_count
            network_list = []
            network_info = DeviceModelBusiness.objects.filter(business_id=business_id).all()
            for network in network_info:
                network_list.append(network.network_id)
            networks = DeviceModel.objects.filter(id__in=network_list).all()
            # 每个业务下网络设备的告警数量统计
            network_businesscount = 0
            for network in networks:
                business_counts = AlarmDetail.objects.filter(alarm_ip=network.ipaddr).annotate(
                    total=Sum('alarm_count'))
                for business_count in business_counts:
                    if business_count.alarm_count:
                        network_businesscount += business_count.alarm_count
            storage_list = []
            storage_info = StorageBusiness.objects.filter(business_id=business_id).all()
            for storage in storage_info:
                storage_list.append(storage.storage_id)
            storages = Storage.objects.filter(id__in=storage_list).all()
            # 每个业务下存储设备的告警数量统计
            storage_businesscount = 0
            for storage in storages:
                business_counts = AlarmDetail.objects.filter(alarm_ip=storage.manage_ip).annotate(
                    total=Sum('alarm_count'))
                for business_count in business_counts:
                    if business_count.alarm_count:
                        storage_businesscount += business_count.alarm_count

            result.append({"name": business.name, "value": server_businesscount + virtual_businesscount +
                                                           network_businesscount + storage_businesscount})
        return result

    @staticmethod
    def get_remain_alarm_detail():
        """
        获取未处理告警的详细信息
        :return:
        """
        dict_ = {'SERVER':'服务器', 'MYSQL':'MySQL', 'ORACLE':'Oracle', 'DM':'达梦', 'REDIS':'Redis',
                 'WEBSPHERE':'WebSphere', 'ROUTER':'路由器', 'SWITCH':'交换机', 'FIREWALL':'防火墙',
                 'LOADBALANCE':'负载均衡', 'STORAGE':'存储'}
        level_ = {'1': '提示', '2': '报警', '3': '重要', '4': '严重', '5': '紧急'}
        alarm_detail = AlarmDetail.objects.filter(alarm_status__in=['告警中','告警升级']).order_by('-alarm_last_time').all()
        alarm_list = alarm_detail.values()
        for alarm in alarm_list:
            if alarm['server_type'] and dict_.get(alarm['server_type']):
                alarm['server_type'] = dict_.get(alarm['server_type'])
            else:
                alarm['server_type'] = 'UNKNOWN'
            alarm['alarm_level'] = level_[str(alarm['alarm_level'])]
        return alarm_list


    @action(detail=False, methods=['GET'])
    def alarm(self, request):
        query = request.query_params.get('query', None)
        if query:
            alarm_info = list(AlarmDetail.objects.get_queryset().filter(alarm_ip__contains=query).order_by('-alarm_last_time'))
            alarm_temp = list()
            for alarm in alarm_info[:]:
                if alarm.alarm_ip not in alarm_temp:
                    alarm_temp.append(alarm.alarm_ip)
                else:
                    alarm_info.remove(alarm)
            return Response(
                self.get_serializer(alarm_info, many=True).data)
        return Response(self.get_serializer(None, many=True).data)

    @action(detail=False, methods=['PUT'], url_path='status')
    def del_alarm(self, request, *args, **kwargs):
        alarm_status = request.data.get('alarm_status')
        id = request.data.get('id')
        alarm_detail = AlarmDetail.objects.filter(id=id).first()
        if alarm_status:
            alarm_detail.alarm_status = alarm_status
            if alarm_status == '处理中':
                alarm_detail.alarm_time = datetime.now()
            elif alarm_status == '告警升级':
                alarm_detail.upgrade_time = datetime.now()
            elif alarm_status == '已处理':
                alarm_detail.finish_time = datetime.now()
            alarm_detail.save()
        result = model_to_dict(alarm_detail)
        if alarm_status == '告警升级':
            from sys_relation.views import UserViewSet
            email_list = UserViewSet().get_user_email()
            AlarmDetailViewSet().send_email(email_list, result['alarm_ip'])
        return Response(data=result, status=status.HTTP_200_OK)

    def send_email(self, email_list, ip):

        # 第三方 SMTP 服务
        smtp_host = SMTP_HOST
        mail_user = MAIL_USER
        mail_pass = MAIL_PASS
        sender = MAIL_SENDER  # 发送邮件

        receivers = ','.join(email_list)  # 接收邮件
        msg = MIMEText('Alarm 告警信息通知邮件...\n 您好,告警源为%s,请及时处理' %(ip), 'plain', 'utf-8')
        message = MIMEMultipart()
        message.attach(msg)
        message['From'] = sender
        message['To'] = receivers
        subject = 'Alarm 告警信息通知'
        message['Subject'] = Header(subject, 'utf-8')

        smtpObj = False
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(smtp_host, 25) #  25为默认端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, email_list, message.as_string())
            logging.info("邮件发送成功")
        except Exception as e:
            logging.error('邮件发送失败,原因: %s' %e)
        finally:
            smtpObj and smtpObj.quit()




