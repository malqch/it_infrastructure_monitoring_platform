#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @Time   :2020/7/2 16:31
# @Author  :CUIXIAOHUA
# @File   :ServerM.py


import psutil
import datetime
import os
import requests
from requests.exceptions import ReadTimeout
import time, sched
import socket
import json
from subprocess import Popen, PIPE

ip = "xxx"
port = "xxx"
api = 'xxx'
url = "http://localhost:8848/server_monitor/host/"


# 获取主机名
def get_hostname():
    hostname = socket.gethostname()
    return hostname

# 获取操作系统信息
def get_os_info():
    os_name = os.name
    if os_name == 'nt':
        print('This is Windows')
    elif os_name == 'posix':
        print('This is Linux')
    print(os_name)
    return os_name

# 判断是不是susu系统
def recognize_suse_system():
    cmd = 'cat /proc/version'
    p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    result = p.stdout.read()
    p.communicate()
    if b'suse' in result.lower():
        return True
    return False

#获取CPU信息
def get_cpu_info():
    cpu = {'start_time': 0, 'os_name': 0,'cpu_user': 0,  'cpu_system': 0, 'cpu_idle': 0,
           'cpu_percent': 0, 'all_percent': []}
    cpu_times = psutil.cpu_times_percent()
    if get_os_info() == 'nt':
        cpu['interrupt'] = cpu_times.interrupt
        cpu['os_name'] = "Windows"
    if get_os_info() == 'posix':
        cpu['nice'] = cpu_times.nice
        cpu['os_name'] = "Linux"
        cpu['iowait'] = cpu_times.iowait
        cpu['interrupt'] = cpu_times.irq + cpu_times.softirq
    cpu['all_percent'] = psutil.cpu_percent(interval=1, percpu=True)
    cpu['cpu_percent'] = psutil.cpu_percent(interval=1)
    cpu['cpu_user'] = cpu_times.user
    cpu['cpu_system'] = cpu_times.system
    cpu['cpu_idle'] = cpu_times.idle
    cpu['cpu_logical_count'] = psutil.cpu_count()
    cpu['cpu_count'] = psutil.cpu_count()
    start_time = get_time()
    cpu['start_time'] = start_time
    return cpu


#获取内存信息
def get_mem_info():
    mem = {"total_mem": 0, "mem_percent": 0, "mem_used": 0, "mem_free": 0}
    mem_info= psutil.virtual_memory()
    mem['total_mem'] = mem_info.total
    mem['mem_percent'] = mem_info.percent
    mem['mem_free'] = mem_info.free
    mem['mem_used'] = mem_info.used
    swap = psutil.swap_memory()
    mem['swap_percent'] = swap.percent
    mem['swap_used'] = swap.used
    mem['swap_free'] = swap.free
    if get_os_info() == "posix":
        # suse系统下没有shared监控
        if not recognize_suse_system():
            mem['shared'] = mem_info.shared
        mem['buffers'] = mem_info.buffers
        mem['cached'] = mem_info.cached
        mem['swap_sin'] = swap.sin
        mem['swap_sout'] = swap.sout
    return mem

#获取磁盘
def get_disk_info():
    disk_io = psutil.disk_io_counters()
    disk_read = disk_io.read_bytes/disk_io.read_time
    disk_write = disk_io.write_bytes/disk_io.write_time
    diskInfo = psutil.disk_partitions()
    disk_count = len(diskInfo)
    disk_dict = {}
    disk_list = []
    total_disk = 0
    used_disk = 0
    for disk in diskInfo:
        disk_info = {"disk_name": '', "mountpoint": 0, "fstype": 0, "opts": 0,
                     "disk_total": 0, "disk_used": 0, "disk_free": 0, "disk_percent": 0}
        disk_name = disk.device
        disk_info['mountpoint'] = disk.mountpoint
        disk_info['fstype'] = disk.fstype
        disk_info['opts'] = disk.opts
        disk_usage = psutil.disk_usage(disk.mountpoint)
        total_disk += disk_usage.total
        used_disk += disk_usage.used
        disk_info['disk_name'] = disk_name
        disk_info['disk_total'] = disk_usage.total
        disk_info['disk_used'] = disk_usage.used
        disk_info['disk_free'] = disk_usage.free
        disk_info['disk_percent'] = disk_usage.percent
        disk_list.append(disk_info)
    disk_dict = {"disk_detail": disk_list}
    disk_rate = "{0:.2f}".format((float(used_disk)/total_disk) * 100)
    total_disk = "{0:.2f}GB".format(total_disk/1024/1024/1024)
    used_disk = "{0:.2f}GB".format(used_disk/1024/1024/1024)
    disk_dict['disk_read'] = disk_read
    disk_dict['disk_write'] = disk_write
    disk_dict['disk_count'] = disk_count
    disk_dict['total_disk'] = total_disk
    disk_dict['used_disk'] = used_disk
    disk_dict['disk_rate'] = disk_rate
    return disk_dict

