#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = "pandaychen"

import threadpool
import socket
import requests
import time
import random
import argparse
import sys
import os
import Queue
import urllib2
import signal
import threading
from bs4 import BeautifulSoup
import traceback

from utils import *


class ProxyGetOnce(object):
    def __init__(self,t_result_queue,t_proxylist_path,t_proxy_webpage,t_max_pageindex,\
                 t_httprequest="URLIB2",t_timeout = 3):
        self.timeout = t_timeout
        self.resultQueue = t_result_queue
        curdate = time.strftime("%Y%m%d")
        self.proxy_result_path= t_proxylist_path+curdate+".conf"
        self.proxy_webpage = t_proxy_webpage
        self.proxy_maxpage_index = t_max_pageindex  #最大的page下标
        self.t_httprequest = t_httprequest

    def proxy_get(self):
        try:
            filehd = open(self.proxy_result_path,"w+")
        except Exception,e:
            Logging("error", "Error to open log file")
            sys.exit(1)

        if self.proxy_maxpage_index <= 0:
            Logging("error","proxy_maxpage_index zero")
            sys.exit(1)

        if not self.proxy_webpage:
            Logging("error","proxy webpage null")
            sys.exit(1)

        for page in range(1,self.proxy_maxpage_index):
            cur_proxy_page = self.proxy_webpage+str(page)
            print cur_proxy_page
            if self.t_httprequest == "URLLIB2":
                httprequest = urllib2.Request(cur_proxy_page)
                #如果不加上UA的话,部分服务器可能会返回500错误
                httprequest.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); zh-CN; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2')
                htmldoc = urllib2.urlopen(httprequest).read()
                soupobj = BeautifulSoup(htmldoc,"html.parser")
                #soupobj = BeautifulSoup(htmldoc)
                trs = soupobj.find('table', id='ip_list').find_all('tr')
                for tr in trs[1:]:
                    tds = tr.find_all('td')
                    ip = tds[2].text.strip()
                    port = tds[3].text.strip()
                    protocol = tds[6].text.strip()
                    #print ip,port,protocol
                    if protocol == 'HTTP' or protocol == 'HTTPS':
                        filehd.write('%s:%s\n' % (ip, port) )
                    self.resultQueue.put((protocol,ip,port))
            else:
                Logging("error","unknown httprequest")
                sys.exit(1)

        filehd.close()

        while True:
            try:
                obj = self.resultQueue.get(False)
                print obj
            except Queue.Empty:
                break


#change it to threading
class ProxyGet(threading.Thread):
    def __init__(self,t_result_queue,t_proxylist_path,t_proxy_webpage,t_max_pageindex,\
                 t_httprequest="URLIB2",t_timeout = 300):
        threading.Thread.__init__(self)
        self.timeout = t_timeout
        self.resultQueue = t_result_queue
        curdate = time.strftime("%Y%m%d")
        self.proxy_result_path= t_proxylist_path+curdate+".conf"
        self.proxy_webpage = t_proxy_webpage
        self.proxy_maxpage_index = t_max_pageindex  #最大的page下标
        self.t_httprequest = t_httprequest
        self.update_time = time.time()


    def run(self):
        self.proxy_get()

    def proxy_get(self):
        #在线程池中定时启动
        while True:
            cur_time = time.time()
            if cur_time - self.update_time <= self.timeout:
                time.sleep(1)
                continue

            self.update_time = cur_time
            print self.update_time
            Logging("errprtest","self.update_time")
            try:
                filehd = open(self.proxy_result_path,"w")
            except Exception,e:
                Logging("error", "Error to open log file")
                sys.exit(1)

            if self.proxy_maxpage_index <= 0:
                Logging("error","proxy_maxpage_index zero")
                sys.exit(1)

            if not self.proxy_webpage:
                Logging("error","proxy webpage null")
                sys.exit(1)

            for page in range(1,self.proxy_maxpage_index):
                cur_proxy_page = self.proxy_webpage+str(page)
                print cur_proxy_page
                if self.t_httprequest == "URLLIB2":
                    httprequest = urllib2.Request(cur_proxy_page)
                    #如果不加上UA的话,部分服务器可能会返回500错误
                    httprequest.add_header('User-Agent', 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); zh-CN; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2')
                    htmldoc = urllib2.urlopen(httprequest).read()
                    soupobj = BeautifulSoup(htmldoc,"html.parser")
                    #soupobj = BeautifulSoup(htmldoc)
                    trs = soupobj.find('table', id='ip_list').find_all('tr')
                    for tr in trs[1:]:
                        tds = tr.find_all('td')
                        ip = tds[2].text.strip()
                        port = tds[3].text.strip()
                        protocol = tds[6].text.strip()
                        #print ip,port,protocol
                        if protocol == 'HTTP' or protocol == 'HTTPS':
                            filehd.write('%s:%s\n' % (ip, port) )
                        self.resultQueue.put((protocol,ip,port))
                else:
                    Logging("error","unknown httprequest")
                    sys.exit(1)

            filehd.close()

            """
            while True:
                try:
                    obj = self.resultQueue.get(False)
                    print obj
                except Queue.Empty:
                    break
            """

if __name__ == '__main__':
    resQueue = Queue.Queue()
    url = "http://www.xicidaili.com/nn/"
    proxy=ProxyGet(resQueue,"./conf/proxylist",url,5,"URLLIB2",10)
    #call for start
    proxy.start()
    proxy.join()