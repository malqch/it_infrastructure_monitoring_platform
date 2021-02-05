import os,sys
from subprocess import Popen,PIPE


bond='''DEVICE=bond0
ONBOOT=yes
BOOTPROTO=static
IPADDR=ip
NETMASK=mask
GATEWAY=gateway
USERCTL=no
BONDING_OPTS="mode=1 miimon=100"
'''

slave='''DEVICE='%s'
TYPE=Ethernet
BOOTPROTO=static
ONBOOT=yes
SLAVE=yes
MASTER=bond0
'''

eth='''DEVICE=ifname
ONBOOT=yes
BOOTPROTO=static
IPADDR=ip
NETMASK=mask
GATEWAY=gateway
USERCTL=no
'''
##获得联通ip的网卡
def get_nicname(vip):
    cmd ='ifconfig'
    p=Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
    lines=p.stdout.read().strip().split('\n')
    
    sections=[]
    sections.append([])
    count=0
    for line in lines:
        if len(line)>0: 
            sections[count].append(line)
        else:
            count=count+1
            sections.append([])
    #网卡名称和ip对应关系
    nicnames=[]
    for s in sections:
        nicname={}
        for l in s:
            if not l.startswith(' ') and 'Link encap:' in l:
                nicname['nic']=l[0:l.find('Link encap:')].strip()
            elif 'inet addr:' in l:
                l=l[l.find('inet addr:')+10:-1]
                ip=''
                for j in l:
                    if j!=' ':
                        ip=ip+j
                    else:
                        break
                nicname['ip']=ip 
        if nicname:
            nicnames.append(nicname)
    #print nicnames
    #返回指定ip对应的网卡名
    for nicname in nicnames:
        if vip==nicname['ip']:
            #print ip, nicname
            return nicname['nic']


def get_nicname_7(vip):
    cmd ='ifconfig'
    p=Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
    lines=p.stdout.read().strip().split('\n')
    
    sections=[]
    sections.append([])
    count=0
    for line in lines:
        nicname={}
        if len(line)>0: 
            sections[count].append(line)
        else:
            count=count+1
            sections.append([])
    #网卡名称和ip对应关系
    nicnames=[]
    for s in sections:
        flag=True
        for l in s:
            if flag and l.startswith('lo:'):
                break
            if flag and not l.startswith(' ') and 'flags=' in l :
                nicname['nic']=l[0:l.find(':')].strip()
            elif flag and 'inet' in l and vip in l:
                return nicname['nic']
                #l=l[l.find('inet')+5:-1].split()[0]
                #nicname['ip']=l 
                #print nicname
                #nicnames.append(nicname)
                #flag=False
                #break
    #print '############'
    #print nicnames
    ##返回指定ip对应的网卡名
    #for nicname in nicnames:
    #    if vip==nicname['ip']:
    #        #print ip, nicname
    #        return nicname['nic']

def get_slaves():
    slaves=[]
    if os.path.exists('/proc/net/bonding/bond0'):
        with open('/proc/net/bonding/bond0','r') as fd:
            lines=fd.readlines()
            for line in lines:
                if line.startswith('Slave Interface'):
                    slaves.append(line.split(':')[1].strip())
    return slaves


