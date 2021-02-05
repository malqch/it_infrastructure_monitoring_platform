import logging
from rest_framework.views import APIView
from rest_framework.response import Response
import os
import conf
import json
import urllib.request
import threading
import time
# from auth.views import MyAuthentication
import paramiko


logger = logging.getLogger('log')
basedir = os.path.abspath(os.path.dirname(__file__))


class BindMacView(APIView):
    @staticmethod
    def post(request):
        mac = request.data.get('mac', None)
        ks_name = request.data.get('ks_name', None)
        profile = request.data.get('profile', None)
        mac_list = os.popen("cobbler system list").read().split()

        if mac in mac_list:
            os.system("cobbler system remove --name={mac}".format(mac=mac) + "> /dev/null 2>&1")
        result = os.system(f"cobbler system add --name={mac} --mac={mac} --profile={profile} --kickstart=/var/lib/cobbler/kickstarts/{ks_name} --interface=eth0 > /dev/null 2>&1")
        logger.info(f"cobbler system add --name={mac} --mac={mac} --profile={profile} --kickstart=/var/lib/cobbler/kickstarts/{ks_name} --interface=eth0")
        if result == 0:
            return Response({"status": 10000, "msg": 'mac绑定成功'})
        else:
            return Response({"status": 10001, "msg": 'mac未绑定成功'})


class CallPmSnIpView(APIView):
    def get(self, request):
        sn = request.query_params.get("sn", None)
        ip = request.query_params.get("ip", None)
        threading.Thread(target=self.call_automation, args=(sn, ip)).start()
        return Response({"msg": "正在调用automation"})

    @staticmethod
    def call_automation(sn, ip):
        try:
            call_url = conf.AUTOMATION_URL + f'job_install/call_snip/?sn={sn}&ip={ip}'
            req = urllib.request.Request(call_url)
            response = urllib.request.urlopen(req)
            data = json.loads(response.read())
            logger.info(data)
            return Response({"msg": "请求成功"})
        except Exception as e:
            logger.error(e)
            return Response({"msg": "请求失败"})


class RemoveMacView(APIView):
    @staticmethod
    def post(request):
        macs = request.data
        res_list = []
        for mac in macs:
            result = os.system("cobbler system remove --name={mac}".format(
                mac=mac) + "> /dev/null 2>&1")
            if result == 0:
                res_list.append(result)
        if len(res_list) == len(macs):
            return Response({"msg": "mac删除成功"})
        else:
            return Response({"msg": "mac删除失败"})


class CheckPingView(APIView):
    @staticmethod
    def get(request):
        ip = request.query_params.get("ip", None)
        consequence = 1
        cmd = f"ping -c 3 {ip}|grep '0 received'|wc -l"
        logger.info(cmd)
        # ping检查过程
        for i in range(5):
            result = os.popen(cmd)
            outcome = result.readline().strip('\n').strip()
            if outcome == '0':
                consequence = 0
                break
            elif outcome == '1':
                time.sleep(1)

        # ping结果
        if consequence == 0:
            return Response({"msg": 'SUCCESS', "status": 10000})
        elif consequence == 1:
            return Response({"msg": "BOOTERROR", "status": 10001})


class ConfigIpView(APIView):
    @staticmethod
    def file_transfer(private_ip):
        """
        传配置文件到服务器上的函数
        """
        try:
            logger.info("开始上传config_hostnameip.py文件")
            logger.info(private_ip)
            path_file = basedir + '/config_hostnameip.py'
            transport = paramiko.Transport((f'{private_ip}', 22))
            transport.connect(username='root', password='P@ssw0rd')
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.put(path_file, '/tmp/config_hostnameip.py')
            transport.close()
            logger.info("config_hostnameip.py上传成功")
            return True
        except Exception as e:
            logger.error(e)
            logger.info("config_hostnameip.py上传失败")
            return False

    @staticmethod
    def ssh_connect(data, private_ip):
        """
        执行命令的函数
        """
        cmd1 = f'python /tmp/config_hostnameip.py {data.get("ip")} {data.get("hostname")} {data.get("netmask")} {data.get("gateway")} {private_ip} "{data.get("mac")}"'
        logger.info(cmd1)
        cmd2 = 'yes|rm /tmp/config_hostnameip.py'
        cmd3 = 'reboot'

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=private_ip, port=22, username='root',
                        password='P@ssw0rd')

            # 执行配置文件
            stdin1, stdout1, stderr1 = ssh.exec_command(cmd1)
            resout1 = stdout1.read().decode()
            reserr1 = stderr1.read().decode()
            # 删除配置文件
            stdin2, stdout2, stderr2 = ssh.exec_command(cmd2)
            resout2 = stdout2.read().decode()
            reserr2 = stderr2.read().decode()
            # 重启机器
            stdin3, stdout3, stderr3 = ssh.exec_command(cmd3)
            resout3 = stdout3.read().decode()
            reserr3 = stderr3.read().decode()
            ssh.close()
            print(resout1, reserr1, resout2, reserr2, resout3, reserr3, 99999999)
            return resout1, reserr1, resout2, reserr2, resout3, reserr3
        except Exception as e:
            logger.error(e)
            return False

    def post(self, request):
        data = request.data
        logger.info(data)
        private_ip = request.query_params.get("ip", None)
        logger.info(private_ip)
        try:
            trans_res = self.file_transfer(private_ip)
            if trans_res:
                exec_out, exec_err, rm_out, rm_err, re_out, re_err = self.ssh_connect(
                    data=data, private_ip=private_ip)
                if exec_err == '' and rm_err == '' and re_err == '':
                    return Response({"status": 10000, "msg": "配置成功"})
                elif exec_err != '':
                    logger.error(exec_err)
                    return Response({"status": 10001, "msg": "配置文件执行失败"})
                elif exec_err == '' and rm_err != '':
                    logger.error(rm_err)
                    return Response({"status": 10001, "msg": "配置文件删除失败"})
                elif exec_err == '' and rm_err == '' and re_err != '':
                    logger.error(re_err)
                    return Response({"status": 10001, "msg": "机器重启失败"})
                else:
                    return Response({"status": 10001, "msg": "执行错误"})
            else:
                return Response({"status": 10001, "msg": "文件上传失败"})
        except Exception as e:
            logger.error(e)
            return Response({"status": 10001, "msg": "ssh连接失败"})



