import os, sys
from subprocess import Popen, PIPE

bond_suse = '''DEVICE=bond0
BOOTPROTO=static
STARTMODE='auto'
IPADDR=ip
NETMASK=mask
USERCTL=no
BONDING_MASTER=yes
BONDING_SLAVE_0=eth0
BONDING_SLAVE_1=eth1
BONDING_MODULE_OPTS='miimon=200 mode=1'
'''

slave_suse = '''DEVICE='%s'
TYPE=Ethernet
BOOTPROTO=static
SLAVE=yes
STARTMODE='auto'
MASTER=bond0
'''

eth_suse = '''DEVICE=ifname
BOOTPROTO=static
IPADDR=ip
NETMASK=mask
USERCTL=no
STARTMODE='auto'
'''
bond_neo='''DEVICE=bond0
ONBOOT=yes
BOOTPROTO=static
IPADDR=ip
NETMASK=mask
GATEWAY=gateway
USERCTL=no
BONDING_OPTS="mode=1 miimon=100"
'''

slave_neo='''DEVICE='%s'
TYPE=Ethernet
BOOTPROTO=static
ONBOOT=yes
SLAVE=yes
MASTER=bond0
'''

eth_neo='''DEVICE=ifname
ONBOOT=yes
BOOTPROTO=static
IPADDR=ip
NETMASK=mask
GATEWAY=gateway
USERCTL=no
'''


def get_nicname(vip):
    cmd = 'ifconfig'
    p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    lines = p.stdout.read().strip().split('\n')

    sections = []
    sections.append([])
    count = 0
    for line in lines:
        if len(line) > 0:
            sections[count].append(line)
        else:
            count = count + 1
            sections.append([])
    nicnames = []
    for s in sections:
        nicname = {}
        for l in s:
            if not l.startswith(' ') and 'Link encap:' in l:
                nicname['nic'] = l[0:l.find('Link encap:')].strip()
            elif 'inet addr:' in l:
                l = l[l.find('inet addr:') + 10:-1]
                ip = ''
                for j in l:
                    if j != ' ':
                        ip = ip + j
                    else:
                        break
                nicname['ip'] = ip
        if nicname:
            nicnames.append(nicname)
    # print nicnames [{"nic": "em1", "ip": "10.10.10.102"}]
    for nicname in nicnames:
        if vip == nicname['ip']:
            # print ip, nicname
            return nicname['nic']


def get_slaves():
    slaves = []
    if os.path.exists('/proc/net/bonding/bond0'):
        with open('/proc/net/bonding/bond0', 'r') as fd:
            lines = fd.readlines()
            for line in lines:
                if line.startswith('Slave Interface'):
                    slaves.append(line.split(':')[1].strip())
    return slaves


def get_nicname_7(vip):
    cmd = 'ifconfig'
    p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    lines = p.stdout.read().strip().split('\n')

    sections = []
    sections.append([])
    count = 0
    for line in lines:
        nicname = {}
        if len(line) > 0:
            sections[count].append(line)
        else:
            count = count + 1
            sections.append([])
    nicnames = []
    for s in sections:
        flag = True
        for l in s:
            if flag and l.startswith('lo:'):
                break
            if flag and not l.startswith(' ') and 'flags=' in l:
                nicname['nic'] = l[0:l.find(':')].strip()
            elif flag and 'inet' in l and vip in l:
                return nicname['nic']


def get_nicname_suse15(vip):
    cmd = 'ip a'
    p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    lines = p.stdout.read().strip().split('\n')

    sections = []
    sections.append([])
    count = -1
    for line in lines:
        if line.startswith(' '):
            sections[count].append(line)
        else:
            count = count + 1
            sections.append([])
            sections[count].append(line)
    nicnames = []
    for s in sections:
        nicname = {}
        for l in s:
            if not l.startswith(' ') and '<BROADCAST' in l:
                nicname['nic'] = l.replace(" ", '').split(':')[1]
            elif 'inet ' in l:
                l = l[l.find('inet') + 5:-1]
                ip = ''
                for j in l:
                    if j != '/':
                        ip = ip + j
                    else:
                        break
                nicname['ip'] = ip
        if nicname:
            nicnames.append(nicname)
    # print nicnames
    for nicname in nicnames:
        if vip == nicname['ip']:
            # print ip, nicname
            return nicname['nic']


