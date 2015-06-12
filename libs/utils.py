#-*- coding: utf-8 -*-

import os
import subprocess
import re
import random
import time
import getpass


def shell(cmd):
    process = subprocess.Popen(
        args=cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    std_out, std_err = process.communicate()
    return_code = process.poll()
    return return_code, std_out, std_err


def get_hostname():
    cmd = "hostname "
    rc, so, se = shell(cmd)

    if rc == 0:
        return so


def get_inner_ip():
    cmd = "hostname -i"
    rc, so, se = shell(cmd)

    if rc == 0:
        return so


def get_extra_ip():
    """ 获取公网 IP.

    """
    cmd = ''' /sbin/ifconfig |grep "inet addr:" |egrep -v "127.0.0.1|10\.|192\.168\." |awk '{print $2}' |awk -F ":" '{print $2}' '''
    rc, so, se = shell(cmd)

    if rc == 0:
        return so


def is_valid_ip(ip):
    """ 检查 ip 是否合法.

    """
    p = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

    s = p.findall(ip.strip())
    if s == []:
        return False

    return len([i for i in s[0].split('.') if (0 <= int(i) <= 255)]) == 4


def mac_random():
    mac = [0x00, 0x16, 0x3e, random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff), random.randint(0x00, 0xff)]
    s = []
    for item in mac:
        s.append(str("%02x" % item))

    return ':'.join(s)


def ping(ip):
    cmd = "ping -c 3 %s &>/dev/null " % ip

    rc, so, se = shell(cmd)
    if rc == 0:
        return True
    else:
        return False


def dns_check(hostname):
    cmd = "nslookup %s &>/dev/null " % hostname

    rc, so, se = shell(cmd)
    if rc == 0:
        return True
    else:
        return False


def check_wait(check_cmd, post_cmd, timeinit=0, interval=10, timeout=600):
    """ 循环等待某一条件成功,就执行 post_cmd,时间超过 timeout 就超时.

    """
    timetotal = timeinit

    while timetotal < timeout:
        rc, ro, re = shell(check_cmd)
        if rc == 0:
            rc, ro, re = shell(post_cmd)
            if rc == 0:
                return True
            else:
                return False

        time.sleep(interval)
        timetotal += interval

    return False


def check_wait_null(check_cmd, timeinit=0, interval=10, timeout=600):
    """ 循环等待某一条件成功,返回 True, 时间超过 timeout 就超时.

    """
    timetotal = timeinit

    while timetotal < timeout:
        rc, ro, re = shell(check_cmd)
        if rc == 0:
            return True

        time.sleep(interval)
        timetotal += interval

    return False


def dns_resolv(hostnames=None):
    if hostnames is None:
        return []
    ips = list()
    for hostname in hostnames:
        cmd = ''' nslookup %s |grep -v "#53" |grep "Address:" ''' % hostname
        rc, so, se = shell(cmd)
        if rc != 0:
            return False

        ip = so.strip().split(":")[-1].strip()
        ips.append(ip)
    return ips


def remote_cmd(host, cmd, user="", sshkey="", timeout=10):
    """ sshkey 是私钥文件路径.

    """
    if user == "":
        user_host = host
    else:
        user_host = "%s@%s" % (user, host)

    if sshkey != "":
        cmd = ''' ssh -oConnectTimeout=%s -oStrictHostKeyChecking=no -i %s %s "%s" ''' % (
            timeout, sshkey, user_host, cmd)
    else:
        cmd = ''' ssh -oConnectTimeout=%s -oStrictHostKeyChecking=no %s "%s" ''' % (
            timeout, user_host, cmd)

    rc, so, se = shell(cmd)
    return rc, so, se


def transfer_dir(hosts, local_dir, remote_dir, user="", sshkey="", timeout=10):
    # 如果不指定 user, 使用运行程序的用户.
    if user == "":
        user = getpass.getuser()

    # sshkey 是私钥文件路径
    if sshkey != "":
        sshkey_option = "-i %s" % sshkey
    else:
        sshkey_option = ""

    # 先修改目标文件夹权限, 否则可能因为权限问题无法传输.
    for host in hosts:
        cmd = "sudo chown %s:%s -R %s" % (
            user, user, remote_dir)
        rc, so, se = remote_cmd(host, cmd, user)
        if rc != 0:
            return False

    for host in hosts:
        # 如果本地文件夹不存在或者为空, 不做处理.
        if not os.path.isdir(local_dir):
            continue
        if os.listdir(local_dir) == []:
            continue

        # 执行传输
        cmd = "scp -r -oConnectTimeout=%s -oStrictHostKeyChecking=no %s %s/* %s@%s:%s" % (
            timeout, sshkey_option, local_dir, user, host, remote_dir)
        rc, so, se = shell(cmd)
        if rc != 0:
            return False

    return True
