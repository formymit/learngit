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
from recognize import captcha
from myRequest import my_request

from mongodb_queue import MongoQueue
IP_queue = MongoQueue('delegateIPs', 'ips')


my_request = my_request()


header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
    }


def getImg():
    try:
        verifyCode = 'abcd'

        # url = 'http://shixin.court.gov.cn/captchaNew.do?captchaId=3faa8e1cf8464ff881e083e4c840aaa2&random=0.3949822987926871'
        url = 'http://shixin.court.gov.cn/captchaNew.do?captchaId=3faa8e1cf8464ff881e083e4c840aaa1'

        for num in range(3, 4):
            print num

            print '重新请求新的验证码...'
            # response = commonUrllib2Request(url)
            response = my_request.urllib2RequestWithDelegateIP(url)

            with open('%s.jpg'%num, 'wb') as f:
                f.write(response.read())
            # time.sleep(1.5)

        #识别验证码
        cap = captcha()
        verifyCode = cap.show('3.jpg')
        print '新的验证码为：' + verifyCode

        #重新获取IP

    #不同错误的不同处理方式  验证码识别失败
    except Exception as e:
        print e
        print '递归获取验证码...'
        verifyCode = getImg()  # 出现识别失败的情况 重新请求获取

        #修改mongodb ip的值  重新请求获得IP 然后写入数据库  complete上一个
        # try:
        #     current_IP = IP_queue.pop_IP()
        #     IP_queue.complete(current_IP)
        #     print '重新获取新的代理IP写入mongodb...'
        #     zhima_API_url = 'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='
        #     resposne = requests.get(zhima_API_url)
        #     new_IP = resposne.text
        #     print '成功获取新的代理IP：', new_IP
        #     IP_queue.push(new_IP)
        # except Exception as e:
        #     print e

        #my_request.__init__()

        # verifyCode = getImg()  #出现识别失败的情况 重新请求获取

    # except TimeoutError:
    #     print 'Max retries exceeded...切换IP'
    #     my_request.__init__()


    return verifyCode

if __name__ == '__main__':
    getImg()