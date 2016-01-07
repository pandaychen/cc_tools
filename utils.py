#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import os
import random
import socket
import struct
import re

g_expression = re.compile('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

def CheckIp(t_regex):
    global g_expression
    if g_expression.match(t_regex):
        return 1
    else:
       return 0

def RandomIpv4():
    ip_start = 0x14000001
    #ip_mod = 0xFFFFFFF0 - ip_start
    ip_end = 0xfffffff0
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_start, ip_end)))    #big-endian

def RandomIpv4Addr(t_ip,t_mask):

    if not CheckIp(t_ip):
        return None

    if t_mask<=0 or t_mask>32:
        return None

    RANDOM_IP_POOL=['192.168.10.222/25']
    str_ip = RANDOM_IP_POOL[random.randint(0,len(RANDOM_IP_POOL) - 1)]
    print str_ip
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mask = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I',socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    ip_addr_min=0
    ip_addr_max=0
    for i in range(31, 31 - int(str_ip_mask), -1):
        mask = mask | ( 1 << i)
        ip_addr_min = ip_addr & (mask & 0xffffffff)
        ip_addr_max = ip_addr | (~mask & 0xffffffff)

    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))


def RandomStr(randomlength=4):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def Logging(t_filename,t_logcontent):
    logpath = './log/'
    curdate = time.strftime("%Y%m%d")
    newpath = './log/'+t_filename+'_'+curdate

    if os.path.exists(logpath):
        pass
    else:
        os.mkdir(logpath)

    try:
        filehd = open(newpath,'a+')
        newcontent = '['+str(time.strftime("%Y-%m-%d %H:%M:%S"))+']'+t_logcontent+'\n'
        filehd.writelines(newcontent)
        filehd.close()
    except Exception,e:
        pass


def Readfile(t_fname):
    if t_fname == None:
        return None
    with open(t_fname, 'r') as f:
        return f.read()


def LoadCookiesConf():
    cookies = {}
    for temp in Readfile('./conf/cookies.conf').split(';'):
        tlist = temp.strip().split('=')
        if tlist[0] == '':
            continue
        cookies[tlist[0]] = '='.join(tlist[1:])

    return cookies
"""
def importdata(self):
    self.data = {}
    for i in self.readfile('data.txt').split('&'):
        t = i.strip().split('=')
        self.data[t[0]] = '='.join(t[1:])
"""

def LoadUrlConf():
    urls = []
    for temp in Readfile('./conf/attack_urls.conf').split('\n'):
        temp = temp.strip()
        if temp == '':
            continue
        urls.append(temp)
    return urls

def LoadUserAgentConf():
    useragents = []
    for temp in Readfile('./conf/useragent.conf').split('\n'):
        temp = temp.strip()
        if temp == '':
            continue
        useragents.append(temp)
    return useragents

def LoadProxyConf():
    proxylist = []
    curdate = time.strftime("%Y%m%d")
    proxyfile = "./conf/proxylist"+curdate+".conf"
    for temp in Readfile(proxyfile).split('\n'):
        if temp.strip() == '':
            continue
        proxylist.append({'http':'http://{0}/'.format(temp.strip())})

    return proxylist
