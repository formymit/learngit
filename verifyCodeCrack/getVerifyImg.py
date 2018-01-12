#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: getVerifyImg.py 
@time: 2018/01/11 
"""

import requests
import urllib2
import time


header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
    }


def getImg(url):
    try:

        for num in range(1454, 2000):
            print num
            request = urllib2.Request(url, headers=header)
            response = urllib2.urlopen(request)

            with open('/Users/iBoy/learngit/verifyCodeCrack/train/'+'%s.jpg'%num, 'wb') as f:
                f.write(response.read())
            time.sleep(1.5)

    except Exception as e:
        print e

if __name__ == '__main__':
    url = 'http://shixin.court.gov.cn/captchaNew.do?captchaId=3faa8e1cf8464ff881e083e4c840aaa2&random=0.3949822987926871'
    getImg(url)