def get_process():
    process_list = []
    os_name = get_os_info()
    for each_process in psutil.process_iter():
        process = {'pid': 0, 'name': 0, 'status': 0, 'create_time': 0}
        pid = each_process.pid
        name = each_process.name()  # 进程名
        status = each_process.status()  # 进程的工作状态
        create_time = each_process.create_time()  # 进程的创建时间点
        cpu_times = each_process.cpu_times()  # 进程使用cpu的时间信息
        mem_info = each_process.memory_info()  # 进程使用内存
        # os_name = get_os_info()
        if os_name == 'posix':
            exe = each_process.exe()  # 进程的ｂｉｎ（安装路径）
            open_files = each_process.open_files()  # 进程打开的文件
            process["exe"] = exe
            process["open_files"] = open_files
        net_connections = each_process.connections()  # 进程相关网络链接
        num_threads = each_process.num_threads()  # 进程的线程数量
        process["pid"] = pid
        process["name"] = name
        process["status"] = status
        process["create_time"] = create_time
        process["cpu_times"] = cpu_times
        process["mem_info"] = mem_info
        process["net_connections"] = net_connections
        process["num_threads"] = num_threads
        process_list.append(process)
    return process_list

def get_network():
    network_info = {"net_io_counters":0, "net_connections": 0, "net_if_stats": 0}
    net_list = psutil.net_io_counters(pernic=True)
    net_io_counters = []
    for net in net_list:
        net_info = {'net_name': 0, 'packets_sent': 0, "packets_recv": 0, "bytes_sent": 0, "bytes_recv": 0}
        net_name = net
        packets_sent = net_list[net].packets_sent
        packets_recv = net_list[net].packets_recv
        bytes_sent = net_list[net].bytes_sent
        bytes_recv = net_list[net].bytes_recv
        errout = net_list[net].errout
        errin = net_list[net].errin
        dropin = net_list[net].dropin
        dropout = net_list[net].dropout
        # print(u"网卡接收流量 %s 网卡发送流量 %s" % (bytes_recv, bytes_sent))
        # print(u"发送数据包 %s 接收数据包 %s" % (packets_sent, packets_recv))
        net_info['net_name'] = net_name
        net_info['packets_sent'] = packets_sent
        net_info['packets_recv'] = packets_recv
        net_info['bytes_sent'] = bytes_sent
        net_info['bytes_recv'] = bytes_recv
        net_info['errout'] = errout
        net_info['errin'] = errin
        net_info['dropin'] = dropin
        net_info['dropout'] = dropout
        net_io_counters.append(net_info)
    network_info['net_io_counters'] = net_io_counters
    net_connections = psutil.net_connections()
    net_connections_info = []
    for net in net_connections:
        net_dict = {"ip": 0, "port": 0, "status": 0, "pid": 0}
        if recognize_suse_system():
            net_dict['ip'] = net.laddr[0]
            net_dict['port'] = net.laddr[1]
        else:
            net_dict['ip'] = net.laddr.ip
            net_dict['port'] = net.laddr.port
        net_dict['status'] = net.status
        net_dict['pid'] = net.pid
        net_connections_info.append(net_dict)
    net_stats_info = []
    # suse系统下没有net_if_stats的监控
    if not recognize_suse_system():
        net_stats = psutil.net_if_stats()
        for net in net_stats.items():
            net_stats_dict = {"net_name": 0, "net_speed": 0, "net_mtu": 0}
            net_stats_dict['net_name'] = net[0]
            net_stats_dict['net_speed'] = net[1].speed
            net_stats_dict['net_mtu'] = net[1].mtu
            net_stats_info.append(net_stats_dict)
        network_info['net_if_stats'] = net_stats_info
    return network_info

def get_time():
    # now time
    now_time = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
    print(now_time)
    # system start time
    start_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    print(u"system start time: %s" % datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
    return now_time, start_time

def get_host_ip():

    """
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def get_temperatures():
    temperatures = psutil.sensors_temperatures()
    return temperatures

def get_sensors_fans():
    fans = psutil.sensors_fans()
    return fans

def get_sensors_battery():
    battery = psutil.sensors_battery()
    return battery

def run_all():
    try:
        server_info = dict()
        # server_info = {"cpu": 0, "mem": 0, "disk": 0, "process": 0, "start_time": 0, "network": 0, "INSTALL_NAME": 0}
        server_info.update(get_cpu_info())
        server_info.update(get_disk_info())
        server_info.update(get_network())
        server_info['process']= len(get_process())
        server_info.update(get_mem_info())
        server_info['INSTALL_NAME'] = get_hostname()
        server_info['LOGIC_IP'] = get_host_ip()
        server_info['MONITOR_TYPE'] = 'SERVER'
        server_info['now_time'], server_info['start_time'] = get_time()
       # server_info['temperatures'] = get_temperatures()
       # server_info['fans'] = get_sensors_fans()
       # server_info['battery'] = get_sensors_battery()
        
        server_info = json.dumps(server_info)
        print(server_info)
        return server_info
    except Exception as e:
        print('Error occurred:', e)

def perform_command(cmd, inc):
    """
     Run itself again after inc seconds
    :param cmd:
    :param inc:
    :return:
    """
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    server_info = cmd()

    try:
        headers = {
            "Content-Type": 'application/json'
        }
        res = requests.post(url=url, data=server_info, headers=headers)
        print(res.status_code)
    except Exception as e:
        print(e)


def timming_exe(cmd, inc=60):
    schedule.enter(inc, 0, perform_command, (cmd, inc))
    schedule.run()  # Continue running until the scheduled time queue becomes empty
		
 
if __name__ == '__main__':
    schedule = sched.scheduler(time.time, time.sleep)
    print('show time after 60 seconds:')
    timming_exe(run_all, 1)




