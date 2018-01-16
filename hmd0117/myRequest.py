# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 下午5:57
# @Author  : Troy
# @Email   : liutao@zhenrongba.com
# @File    : myRequest.py
# @Software: PyCharm

import requests
import urllib2
import traceback
import time
# from  data5uUtil import data5uUtil

from mongodb_queue import MongoQueue

IP_queue = MongoQueue('delegateIPs', 'ips')



###############
class my_request():
    def __init__(self):
        # self.proxy_ip = '114.228.91.40:5671' #随即请求
        self.proxy_ip = '115.207.119.211:7305' #随即请求

        # zhima_API_url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        # resposne = requests.get(zhima_API_url)
        # tmp = resposne.text
        # self.new_IP = tmp.replace('\r\n', '')
        # print '成功获取新的代理IP：', self.new_IP
        #
        # IP_queue.push(self.new_IP)
        # time.sleep(2)

        # import logging
        # logger = logging.getLogger()
        # info = {'logger': logger}
        # my_data5uUtil = data5uUtil(info)
        #
        # self.proxy_ip = self.proxy_ip  #初始化随机取一个IP


        # print '当前IP为：', self.proxy_ip

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
        }

        ###########
        # datau5
        # # 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
        # order = "408d35b8159d4e89720febc363f65cd5";
        # # 获取IP的API接口
        # apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order;
        #
        # # 获取IP列表
        # res = urllib2.urlopen(apiUrl).read().strip("\n");
        # # 按照\n分割获取到的IP
        # ips = res.split("\n");
        # self.proxy_ip = ips[0]
        # print '目前代理：', ips[0]
        #############
        # self.getNewIP()


    #each time get a new IP:  每次都调用一下换IP
    def getNewIP(self):
        try:
            #zhi ma
            # url='http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
            # response = requests.get(url, headers = self.headers)

            #datau5
            # 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
            # order = "408d35b8159d4e89720febc363f65cd5";
            # order = "c2cf1e860b58d92b49417e8733d798fb";
            # # 获取IP的API接口
            # apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order;
            #
            # # 获取IP列表
            # res = urllib2.urlopen(apiUrl).read().strip("\n");
            # # 按照\n分割获取到的IP
            # ips = res.split("\n");
            # self.proxy_ip = ips[0]
            # ips = ['117.86.191.26:5612']

            # 从mongodb获取代理  报错的时候修改mongodb代理数据
            # new_ip = IP_queue.pop_IP()

            ips = ['49.67.99.151:7671']
            print '目前代理：', ips[0]


        except Exception as e:
            print e
        return ips[0]

    #GET requests & requests wtih delegate
    def commonGet(self, url):
        '''
        common request
        :param url:
        :return:
        '''
        try:
            response = requests.get(url, headers=self.headers)
        except Exception as e:
            # response = self.commonRquest(url)
            print e
        return response

    def GetWithDelegateIP(self,url):
        '''
        with delegate IPs  每次请求都用不同的IP
        :param url:
        :return:
        '''
        # try:
        proxies = {'http': self.getNewIP()}
        # print '当前代理IP：',self.getNewIP()
        response = requests.get(url, headers=self.headers, proxies = proxies, timeout=10)
        # except Exception as e:
        #     response = self.GetWithDelegateIP(url)
        return response

    #POST
    def commonPost(self,url, data):
        '''
        common request
        :param url:
        :return:
        '''
        try:
            response = requests.post(url, data=data, headers=self.headers, timeout=10)
        except Exception as e:
            # response = self.commonPost(url,data)
            print e
        return response

    def PostWithDelegateIP(self, url,data):
        '''
        with delegate IPs
        :param url:
        :return:
        '''
        try:
            proxies = {'http': self.getNewIP()}  #随机从redis中取得一个代理IP
            # print '当前代理IP：', self.proxy_ip

            response = requests.post(url, data=data,headers=self.headers, proxies = proxies, timeout=10)
        except Exception as e:
            # response = self.PostWithDelegateIP(url, data)
            print e
        return response

    #urllib2 request
    def commonUrllib2Request(self, url):
        '''
        common
        :param url:
        :return:
        '''
        try:
            response = ''
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request, timeout = 10)

        except Exception as e:
            # response = self.commonUrllib2Request(url)
            print e
        return response


    def urllib2RequestWithDelegateIP(self, url):
        '''
        with delegate IPs
        :param url:
        :return:
        '''
        try:
            response = ''
            # self.proxy_ip = self.proxy_ip
            proxies = {'http': self.getNewIP()}
            # print '当前代理IP：', self.proxy_ip

            proxy_s = urllib2.ProxyHandler(proxies)
            opener = urllib2.build_opener(proxy_s)
            urllib2.install_opener(opener)

            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request, timeout=10)

        except Exception as e:
            # response = self.urllib2RequestWithDelegateIP(url)
            print e
        return response





if __name__ == '__main__':
    my_request = my_request()
    my_request.getNewIP()