#将ifname修改为指定的ip
def modifyip(ip,netmask,gateway,private_ip,ifs):
    # 修改为以下：
    # DEVICE=bond0
    # ONBOOT=yes
    # BOOTPROTO=static
    # IPADDR=172.30.10.60
    # NETMASK=255.255.255.0
    # GATEWAY=172.30.10.254
    # USERCTL=no
    # BONDING_OPTS="mode=1 miimon=100"

    # modify bond infomation
    cmd="uname -r"
    p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
    result = p.stdout.read()
    p.communicate()
    if result.startswith('2'):
        print('rhel6##################')
        file='/etc/sysconfig/network-scripts/ifcfg-bond0'
        nicname=get_nicname(private_ip)
        if len(ifs)==2:
            #修改
            bondstr=bond
            bondstr=bondstr.replace('ip',ip)
            bondstr=bondstr.replace('mask',netmask)
            bondstr=bondstr.replace('gateway',gateway)
            with open(file,'w') as fd:
                fd.write(bondstr)

            #modify eth infomation
            slaves=ifs 
            for s in slaves:
                slavestr=slave
                slavestr=slavestr % s
                if os.path.exists('/etc/sysconfig/network-scripts/ifcfg-'+s):
                    fe='/etc/sysconfig/network-scripts/ifcfg-'+s
                    with open(fe,'w') as fd:
                        fd.write(slavestr)
        else:
            nicname=get_nicname(private_ip)
            if nicname:
                # modify eth infomation
                file='/etc/sysconfig/network-scripts/ifcfg-'+nicname
                if os.path.exists(file):
                    #备份
                    import datetime
                    import shutil
                    start=datetime.datetime.now()
                    backfile=file+'.'+start.strftime("%Y-%m-%d")+'.bak'
                    shutil.copyfile(file,backfile)
                    #修改
                    ethstr=eth
                    ethstr=ethstr.replace('ifname',nicname)
                    ethstr=ethstr.replace('ip',ip)
                    ethstr=ethstr.replace('mask',netmask)
                    ethstr=ethstr.replace('gateway',gateway)
                    with open(file,'w') as fd:
                        fd.write(ethstr)
    elif result.startswith('3'):
        print('rhel7##################')
        if len(ifs)==2:
            print('team0')
            #根据ip获取devicename
            nicname=get_nicname_7(private_ip)
            cmd="nmcli connection show --active|grep %s|tail -1" % nicname
            print(cmd)
            p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
            conname =' '.join( p.stdout.read().split()[:-3])
            p.communicate()
            #删除不用con
            cmd="nmcli connection show|sed -n '2,$p'|awk '{print $1}'"
            print(cmd)
            p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
            connames= p.stdout.readlines()
            p.communicate()
            for c in connames:
                 c=c.strip()
                 if c.strip()!=conname:
                     #delete other connames
                     cmd="nmcli connection delete %s " % c
                     print(cmd)
                     p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
                     p.communicate()


            #新增team0
            exchangeme_mask=lambda netmask: sum(bin(int(i)).count('1') for i in netmask.split('.'))
            netmask=exchangeme_mask(netmask)
            cmd="nmcli connection add type team con-name team0 ifname team0 ipv4.address %s/%s ipv4.gateway %s ipv4.method static " % (ip,netmask,gateway)
            print(cmd)
            p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
            result = p.stdout.read()
            p.communicate()


            #修改名称 
            for i in ifs:
                print(i)
                if i == conname:
                    cmd="nmcli connection modify '%s' con-name %s ifname %s master team0" % (conname,nicname,nicname)
                else:
                    cmd="nmcli connection add con-name %s ifname %s type team-slave master team0" % (i,i)
                    # nmcli connection add con-name enp137s0f0 ifname enp137s0f0 master team0 type team-slave 
                print(cmd)
                p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
                result = p.stdout.read()
                p.communicate()
        else:
            print('a nic')
            exchangeme_mask=lambda netmask: sum(bin(int(i)).count('1') for i in netmask.split('.'))
            netmask=exchangeme_mask(netmask)
            nicname=get_nicname_7(private_ip)
            print(nicname)
            cmd="nmcli connection show --active|grep %s|tail -1" % nicname
            p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
            conname =' '.join( p.stdout.read().split()[:-3])
            p.communicate()
            
            cmd="nmcli connection modify '%s' ipv4.address %s/%s ipv4.gateway %s ipv4.method static " % (conname,ip,netmask,gateway)

            print(cmd)
            p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
            iiresult = p.stdout.read()
            p.communicate()
def getifname(macs):
    cmd="uname -r"
    p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
    result = p.stdout.read()
    p.communicate()
    if result.startswith('2'):
        cmd="""ip link show|awk '{if(NR%2!=0){ORS=" "}else{ORS="\\n"}{print}}' |awk  '{print $2,$13}'"""
    else:
        cmd="""ip link show|awk '{if(NR%2!=0){ORS=" "}else{ORS="\\n"}{print}}' |awk  '{print $2,$15}'"""
    p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
    result = p.stdout.readlines()
    ifs=[]
    p.communicate()
    for i in macs:
        for j in result:
            if i in j:
               ifs.append(j.split()[0].strip(':'))
    return ifs
        
def modifyhostname(hostname):
    #change temp name
    
    cmd="uname -r"
    p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
    result = p.stdout.read()
    p.communicate()
    if result.startswith('2'):
        cmd="hostname "+hostname
        p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
        result = p.stdout.read()
        p.communicate()
        print(result)
        #modify configuration file
        config='HOSTNAME='+hostname+'\n'
        with open(r'/etc/sysconfig/network','w') as fd:
            fd.write("NETWORKING=yes\n")
            fd.write(config)
    elif result.startswith('3'):
        cmd="hostnamectl --static set-hostname " + hostname
        p = Popen([cmd],stdout=PIPE,stdin=PIPE,stderr=PIPE,shell=True)
        result = p.stdout.read()
        p.communicate()

if __name__=='__main__':
    ip=sys.argv[1]
    hostname=sys.argv[2]
    netmask=sys.argv[3]
    gateway=sys.argv[4]
    private_ip=sys.argv[5]
    ifs=sys.argv[6]
    ifs=eval(ifs)
    ifs= getifname(ifs)
    modifyhostname(hostname)
    modifyip(ip,netmask,gateway,private_ip,ifs)
