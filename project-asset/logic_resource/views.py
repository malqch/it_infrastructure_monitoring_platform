import logging
from django.http import FileResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from logic_resource.models import Staff, Business, Contract, Vendor
from logic_resource.serializers import StaffSerializer, BusinessSerializer, ContractSerializer, VendorSerializer
import datetime
from django.core.paginator import Paginator
import os

logger = logging.getLogger('log')
basedir = os.path.abspath(os.path.dirname(__file__))


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

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
        username = request.query_params.get('username', None)
        if username:
            search_dict['username__contains'] = username
        phone = request.query_params.get('phone', None)
        if phone:
            search_dict['phone__contains'] = phone
        email = request.query_params.get('email', None)
        if email:
            search_dict['email__contains'] = email
        logger.info(search_dict)
        staff_info = Staff.objects.get_queryset().filter(**search_dict).order_by('-update_time')
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(staff_info, pre_page)
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
            return Response(self.get_serializer(staff_info, many=True).data)

    def destroy(self, request, *args, **kwargs):
        """
        逻辑删除负责人信息，删除时需要把绑定到该负责人的业务的staff字段清空
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        staff = self.get_object()
        staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(detail=False, methods=['GET'])
    # def staff(self, request):
    #     staff_list = Business.objects.values_list('staff_id', flat=True)
    #     staff_list = list(filter(None, staff_list))
    #     staff_info = Staff.objects.exclude(id__in=staff_list).filter().all()
    #     return Response(self.get_serializer(staff_info, many=True).data)


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

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
        name = request.query_params.get('name', None)
        if name:
            search_dict['name'] = name
        search_dict['is_delete'] = 0
        business = Business.objects.get_queryset().filter(**search_dict).order_by('-update_time')
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(business, pre_page)
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
            return Response(self.get_serializer(business, many=True).data)

    @action(detail=True)
    def staff(self, request, pk):
        """
        查询指定业务下的负责人信息
        :param request:
        :param pk: 指定的业务信息
        :return: HTTP Response
        """
        role = self.get_object()
        serializer = BusinessSerializer(role)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(request.data)
        name = request.data.get('name', None)
        business_info = Business.objects.filter(name=name, is_delete=0).first()
        if business_info:
            return Response({'msg': "业务名已存在"}, status=status.HTTP_409_CONFLICT)
        staff_id = request.data.get("staff", None)
        if staff_id:
            staff_info = Staff.objects.get(id=staff_id)
            request.data['staff'] = staff_info
        business = Business(**request.data)
        business.save()
        return Response({"msg": "保存成功"}, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        logger.info(request.data)
        name = request.data.get('name', None)
        business_id = request.data.get('id')
        business = Business.objects.filter(name=name, is_delete=0).first()
        if business and business.id != business_id:
            return Response({'msg': "业务名已存在"}, status=status.HTTP_409_CONFLICT)
        business = self.get_object()
        staff_id = request.data.get("staff", None)
        business.staff_id = staff_id
        business.name = request.data.get("name")
        business.remark = request.data.get("remark")
        business.save()
        return Response({"msg": "修改成功"}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        business = self.get_object()
        device_info = business.device_set.all()
        if len(device_info):
            result = {'msg': '该业务下有关联服务器'}
            return Response(result)
        virtual_info = business.virtualserver_set.all()
        if len(virtual_info):
            result = {'msg': '该业务下有关联虚拟服务器'}
            return Response(result)
        network_info = business.devicemodel_set.all()
        if len(network_info):
            result = {'msg': '该业务下有关联网络设备'}
            return Response(result)
        storage = business.storage_set.all()
        if len(storage):
            result = {'msg': '该业务下有关联存储设备'}
            return Response(result)
        business.is_delete = 1
        business.remove_time = datetime.datetime.now()
        business.staff = None
        business.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST'])
    def devicebusiness(self, request):
        belong_business = request.data.get("business")
        business = Business.objects.get_queryset().filter(id__in=belong_business)
        return Response(self.get_serializer(business, many=True).data)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

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
        contract_name = request.query_params.get('contract_name', None)
        if contract_name:
            search_dict['contract_name__contains'] = contract_name
        search_dict['is_delete'] = 0
        contract_info = Contract.objects.get_queryset().filter(**search_dict).order_by('-update_time')
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(contract_info, pre_page)
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
            return Response(self.get_serializer(contract_info, many=True).data)

    def create(self, request, *args, **kwargs):
        logger.info(request.data)
        file_obj = request.data.get('file', None)
        contract_name = request.data.get("contract_name", None)
        contract_info = Contract.objects.filter(contract_name=contract_name).first()
        if contract_info:
            return Response({'msg': "文件名重复，请检查是否为同一文件"}, status=status.HTTP_202_ACCEPTED)
        filepath = basedir + '/contract'
        filedir = os.path.join(filepath, contract_name)
        with open(filedir, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        return super().create(request, *args, **kwargs)

    def update(self, request, pk, *args, **kwargs):
        logger.info(request.data)
        contact_id = int(pk)
        file_obj = request.data.get('file', None)
        contract_name = request.data.get("contract_name", None)
        contract_info = Contract.objects.filter(
            contract_name=contract_name).first()
        if contract_info and contract_info.id != contact_id:
            return Response({'msg': "文件名重复，请检查是否为同一文件"},
                            status=status.HTTP_202_ACCEPTED)
        if file_obj:
            filepath = basedir + '/contract'
            filedir = os.path.join(filepath, contract_name)
            with open(filedir, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        contract = self.get_object()
        contract.is_delete = 1
        contract.remove_time = datetime.datetime.now()
        contract.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def file_iterator(self, file_name, chunk_size=512):
        '''
        # 用于形成二进制数据
        :return:
        '''
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    # @action(detail=False, methods=['POST'])
    # def contract(self, request):
    #     print(1111)
    #     print(request.data, 888)
    #     contract_name = request.data.get("contract_name")
    #     # contract_name = request.query_params.get('contract_name')
    #     filedir = basedir + '/contract/' + contract_name
    #     # lines = open(filedir, 'r', encoding='gbk').read()
    #     # cmd = "cat %s" %filedir
    #     # a = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    #     # lines = a.stdout.readlines()
    #     file = self.file_iterator(filedir)
    #     response = StreamingHttpResponse(file)
    #     response['Content-Type'] = 'application/txt'
    #     # 注意filename 这个是下载后的名字
    #     response['Content-Disposition'] = 'attachment;filename="{}"'.format(
    #         contract_name)
    #     return response

    @action(detail=False, methods=['POST'])
    def download(self, request):
        contract_name = request.data.get("contract_name")
        filedir = basedir + '/contract/' + contract_name
        file = open(filedir, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/msword'
        response['Content-Disposition'] = 'attachment;filename=' + contract_name
        return response


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

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
        vendor_name = request.query_params.get('vendor_name', None)
        if vendor_name:
            search_dict['vendor_name'] = vendor_name
        contact = request.query_params.get("contact", None)
        if contact:
            search_dict['contact__contains'] = contact
        phone = request.query_params.get("phone", None)
        if phone:
            search_dict['phone__contains'] = phone
        email = request.query_params.get("email", None)
        if email:
            search_dict['email__contains'] = email
        search_dict['is_delete'] = 0
        vendor_info = Vendor.objects.get_queryset().filter(**search_dict).order_by('-update_time')
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(vendor_info, pre_page)
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
            return Response(self.get_serializer(vendor_info, many=True).data)

    def destroy(self, request, *args, **kwargs):
        logger.info(request.data)
        vendor = self.get_object()
        device_info = vendor.device_set.all()
        if len(device_info):
            return Response({'msg': '该厂商下有关联设备'})
        vendor.is_delete = 1
        vendor.remove_time = datetime.datetime.now()
        vendor.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        logger.info(request.data)
        vendor_name = request.data.get('vendor_name', None)
        vendor_info = Vendor.objects.filter(vendor_name=vendor_name, is_delete=0).first()
        if vendor_info:
            return Response({'msg': "厂商名已存在"}, status=status.HTTP_409_CONFLICT)
        vendor = Vendor(**request.data)
        vendor.save()
        return Response({"msg": "保存成功"}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        logger.info(request.data)
        vendor_name = request.data.get('vendor_name', None)
        vendor_id = request.data.get('id')
        vendor = Vendor.objects.filter(vendor_name=vendor_name, is_delete=0).first()
        if vendor and vendor.id != vendor_id:
            return Response({'msg': "厂商名已存在"}, status=status.HTTP_409_CONFLICT)
        return super().update(request, *args, **kwargs)
