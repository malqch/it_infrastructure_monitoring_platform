import json
import multiprocessing
import os
import time
import datetime
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
import logging
import paramiko
from django.core.paginator import Paginator
from dwebsocket import require_websocket, websocket
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from sys_auth.views import MyAuthentication
from conf import SCRIPT_PATH
from script import scheduler, bonus_redis
from script.models import Script, ScriptLog, ScriptTimedTask
from script.serializers import ScriptSerializer, ScriptLogSerializer, ScriptTimedTaskSerializer
from patrol.models import Patrol

logger = logging.getLogger('log')

class ScriptViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer

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
        category = request.query_params.get('category')
        script_type = request.query_params.get('scrip_type')
        script_name = request.query_params.get('name')
        use = request.query_params.get('use')
        id = request.query_params.get('id')
        # 查询数据
        if id:
            search_dict['id'] = id
        if category:
            search_dict['category__contains'] = category
        if script_type:
            search_dict['script_type__contains'] = script_type
        if script_name:
            search_dict['script_name__contains'] = script_name
        if use:
            search_dict['use'] = use
        search_dict['is_delete'] = 0
        script_list = Script.objects.get_queryset().filter(**search_dict).order_by('id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(script_list, pre_page)
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
            return Response(self.get_serializer(script_list, many=True).data)

    def create(self, request, *args, **kwargs):
        scripts = Script.objects.filter(script_name=request.data.get('script_name')).all()
        if len(scripts) == 0:
            with open(os.path.join(SCRIPT_PATH, request.data.get('script_name')), 'w') as f:
                f.write(request.data.get('content'))
            return super().create(request, *args, **kwargs)
        else:
            result = {'msg': '脚本名已存在'}
            return Response(result, status=status.HTTP_409_CONFLICT)

    def update(self, request, *args, **kwargs):
        with open(os.path.join(SCRIPT_PATH, request.data.get('script_name')), 'w') as f:
            f.write(request.data.get('content'))
        request.data['update_time'] = datetime.datetime.now()
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['post'], url_path='exec_script')
    def exec_script(self, request):
        """多个ip执行脚本"""
        uname = request.headers.get("username")
        script_name = request.data.get("script_name", None)
        param = request.data.get("param", None)
        host_info = request.data.get("host_info", None)
        uuid = request.data.get("uuid", None)
        if not script_name:
            result = {'msg': '请选择脚本名字！'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        p = multiprocessing.Process(target=self.task_thread, args=(uname, script_name, param, host_info, uuid, None, None))
        p.start()
        result = {'msg': '脚本正在执行中，请稍后查询！'}
        return Response(result, status=status.HTTP_200_OK)

    def task_thread(self, uname, script_name, param, host_info, uuid, patrol_name, use):
        """
        通过多线程执行多脚本
        :param script_name:
        :param param:
        :param host_info:
        :return:
        """
        with redis_lock(uuid) as lock:
            if lock:
                data = [(uname, script_name, param, hosts, uuid, patrol_name, use) for hosts in host_info]
                with ThreadPoolExecutor(max_workers=len(host_info)) as pool:
                    pool.map(self.__execu_script, data)

    def __execu_script(self, data):
        """
        执行脚本
        :param data:
        :return:
        """
        script_log = ScriptLog.objects.create(script_name=data[1], network_ip=data[3].get('network_ip', None),
                                              hostname=data[3].get('hostname', None), username=data[3].get('username', None), executor=data[0],
                                              execute_res='执行中', uuid=data[4], patrol_name=data[-2] or None, log_use=data[-1] or 0)
        local_file = os.path.join(SCRIPT_PATH, data[1])
        remote_file = '/home/' + data[1]
        if data[1].endswith('.py'):
            cmd = f"python {remote_file} {data[2]}"
        elif data[1].endswith('.sh'):
            cmd = f"bash {remote_file} {data[2]}"
        elif data[1].endswith('.pl') or data[1].endswith('.perl'):
            cmd = f"perl {remote_file} {data[2]}"
        else:
            cmd = ''
        # 执行脚本
        self.upload_execute_script(local_file, remote_file, data[3].get('network_ip', None), cmd, script_log,
                                   data[3].get('username', None), data[3].get('password', None), data[3].get('ssh_port', None))

    def upload_execute_script(self, local_file, remote_file, ip, cmd, script_log, username, passwd, ssh_port):
        """
        上传脚本到服务器并执行
        """
        try:
            logger.info("开始连接{ip}".format(ip=ip))
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, ssh_port, username=username, password=passwd, timeout=10)
            t = paramiko.Transport((ip, ssh_port))
            t.connect(username=username, password=passwd)
            # 上传脚本
            logger.info("正在上传脚本文件到{ip}".format(ip=ip))
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(local_file, remote_file)
            logger.info("脚本文件上传到{ip}成功".format(ip=ip))
            t.close()
            # 执行脚本
            logger.info("{ip}正在执行脚本".format(ip=ip))
            stdint, stdout, stderr = ssh.exec_command(cmd)
            out_res = stdout.readlines()
            logger.info("{ip}脚本执行结果：{res}".format(ip=ip, res=out_res))
            ScriptLog.objects.filter(id=script_log.id).update(script_output=out_res, execute_res='已完成')
            ssh.close()
        except Exception as e:
            ssh.close()
            ScriptLog.objects.filter(id=script_log.id).update(execute_res='执行失败：%s' % str(e))
            logger.error('{ip}脚本执行失败：{error}'.format(ip=ip, error=str(e)))

    @action(detail=False, methods=['post'], url_path='timing_exec_script')
    def timing_exec_script(self, request):
        """
        定时执行脚本任务
        :param request:
        :return:
        """
        # 接收参数
        timing_dict = dict()
        timing_dict['uname'] = request.headers.get("username")
        timing_dict['script_name'] = request.data.get("script_name", None)
        timing_dict['use'] = request.data.get("use", None)
        timing_dict['patrol_name'] = request.data.get("patrol_name", None)
        timing_dict['patrol_id'] = request.data.get("patrol_id", None)
        timing_dict['param'] = request.data.get("param", None)
        timing_dict['host_info'] = request.data.get("host_info", None)
        timing_dict['uuid'] = request.data.get("uuid", None)
        timing_dict['exec_type'] = request.data.get("exec_type")
        if timing_dict['exec_type'] == '定时执行':
            timing_dict['exec_time'] = request.data.get("exec_time", None)
        elif timing_dict['exec_type'] == '周期性执行':
            timing_dict['exec_time'] = request.data.get("cron_exec_time", None)
        else:
            timing_dict['exec_time'] = request.data.get("interval_exec_time", None)
        timing_dict['exec_week'] = request.data.get("exec_week", None)
        timing_dict['start_time'] = request.data.get("start_time", None)
        timing_dict['end_time'] = request.data.get("end_time", None)
        if not timing_dict['script_name']:
            result = {'msg': '请选择脚本名字！'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        # 执行条件
        job_dict = dict()
        if timing_dict['exec_type'] == "定时执行":
            job_dict['trigger'] = 'date'
            job_dict['run_date'] = timing_dict['exec_time']
        elif timing_dict['exec_type'] == "周期性执行":
            job_dict['trigger'] = 'cron'
            exec_time_list = timing_dict['exec_time'].split(' ')
            job_dict['year'] = exec_time_list[4]
            job_dict['month'] = exec_time_list[3]
            job_dict['day'] = exec_time_list[2]
            job_dict['hour'] = exec_time_list[1]
            job_dict['minute'] = exec_time_list[0]
            if timing_dict['exec_week']:
                job_dict['day_of_week'] = timing_dict['exec_week']
            if timing_dict['start_time']:
                job_dict['start_date'] = timing_dict['start_time']
            if timing_dict['end_time']:
                job_dict['end_date'] = timing_dict['end_time']
        else:
            job_dict['trigger'] = 'interval'
            exec_time_list = timing_dict['exec_time'].split('/')
            job_dict['hours'] = int(exec_time_list[0])
            job_dict['minutes'] = int(exec_time_list[1])
            job_dict['seconds'] = int(exec_time_list[2])
            if timing_dict['start_time']:
                job_dict['start_date'] = timing_dict['start_time']
            if timing_dict['end_time']:
                job_dict['end_date'] = timing_dict['end_time']
        job_dict['id'] = timing_dict['uuid']
        logger.info('定时任务执行条件：%s', job_dict)
        scheduler.add_job(func=ScriptViewSet().task_thread, args=(timing_dict['uname'], timing_dict['script_name'],
                                                       timing_dict['param'], timing_dict['host_info'],
                                                       timing_dict['uuid'], timing_dict['patrol_name'], timing_dict['use']), **job_dict)
        # 保存到数据库
        if timing_dict['use']:
            Patrol.objects.filter(id=timing_dict['patrol_id']).update(status='执行中', exec_time=timing_dict['exec_time'], uuid=timing_dict['uuid'])
            result = {'msg': '巡检任务添加成功'}
        else:
            ScriptTimedTask.objects.create(script_name=timing_dict['script_name'],
                                           host_info=json.dumps(timing_dict['host_info']),
                                           execute_type=timing_dict['exec_type'], execute_time=timing_dict['exec_time'],
                                           execute_week=timing_dict['exec_week'], start_time=timing_dict['start_time'],
                                           end_time=timing_dict['end_time'], executor=timing_dict['uname'],
                                           uuid=timing_dict['uuid'])
            result = {'msg': '定时任务添加成功'}
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='remove_timed_task')
    def remove_timed_task(self, request):
        """
        移除定时任务
        :param request:
        :return:
        """
        uuid = request.data.get('uuid', None)
        patrol_id = request.data.get('id', None)
        logger.info('待执行的定时任务:%s' % (scheduler.get_jobs()))
        if uuid:
            try:
                if scheduler.get_job(uuid):
                    scheduler.remove_job(uuid)
                    if patrol_id:
                        Patrol.objects.filter(id=patrol_id).update(is_delete=1)
                        result = {'msg': '巡检任务移除成功'}
                    else:
                        ScriptTimedTask.objects.filter(uuid=uuid).update(is_delete=1)
                        result = {'msg': '定时任务移除成功'}
                else:
                    if patrol_id:
                        Patrol.objects.filter(id=patrol_id).update(is_delete=1)
                        result = {'msg': '巡检任务移除成功'}
                    else:
                        ScriptTimedTask.objects.filter(uuid=uuid).update(is_delete=1)
                        result = {'msg': '定时任务移除成功'}
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                logger.info('任务移除失败:%s' % str(e))
                result = {'msg': '任务移除失败:%s' % str(e)}
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            result = {'msg': '未查询到任务id'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='pause_timed_task')
    def pause_timed_task(self, request):
        """
        暂停定时任务
        :param request:
        :return:
        """
        uuid = request.data.get('uuid', None)
        patrol_id = request.data.get('id', None)
        logger.info('待执行的定时任务:%s' % (scheduler.get_jobs()))
        if uuid:
            try:
                if scheduler.get_job(uuid):
                    scheduler.pause_job(uuid)
                    if patrol_id:
                        Patrol.objects.filter(id=patrol_id).update(status='已暂停')
                        result = {'msg': '巡检任务暂停成功'}
                    else:
                        ScriptTimedTask.objects.filter(uuid=uuid).update(status=1)
                        result = {'msg': '定时任务暂停成功'}
                    return Response(result, status=status.HTTP_200_OK)
                else:
                    # ScriptTimedTask.objects.filter(uuid=uuid).update(status=1)
                    logger.info('未查询到定时任务:%s信息' % uuid)
                    result = {'msg': '未查询到定时任务:%s信息' % uuid}
                    return Response(result, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.info('定时任务暂停失败:%s' % str(e))
                result = {'msg': '定时任务暂停失败:%s' % str(e)}
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            result = {'msg': '未查询到定时任务id'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='restart_timed_task')
    def resume_timed_task(self, request):
        """
        恢复定时任务
        :param request:
        :return:
        """
        uuid = request.data.get('uuid', None)
        patrol_id = request.data.get('id', None)
        logger.info('待执行的定时任务:%s' % (scheduler.get_jobs()))
        if uuid:
            try:
                if scheduler.get_job(uuid):
                    scheduler.resume_job(uuid)
                    if patrol_id:
                        Patrol.objects.filter(id=patrol_id).update(status='执行中')
                        result = {'msg': '巡检任务重启成功'}
                    else:
                        ScriptTimedTask.objects.filter(uuid=uuid).update(status=0)
                        result = {'msg': '定时任务重启成功'}
                else:
                    scheduled_task = ScriptTimedTask.objects.get(uuid=uuid)
                    if scheduled_task:
                        # 参数解析
                        timing_dict = dict()
                        timing_dict['uname'] = scheduled_task.executor
                        timing_dict['script_name'] = scheduled_task.script_name
                        timing_dict['param'] = scheduled_task.param
                        timing_dict['host_info'] = json.loads(scheduled_task.host_info)
                        timing_dict['uuid'] = scheduled_task.uuid
                        timing_dict['exec_type'] = scheduled_task.execute_type
                        timing_dict['exec_time'] = str(scheduled_task.execute_time)
                        timing_dict['exec_week'] = scheduled_task.execute_week
                        timing_dict['start_time'] = str(scheduled_task.start_time)
                        timing_dict['end_time'] = str(scheduled_task.end_time)
                        # 执行条件解析
                        job_dict = dict()
                        if timing_dict['exec_type'] == "定时执行":
                            job_dict['trigger'] = 'date'
                            job_dict['run_date'] = timing_dict['exec_time']
                        elif timing_dict['exec_type'] == "周期性执行":
                            job_dict['trigger'] = 'cron'
                            exec_time_list = timing_dict['exec_time'].split(' ')
                            job_dict['year'] = exec_time_list[4]
                            job_dict['month'] = exec_time_list[3]
                            job_dict['day'] = exec_time_list[2]
                            job_dict['hour'] = exec_time_list[1]
                            job_dict['minute'] = exec_time_list[0]
                            if timing_dict['exec_week']:
                                job_dict['day_of_week'] = timing_dict['exec_week']
                            if timing_dict['start_time']:
                                job_dict['start_date'] = timing_dict['start_time']
                            if timing_dict['end_time']:
                                job_dict['end_date'] = timing_dict['end_time']
                        else:
                            job_dict['trigger'] = 'interval'
                            exec_time_list = timing_dict['exec_time'].split('/')
                            job_dict['hours'] = int(exec_time_list[0])
                            job_dict['minutes'] = int(exec_time_list[1])
                            job_dict['seconds'] = int(exec_time_list[2])
                            if timing_dict['start_time']:
                                job_dict['start_date'] = timing_dict['start_time']
                            if timing_dict['end_time']:
                                job_dict['end_date'] = timing_dict['end_time']
                        job_dict['id'] = timing_dict['uuid']
                        logger.info('定时任务执行条件：%s', job_dict)
                        # 添加定时任务
                        scheduler.add_job(func=ScriptViewSet().task_thread, args=(timing_dict['uname'], timing_dict['script_name'],
                                                                       timing_dict['param'], timing_dict['host_info'],
                                                                       timing_dict['uuid'], None, None), **job_dict)
                        ScriptTimedTask.objects.filter(uuid=uuid).update(status=0)
                        result = {'msg': '定时任务:%s重启成功' % uuid}
                return Response(result, status=status.HTTP_200_OK)
            except Exception as e:
                logger.info('定时任务重启失败:%s' % str(e))
                result = {'msg': '定时任务重启失败:%s' % str(e)}
                return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            result = {'msg': '未查询到定时任务id'}
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

class ScriptLogViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = ScriptLog.objects.all()
    serializer_class = ScriptLogSerializer

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """# 定义条件查询参数
        search_dict = dict()
        script_name = request.query_params.get('name')
        log_use = request.query_params.get('log_use')
        # 查询数据
        if script_name:
            search_dict['script_name__contains'] = script_name
        if log_use:
            search_dict['log_use'] = log_use
        search_dict['is_delete'] = 0
        # 查询数据
        script_log_list = ScriptLog.objects.get_queryset().filter(**search_dict).order_by('-id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(script_log_list, pre_page)
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
            return Response(self.get_serializer(script_log_list, many=True).data)

class ScriptTimedTaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [MyAuthentication, ]
    queryset = ScriptTimedTask.objects.all()
    serializer_class = ScriptTimedTaskSerializer

    def list(self, request, *args, **kwargs):
        """
        重写查询方法，增加翻页功能
        :param request: 请求对象，从中获取查询字符串参数，包括翻页参数及条件查询参数
        :param args:
        :param kwargs:
        :return:
        """
        # 查询已启动的定时任务信息
        scheduled_tasks = scheduler.get_jobs()
        logger.info('已启动定时任务：%s' % scheduled_tasks)
        scheduled_tasks_id = [job.id for job in scheduled_tasks]
        ScriptTimedTask.objects.exclude(uuid__in=scheduled_tasks_id, is_delete=0).update(status=1)
        # 定义条件查询参数
        search_dict = dict()
        script_name = request.query_params.get('name', None)
        status = request.query_params.get('status', None)
        # 查询数据
        if script_name:
            search_dict['script_name__contains'] = script_name
        if status:
            search_dict['status'] = status
        script_timed_task_list = ScriptTimedTask.objects.get_queryset().filter(**search_dict, is_delete=0).order_by('-id')
        # 设置翻页
        current_page = int(request.query_params.get('current_page', 0))
        pre_page = int(request.query_params.get('pre_page', 0))
        if current_page != 0 and pre_page != 0:
            paginator = Paginator(script_timed_task_list, pre_page)
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
            return Response(self.get_serializer(script_timed_task_list, many=True).data)

# websocket请求长连接
@require_websocket
def executing_script(request):
    n = 0
    while True:
        time.sleep(1)
        message = ScriptLog.objects.filter(uuid=request.GET.get('uuid')).all()
        n += 1
        print('message', message)
        if message:
            message_dict = ScriptLogSerializer(message, many=True).data
            request.websocket.send(json.dumps(message_dict))
            execute_res_list = [info['execute_res'] for info in message_dict]
            print('result', execute_res_list)
            if '执行中' not in execute_res_list:
                request.websocket.close()
                break
        else:
            if n > 10:
                break

# redis分布式锁
@contextmanager
def redis_lock(name, timeout=(24 + 2) * 60 * 60):
    try:
        today_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key = f"scheduler.lock.{name}.{today_string}"
        logger.info(f"<Redis Lock> {key}")
        # nx: 不存在，key值设置为value，返回1，存在，不操作，返回0
        # ex: 设置超时
        lock = bonus_redis.set(key, value=1, nx=True, ex=timeout)
        yield lock
    finally:
        bonus_redis.delete(key) # 释放锁

# websocket请求长连接
@require_websocket
def immediate_exec_script(request):
    """立即执行脚本"""
    data = request.websocket.wait()
    data = json.loads(str(data, encoding="utf-8"))
    uname = data.get("username")
    script_name = data.get("script_name", None)
    param = data.get("param", None)
    host_info = data.get("host_info", None)
    uuid = data.get("uuid", None)
    if not script_name:
        result = {'msg': '请选择脚本名字！'}
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    # 日志存库
    script_log = ScriptLog.objects.create(script_name=script_name, network_ip=host_info[0].get('network_ip', None),
                                          hostname=host_info[0].get('hostname', None),
                                          username=host_info[0].get('username', None), executor=uname,
                                          execute_res='执行中', uuid=uuid)
    local_file = os.path.join(SCRIPT_PATH, script_name)
    remote_file = '/home/' + script_name
    if script_name.endswith('.py'):
        cmd = f"python {remote_file} {param}"
    elif script_name.endswith('.sh'):
        cmd = f"bash {remote_file} {param}"
    elif script_name.endswith('.pl') or script_name.endswith('.perl'):
        cmd = f"perl {remote_file} {param}"
    else:
        cmd = ''
    # 执行脚本
    upload_immediate_exec_script(request, local_file, remote_file, host_info[0].get('network_ip', None), cmd, script_log,
                                 host_info[0].get('username', None), host_info[0].get('password', None), host_info[0].get('ssh_port', 22))

def upload_immediate_exec_script(request, local_file, remote_file, ip, cmd, script_log, username, passwd, ssh_port):
    """
    上传脚本到服务器并执行
    """
    try:
        logger.info("开始连接{ip}".format(ip=ip))
        request.websocket.send('connect to {ip}'.format(ip=ip))
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, ssh_port, username=username, password=passwd, timeout=10)
        t = paramiko.Transport((ip, ssh_port))
        t.connect(username=username, password=passwd)
        # 上传脚本
        logger.info("正在上传脚本文件到{ip}".format(ip=ip))
        request.websocket.send('upload file to {ip}'.format(ip=ip))
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_file, remote_file)
        logger.info("脚本文件上传到{ip}成功".format(ip=ip))
        request.websocket.send('upload file to {ip} successful'.format(ip=ip))
        t.close()
        # 执行脚本
        logger.info("{ip}正在执行脚本".format(ip=ip))
        request.websocket.send('start script execution...')
        stdint, stdout, stderr = ssh.exec_command(cmd)
        # 循环发送消息给前端页面
        output_res = list()
        while True:
            nextline = stdout.readline().strip()
            if nextline:
                request.websocket.send(nextline)
                logger.info("{ip}脚本执行输出：{res}".format(ip=ip, res=nextline))
                output_res.append(nextline)
                time.sleep(1)
            else:
                ScriptLog.objects.filter(id=script_log.id).update(script_output=output_res, execute_res='已完成')
                break
        ssh.close()
    except Exception as e:
        ssh.close()
        request.websocket.send('{ip} script execution failed:{error}'.format(ip=ip, error=str(e)))
        ScriptLog.objects.filter(id=script_log.id).update(execute_res='执行失败：%s' % str(e))
        logger.error('{ip}脚本执行失败：{error}'.format(ip=ip, error=str(e)))
