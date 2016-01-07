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

"""
class ProxyCheck(object):
    def __init__(self,t_result_queue,t_proxylist_path,t_proxy_webpage,t_max_pageindex,\
                 t_httprequest="URLIB2",t_timeout = 3):
        self.timeout = t_timeout
        self.resultQueue = t_result_queue
        curdate = time.strftime("%Y%m%d")
        self.proxy_result_path= t_proxylist_path+curdate
        self.proxy_webpage = t_proxy_webpage
        self.proxy_maxpage_index = t_max_pageindex  #最大的page下标
        self.t_httprequest = t_httprequest

    def proxy_checking(self):
        print self.proxy_result_path
        try:
            filehd = open(self.proxy_result_path,"r")
        except Exception,e:
            Logging("error","error to read proxylist path")
            sys.exit(1)

        verify_url = "http://www.qq.com"

        for line in filehd.readlines():
            tlist = line.split(":")
            #print tlist[0]
            #print tlist[1]

            #注册一个proxy代理
            #The proxy address and port:
            proxyinfo={ \
                        'host':tlist[0],\
                        'port' : int(tlist[1]) \
                      }
            #create a handler for the proxy
            proxy_support = urllib2.ProxyHandler({"http":"http://%(host)s:%(port)d" % proxyinfo})
            #create an opener which uses this handler:
            opener=urllib2.build_opener(proxy_support)
            # Then we install this opener as the default opener for urllib2
            urllib2.install_opener(opener)

            #htmlpage = urllib2.urlopen("http://sebsauvage.net/").read(200000)
            proxyrequest = urllib2.Request(verify_url)
            proxyrequest.get_method = lambda : 'HEAD'
            proxyrequest.add_header("Accept-Language","zh-cn")    #加入头信息，这样可以避免403错误
            proxyrequest.add_header("Content-Type","text/html; charset=gb2312")
            proxyrequest.add_header("User-Agent",'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
            try:
                response = urllib2.urlopen(proxyrequest,timeout=3)
            except urllib2.HTTPError, e:
                print e.code
            except urllib2.URLError as e:
                if hasattr(e, 'code'):
                    print 'Error code:',e.code
                elif hasattr(e, 'reason'):
                    print 'Reason:',e.reason
            except Exception,e:
                 exc_type, exc_value, exc_tb = sys.exc_info()
                 #print 'the exc type is:', exc_type
                 #print 'the exc value is:', exc_value
                 #print 'the exc tb is:', exc_tb
                 traceback.print_exception(exc_type, exc_value, exc_tb)
            else:
                print "No exceptions caught"
                if  response:
                    print response.info()
                    print response.getcode()
                else:
                    print "response null"
            """"""
            except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
                print "The server couldn't fulfill the request"
                print "Error code:",e.code
                print "Return content:",e.read()
            except urllib2.URLError,e:
                print "Failed to reach the server"
                print "The reason:",e.reason
            except ValueError:
                pass
            except TypeError:
                pass
            except socket.timeout:
                print "timeout.."
                pass
            except socket.error:
                pass
            else:
                #something you should do
                pass  #其他异常的处理
            """"""
        filehd.close()
"""

#change to threading
class ProxyCheck(threading.Thread):
    def __init__(self,t_result_queue,t_proxylist_path,t_newproxylist_path,t_proxy_webpage,t_max_pageindex,\
                 t_httprequest="URLIB2",t_timeout = 3):
        threading.Thread.__init__(self)
        self.timeout = t_timeout
        self.resultQueue = t_result_queue
        curdate = time.strftime("%Y%m%d")
        self.proxy_result_path= t_proxylist_path+curdate+".conf"
        self.proxy_webpage = t_proxy_webpage
        self.proxy_maxpage_index = t_max_pageindex  #最大的page下标
        self.t_httprequest = t_httprequest
        self.okproxylistpath =t_newproxylist_path+curdate+".conf"

    def run(self):
        self.proxy_checking()

    def proxy_checking(self):
        print self.proxy_result_path
        try:
            filehd = open(self.proxy_result_path,"r")
        except Exception,e:
            Logging("error","error to read proxylist path")
            sys.exit(1)

        try:
            filehdother = open(self.okproxylistpath,"w")
        except Exception,e:
            Logging("error","error to write newproxylist path")
            sys.exit(1)

        verify_url = "http://www.qq.com"

        for line in filehd.readlines():
            tlist = line.split(":")
            #print tlist[0]
            #print tlist[1]

            #注册一个proxy代理
            #The proxy address and port:
            proxyinfo={ \
                        'host':tlist[0],\
                        'port' : int(tlist[1]) \
                      }
            #create a handler for the proxy
            proxy_support = urllib2.ProxyHandler({"http":"http://%(host)s:%(port)d" % proxyinfo})
            #create an opener which uses this handler:
            opener=urllib2.build_opener(proxy_support)
            # Then we install this opener as the default opener for urllib2
            urllib2.install_opener(opener)

            #htmlpage = urllib2.urlopen("http://sebsauvage.net/").read(200000)
            proxyrequest = urllib2.Request(verify_url)
            proxyrequest.get_method = lambda : 'HEAD'
            proxyrequest.add_header("Accept-Language","zh-cn")    #加入头信息，这样可以避免403错误
            proxyrequest.add_header("Content-Type","text/html; charset=gb2312")
            proxyrequest.add_header("User-Agent",'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
            try:
                response = urllib2.urlopen(proxyrequest,timeout=3)
                """
                if  response:
                    print response.info()
                    print response.getcode()
                else:
                    print "response null"
                """
            except urllib2.HTTPError, e:
                print e.code
            except urllib2.URLError as e:
                if hasattr(e, 'code'):
                    print 'Error code:',e.code
                elif hasattr(e, 'reason'):
                    print 'Reason:',e.reason
            except Exception,e:
                 exc_type, exc_value, exc_tb = sys.exc_info()
                 #print 'the exc type is:', exc_type
                 #print 'the exc value is:', exc_value
                 #print 'the exc tb is:', exc_tb
                 traceback.print_exception(exc_type, exc_value, exc_tb)
            else:
                print "No exceptions caught"
                if  response:
                    print response.info()
                    print response.getcode()
                    filehdother.writelines(tlist)
                else:
                    print "response null"
            """
            except urllib2.HTTPError,e:    #HTTPError必须排在URLError的前面
                print "The server couldn't fulfill the request"
                print "Error code:",e.code
                print "Return content:",e.read()
            except urllib2.URLError,e:
                print "Failed to reach the server"
                print "The reason:",e.reason
            except ValueError:
                pass
            except TypeError:
                pass
            except socket.timeout:
                print "timeout.."
                pass
            except socket.error:
                pass
            else:
                #something you should do
                pass  #其他异常的处理
            """
        filehd.close()
        filehdother.close()

if __name__ == '__main__':
    resQueue=Queue.Queue()
    url = "http://www.xicidaili.com/nn/"
    proxycheck = ProxyCheck(resQueue,"./conf/proxylist","./conf/newproxylist",url,5,"URLLIB2",3)
    #proxycheck.proxy_checking()
    proxycheck.start()
    proxycheck.join()