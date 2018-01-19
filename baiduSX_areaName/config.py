#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: config.py.py 
@time: 2018/01/19 
"""

#请先配置配置文件

class basicConfig():
    def __init__(self):

        #四位数字id的起止范围
        self.cardNumStart = 4999 # 5000
        self.cardNumEnd = 7000

        self.processNum = 30 #进程数

        #配置抓取页面数
        self.maxPn = 21


        ######这里一般无需配置######################

        self.databaseName = 'baiduSX'
        self.collectionName = 'json_url_areaName_' + str(self.cardNumStart) + '_' + str(self.cardNumEnd)

        self.jsonFileName = 'json_data_' + str(self.cardNumStart) + '_' + str(self.cardNumEnd)
        self.inameCardNumFileName = 'iname_cardNum_search_cardNum_'  + str(self.cardNumStart) + '_' + str(self.cardNumEnd)

        #########################################