def modifyip(ip, netmask, gateway, private_ip, ifs):
    # modify bond infomation
    cmd = "cat /proc/version"
    p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    result = p.stdout.read()
    p.communicate()
    if 'suse' in result.lower():
        file = '/etc/sysconfig/network/ifcfg-bond0'
        cmd = "uname -r"
        p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        result = p.stdout.read()
        p.communicate()
        if result.startswith('3'):
            nicname = get_nicname(private_ip)
        else:
            nicname = get_nicname_suse15(private_ip)
        print(nicname)
        if len(ifs) == 2:
            bondstr = bond_suse
            bondstr = bondstr.replace('ip', ip)
            bondstr = bondstr.replace('mask', netmask)
            bondstr = bondstr.replace('eth0', ifs[0])
            bondstr = bondstr.replace('eth1', ifs[1])
            with open(file, 'w') as fd:
                fd.write(bondstr)
            config = 'default  ' + gateway
            with open(r'/etc/sysconfig/network/routes', 'w') as fd:
                fd.write(config)
                # modify eth infomation
            slaves = ifs
            for s in slaves:
                slavestr = slave_suse
                slavestr = slavestr % s
                fe = '/etc/sysconfig/network/ifcfg-' + s
                with open(fe, 'w') as fd:
                    fd.write(slavestr)
        else:
            if nicname:
                # modify eth infomation
                file = '/etc/sysconfig/network/ifcfg-' + nicname
                if os.path.exists(file):
                    import datetime
                    import shutil
                    start = datetime.datetime.now()
                    backfile = file + '.' + start.strftime("%Y-%m-%d") + '.bak'
                    shutil.copyfile(file, backfile)
                    ethstr = eth_suse
                    ethstr = ethstr.replace('ifname', nicname)
                    ethstr = ethstr.replace('ip', ip)
                    ethstr = ethstr.replace('mask', netmask)
                    with open(file, 'w') as fd:
                        fd.write(ethstr)
                    config = 'default  ' + gateway
                    with open(r'/etc/sysconfig/network/routes', 'w') as fd:
                        fd.write(config)
    else:
        cmd = "uname -r"
        p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        result = p.stdout.read()
        p.communicate()
        if result.startswith('2'):
            print('rhel6##################')
            file = '/etc/sysconfig/network-scripts/ifcfg-bond0'
            nicname = get_nicname(private_ip)
            if len(ifs) == 2:
                bondstr = bond_neo
                bondstr = bondstr.replace('ip', ip)
                bondstr = bondstr.replace('mask', netmask)
                bondstr = bondstr.replace('gateway', gateway)
                with open(file, 'w') as fd:
                    fd.write(bondstr)

                # modify eth infomation
                slaves = ifs
                for s in slaves:
                    slavestr = slave_neo
                    slavestr = slavestr % s
                    if os.path.exists(
                            '/etc/sysconfig/network-scripts/ifcfg-' + s):
                        fe = '/etc/sysconfig/network-scripts/ifcfg-' + s
                        with open(fe, 'w') as fd:
                            fd.write(slavestr)
            else:
                nicname = get_nicname(private_ip)
                if nicname:
                    # modify eth infomation
                    file = '/etc/sysconfig/network-scripts/ifcfg-' + nicname
                    if os.path.exists(file):
                        import datetime
                        import shutil
                        start = datetime.datetime.now()
                        backfile = file + '.' + start.strftime(
                            "%Y-%m-%d") + '.bak'
                        shutil.copyfile(file, backfile)
                        ethstr = eth_neo
                        ethstr = ethstr.replace('ifname', nicname)
                        ethstr = ethstr.replace('ip', ip)
                        ethstr = ethstr.replace('mask', netmask)
                        ethstr = ethstr.replace('gateway', gateway)
                        with open(file, 'w') as fd:
                            fd.write(ethstr)
        elif result.startswith('3'):
            print('rhel7##################')
            if len(ifs) == 2:
                print('team0')
                nicname = get_nicname_7(private_ip)
                cmd = "nmcli connection show --active|grep %s|tail -1" % nicname
                print(cmd)
                p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE,
                          shell=True)
                conname = ' '.join(p.stdout.read().split()[:-3])
                p.communicate()
                cmd = "nmcli connection show|sed -n '2,$p'|awk '{print $1}'"
                print(cmd)
                p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE,
                          shell=True)
                connames = p.stdout.readlines()
                p.communicate()
                for c in connames:
                    c = c.strip()
                    if c.strip() != conname:
                        # delete other connames
                        cmd = "nmcli connection delete %s " % c
                        print(cmd)
                        p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE,
                                  shell=True)
                        p.communicate()

                exchangeme_mask = lambda netmask: sum(
                    bin(int(i)).count('1') for i in netmask.split('.'))
                netmask = exchangeme_mask(netmask)
                cmd = "nmcli connection add type team con-name team0 ifname team0 ipv4.address %s/%s ipv4.gateway %s ipv4.method static " % (
                ip, netmask, gateway)
                print(cmd)
                p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE,
                          shell=True)
                result = p.stdout.read()
                p.communicate()

                for i in ifs:
                    print(i)
                    if i == conname:
                        cmd = "nmcli connection modify '%s' con-name %s ifname %s master team0" % (
                        conname, nicname, nicname)
                    else:
                        cmd = "nmcli connection add con-name %s ifname %s type team-slave master team0" % (
                        i, i)
                    print(cmd)
                    p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE,
                              shell=True)
                    result = p.stdout.read()
                    p.communicate()
            else:
                print('a nic')
                exchangeme_mask = lambda netmask: sum(
                    bin(int(i)).count('1') for i in netmask.split('.'))
                netmask = exchangeme_mask(netmask)
                nicname = get_nicname_7(private_ip)
                print(nicname)
                cmd = "nmcli connection show --active|grep %s|tail -1" % nicname
                p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE,
                          shell=True)
                conname = ' '.join(p.stdout.read().split()[:-3])
                p.communicate()

                cmd = "nmcli connection modify '%s' ipv4.address %s/%s ipv4.gateway %s ipv4.method static " % (
                conname, ip, netmask, gateway)

                print(cmd)
                p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE,
                          shell=True)
                iiresult = p.stdout.read()
                p.communicate()


