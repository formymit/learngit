#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: goafa.py 
@time: 2018/01/15 
"""
import requests
import time
import random


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
    }

def crawlDetails():
    '''
    抓去详细信息
    :return:
    '''
    for i in range(701000000, 701000020):
        try:
            verifyCode = 'ejsw'
            #可以随机生成 captchaId  匹配对应的imgcode
            url = 'http://shixin.court.gov.cn/disDetailNew?id='+str(i)+'&pCode='+ verifyCode +'&captchaId=3faa8e1cf8464ff881e083e4c840aaa1'

            #代理IP
            proxy_ip = '182.100.239.0:9756'
            proxies = {'http': proxy_ip}

            response = requests.get(url, headers=headers,  timeout=10)
            print(response.text)

            #如果返回空数据则
            time.sleep(1 + random.random())
        except Exception as e:
            print(e)
if __name__ == '__main__':

    # crawl()
    # crawlBySelenium()
    # post_crawl()
    crawlDetails()