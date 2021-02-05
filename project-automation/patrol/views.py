import datetime
import logging
from django.core.paginator import Paginator
from django.forms import model_to_dict
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from sys_auth.views import MyAuthentication
from patrol.models import Patrol, PatrolScript
from patrol.serializers import PatrolSerializer
from script.models import Script

logger = logging.getLogger('log')

class PatrolViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Patrol.objects.all()
    serializer_class = PatrolSerializer

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
        patrol_name = request.query_params.get('patrol_name')
        status = request.query_params.get('status')
        # 查询数据
        if status:
            search_dict['status'] =status
        if patrol_name:
            search_dict['patrol_name__contains'] = patrol_name
        search_dict['is_delete'] = 0
        patrol_list = Patrol.objects.get_queryset().filter(**search_dict).order_by('-create_time', 'id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(patrol_list, pre_page)
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
            return Response(self.get_serializer(patrol_list, many=True).data)

    def create(self, request, *args, **kwargs):
        patrol = Patrol.objects.filter(patrol_name=request.data.get('patrol_name'), is_delete=0).first()
        if not patrol:
            super().create(request, *args, **kwargs)
            patrol = Patrol.objects.filter(patrol_name=request.data.get('patrol_name'), is_delete=0).first()

            script_list = request.data.get('script')
            for script in script_list:
                patrol_script = PatrolScript()
                patrol_script.patrol_id = patrol.id
                if type(script) == int:
                    patrol_script.script_id = script
                else:
                    script_obj = Script.objects.filter(script_name=script).first()
                    patrol_script.script_id = script_obj.id
                patrol_script.save()
            data = {"result": "创建成功"}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            result = {'msg': '巡检任务名称已存在'}
            return Response(data=result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        patrol = Patrol.objects.filter(patrol_name=request.data.get('patrol_name'), is_delete=0).first()
        id = int(kwargs['pk'])
        if patrol and patrol.id != id:
            result = {'msg': '巡检任务名称已存在'}
            return Response(data=result, status=status.HTTP_409_CONFLICT)
        else:
            super().update(request, *args, **kwargs)
            script_list = request.data.get('script')
            PatrolScript.objects.filter(patrol_id=id).delete()
            for script in script_list:
                patrol_script = PatrolScript()
                patrol_script.patrol_id = id
                if type(script) == int:
                    patrol_script.script_id = script
                else:
                    script_obj = Script.objects.filter(script_name=script).first()
                    patrol_script.script_id = script_obj.id
                patrol_script.save()
            result = {"msg": "修改成功"}
            return Response(data=result, status=status.HTTP_200_OK)

    @action(detail=True, methods=["PUT"])
    def logic_delete(self, request, pk):
        id = int(pk)
        patrol = Patrol.objects.filter(id=id).first()
        patrol.is_delete = request.data.get('is_delete')
        patrol.save()
        result = model_to_dict(patrol)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='script')
    def get_script(self, request):
        patrol_id = request.query_params.get('id')
        if patrol_id:
            script_id_list = []
            scripts = PatrolScript.objects.filter(patrol_id=patrol_id).all()
            for script in scripts:
                script_id_list.append(script.script_id)
            script_info = Script.objects.filter(id__in=script_id_list, is_delete=0).all().values()
            return Response(data=script_info, status=status.HTTP_200_OK)
        else:
            result = {'msg': '缺少参数'}
            return Response(data=result, status=status.HTTP_204_NO_CONTENT)

    #
    # @action(detail=False, methods=['post'], url_path='generate_report')
    # def generate_report(self, request):
    #     import xlwt
    #     w = xlwt.Workbook()  # 创建一个Excel文件
    #     ws = w.add_sheet('巡检报告')  # 创建一个工作表
    #     # 采用坐标的形式定义表的第一行
    #     ws.write(0, 0, '脚本名称')
    #     ws.write(0, 1, '主机ip')
    #     ws.write(0, 2, '主机名')
    #     ws.write(0, 3, '执行时间')
    #     ws.write(0, 4, '执行结果')
    #     # 连接数据库
    #     import pymysql
    #     connect = pymysql.Connect(
    #         host='10.10.10.16',
    #         port=3306,
    #         user='root',
    #         passwd='@WSX3edc',
    #         db='test_automation',
    #         charset='utf8'
    #     )
    #     start_time = request.data.get('start_time')
    #     end_time = request.data.get('end_time')
    #     logger.info("写入中，请等待……")
    #     cursor = connect.cursor()
    #     # sql语句
    #     if start_time and end_time:
    #         sql = 'select script_name, network_ip, hostname, execute_time, execute_res, script_output ' \
    #               'from test_automation.automation_script_log where log_use=1 and execute_time > "%s" and execute_time < "%s"' % (
    #               start_time, end_time)
    #         try:
    #             cursor.execute(sql)  # 执行sql语句
    #             results = cursor.fetchall()  # 获取执行结果
    #             print("hello")  # 测试
    #             i = 1  # 坐标定义
    #             for row in results:
    #                 j = 0
    #                 for one in row:
    #                     ws.write(i, j, one)  # write函数的参数分别是行、列、要写入的数据
    #                     j = j + 1
    #                 i = i + 1  # 实现循环
    #         except Exception as e:
    #             print("error", e)
    #         connect.close()
    #         w.save('/home/cuixh/developer/workspace/mytest.xls')  # 将文件保存到指定目录下
    #     return Response(data=None, status=status.HTTP_200_OK)

    # def excel2Pdf(fromRootFolderPath, toRootFolderPath, excels):
    #     import win32com.client
    #     # 如果没有文件则提示后直接退出
    #     if (len(excels) < 1):
    #         return
    #     # 开始转换
    #     logger.info("\n【 Excel -> PDF 转换】")
    #     fromRootFolderPath = formatPath(fromRootFolderPath)
    #     toRootFolderPath = formatPath(toRootFolderPath)
    #     try:
    #         insertLog("\n打开 Excel 进程中...")
    #         excel = win32com.client.Dispatch("Excel.Application")
    #         excel.Visible = 0
    #         excel.DisplayAlerts = False
    #         wb = None
    #         ws = None
    #         for i in range(len(excels)):
    #             insertLog("\n" + str(i))
    #             fromFilePath = formatPath(excels[i])
    #             fromFileName = os.path.basename(fromFilePath)
    #             insertLog("原始文件：" + fromFilePath)
    #             if (isKeepFolderStructureVar.get() == 1):
    #                 subPath = fromFilePath[len(fromRootFolderPath) + 1: len(fromFilePath) - len(fromFileName)]
    #             else:
    #                 subPath = ""
    #             toSubFolderPath = os.path.join(toRootFolderPath, subPath)
    #             # 子文件夹创建
    #             if not os.path.exists(toSubFolderPath):
    #                 os.makedirs(toSubFolderPath)
    #             # 某文件出错不影响其他文件打印
    #             try:
    #                 wb = excel.Workbooks.Open(fromFilePath)
    #                 count = wb.Worksheets.Count
    #                 insertLog("此 Excel 一共有" + str(count) + "张表：")
    #                 for j in range(count):  # 工作表数量，一个工作簿可能有多张工作表
    #                     insertLog("\n转换第" + str(j + 1) + "张表中...")
    #                     if (count == 1):
    #                         toFileName = changeSufix2Pdf(fromFileName)  # 生成的文件名称
    #                     else:
    #                         toFileName = changeSufix2Pdf(addWorksheetsOrder(fromFileName, j + 1))  # 仅多张表时加序号
    #                     toFilePath = os.path.join(toSubFolderPath, toFileName)  # 生成的文件地址
    #                     insertLog("生成文件：" + toFilePath)
    #                     ws = wb.Worksheets(j + 1)  # 若为[0]则打包后会提示越界
    #                     ws.ExportAsFixedFormat(0, toFilePath)  # 每一张都需要打印
    #             except Exception as e:
    #                 insertLog(str(e))
    #         # 关闭 Excel 进程
    #         insertLog("\n所有 Excel 文件已转换完毕\n")
    #         insertLog("结束 Excel 进程中...")
    #         ws = None
    #         wb.Close()
    #         wb = None
    #         excel.Quit()
    #         excel = None
    #         insertLog("已结束 Excel 进程\n")
    #     except Exception as e:
    #         insertLog(str(e))
    #     finally:
    #         gc.collect()









