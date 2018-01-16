# -*- coding: utf-8 -*-
# @Time    : 2018/1/16 下午8:30
# @Author  : Troy
# @Email   : liutao@zhenrongba.com
# @File    : test.py
# @Software: PyCharm

import requests
#
# resposne = requests.get(
#     'http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
#
# print resposne.text


dada = '106.111.209.106:2444\r\n'

data = dada.replace('\r\n','')
print data