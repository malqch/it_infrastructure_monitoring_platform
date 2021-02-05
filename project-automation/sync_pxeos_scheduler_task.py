from apscheduler.schedulers.blocking import BlockingScheduler
import paramiko
import base64
import json
import urllib.request


def sync_os_by_pxe():
    # 获取pxe列表
    headers = {"username": "admin", "password": "111111", "Content-type": "application/json"}
    pxe_url = "http://localhost:8004/automation/api/pxe_server/"
    req = urllib.request.Request(pxe_url, headers=headers)
    response = urllib.request.urlopen(req)
    pxe_infos = json.loads(response.read())
    print(pxe_infos)
    os_info = []
    for pxe_info in pxe_infos:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=pxe_info.get("pxe_server_ip"), port=22, username='root', password='P@ssw0rd', timeout=5)
            cmd1 = "cobbler profile list"
            stdin1, stdout1, stderr1 = ssh.exec_command(cmd1)
            profile_list = stdout1.read().decode("utf8")
            profile_list = str(profile_list).replace(" ", "").split("\n")
            profile_ks_content_list = []
            for profile in profile_list:
                if profile:
                    cmd2 = "cobbler profile getks --name %s" % profile
                    stdin2, stdout2, stderr2 = ssh.exec_command(cmd2)
                    ks_content = stdout2.read().decode("utf-8")
                    param = {"profile": profile, "ks_content": str(ks_content)}
                    profile_ks_content_list.append(param)
            os_info.append({"pxe_server_id": pxe_info.get("id"), "profile_ks_content_list": profile_ks_content_list})
        except Exception as e:
            print(e)
        finally:
            ssh.close()
    os_url = "http://localhost:8004/automation/api/pxe_server_os/allpxeos/"
    params = json.dumps(os_info)
    params = bytes(params, 'utf8')
    req = urllib.request.Request(os_url, data=params, headers=headers, method="POST")
    response = urllib.request.urlopen(req)
    os_infos = response.read()
    os_infos = json.loads(os_infos)
    print(os_infos)


scheduler = BlockingScheduler()
scheduler.add_job(func=sync_os_by_pxe, trigger='interval', seconds=20)

scheduler.start()