def getifname(macs):
    cmd = "cat /proc/version"
    p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    result = p.stdout.read()
    p.communicate()
    if 'suse' in result.lower():
        cmd = "uname -r"
        p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        result = p.stdout.read()
        p.communicate()
        if result.startswith('3'):
            cmd = """ip link show|awk '{if(NR%2!=0){ORS=" "}else{ORS="\\n"}{print}}' |awk  '{print $2,$13}'"""
        else:
            cmd = """ip link show|awk '{if(NR%2!=0){ORS=" "}else{ORS="\\n"}{print}}' |awk  '{print $2,$17}'"""
        p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        result = p.stdout.readlines()
    else:
        cmd = "uname -r"
        p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        result = p.stdout.read()
        p.communicate()
        if result.startswith('2'):
            cmd = """ip link show|awk '{if(NR%2!=0){ORS=" "}else{ORS="\\n"}{print}}' |awk  '{print $2,$13}'"""
        else:
            cmd = """ip link show|awk '{if(NR%2!=0){ORS=" "}else{ORS="\\n"}{print}}' |awk  '{print $2,$15}'"""
        p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        result = p.stdout.readlines()
    ifs = []
    p.communicate()
    for i in macs:
        for j in result:
            if i in j:
                ifs.append(j.split()[0].strip(':'))
    return ifs


def modifyhostname(hostname):
    # change temp name
    cmd = "cat /proc/version"
    p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    result = p.stdout.read()
    p.communicate()
    if 'suse' in result.lower():
        cmd = "hostname " + hostname
        p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        result = p.stdout.read()
        p.communicate()
        print(result)
        # modify configuration file
        config = 'HOSTNAME=' + hostname + '\n'
        with open(r'/etc/HOSTNAME', 'w') as fd:
            fd.write(config)
    else:
        cmd = "uname -r"
        p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        result = p.stdout.read()
        p.communicate()
        if result.startswith('2'):
            cmd = "hostname " + hostname
            p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
            result = p.stdout.read()
            p.communicate()
            print(result)
            # modify configuration file
            config = 'HOSTNAME=' + hostname + '\n'
            with open(r'/etc/sysconfig/network', 'w') as fd:
                fd.write("NETWORKING=yes\n")
                fd.write(config)
        elif result.startswith('3'):
            cmd = "hostnamectl --static set-hostname " + hostname
            p = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
            result = p.stdout.read()
            p.communicate()


if __name__ == '__main__':
    ip = sys.argv[1]
    hostname = sys.argv[2]
    netmask = sys.argv[3]
    gateway = sys.argv[4]
    private_ip = sys.argv[5]
    ifs = sys.argv[6]
    ifs = eval(ifs)
    ifs = getifname(ifs)
    modifyhostname(hostname)
    modifyip(ip, netmask, gateway, private_ip, ifs)
