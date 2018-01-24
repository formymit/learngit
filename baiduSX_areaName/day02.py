#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: day01.py 
@time: 2018/01/03 
"""

import requests
import json
import time
from mongodb_queue import MongoQueue
import multiprocessing
from config import basicConfig
import traceback

import re
import sys

reload(sys)
sys.setdefaultencoding("utf8")


myConfig = basicConfig()
# spider_queue = MongoQueue(myConfig.databaseName, 'kw_words')
spider_queue = MongoQueue(myConfig.databaseName, 'test_kw_words')

# data_insert_queue = MongoQueue(myConfig.databaseName, myConfig.dataInsertCollecitonName)
data_insert_queue = MongoQueue(myConfig.databaseName, 'test0124_duibi')
data_insert_queue.clear()

caseCode_judge_queue = MongoQueue(myConfig.databaseName, 'test_judge0124_duibi')  #不用这种方法判重 没次自己的数组内
caseCode_judge_queue.clear()





headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
}


#################
#delegate
proxies = {'http': '180.95.168.104:3012'}


# 多进程
def getInfo():
    while True:
        try:
            url = spider_queue.pop()
            real_url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信被执行人名单&cardNum=' + url +'&rn=10&ie=utf-8&oe=utf-8&format=json&t=1514970458551&cb=jQuery110204907454377081921_1514968028687&_=1514968028769'
            print(real_url)
        except KeyError:
            print('No data...')
            break
        else:
            get_baidu(real_url, url)

            #优化：如果某一类url已经获取不到数据 的改变number没有意义则全部comple  &iname=&areaName=&pn=
            spider_queue.complete(url)


def get_baidu(url,url_set):
    try:
        head_length = len('/**/jQuery110204907454377081921_1514968028687(')

        response = requests.get(url, headers=headers, proxies=proxies)

        if len(response.text) > len('/**/jQuery110204907454377081921_1514968028687({"status":"0","t":"1514970458551","set_cache_time":"","data":[]});'):
            ######
            #这里应该做判断是是否还有数据 需要继续扩大深度的key
            #######
            my_str = response.text[head_length: -2]

            my_json = json.loads(my_str)

            result_list = my_json['data'][0]['result']
            # print(result_list)

            #保留一份json全的数据
           # with open(myConfig.jsonFileName + '_2', 'a') as f22:
               # f22.write(str(result_list) + '\n')
            judge_list = []
            #解析数据并且写入数据库 返回插入新数据条数
            count,judge_list = parseData(result_list, judge_list)

            #通过count判断是否抓下一页： 有新数据插入（count > 0）才进行下一页抓取
            # str(cardNum) + '&iname=&areaName=' + each + '&pn=' + str(pn * 10)
            while count > 0: #只要有新数据插入 不断增加pn继续抓取
                current_page = re.findall('&pn=(.*?)&', url)[0]
                next_page = int(current_page) + 10
                url = url.replace('&pn='+current_page+'&', '&pn='+str(next_page)+'&')
                response = requests.get(url, headers=headers, proxies=proxies)
                print '获取下一页：', url
                if len(response.text) > len(
                    '/**/jQuery110204907454377081921_1514968028687({"status":"0","t":"1514970458551","set_cache_time":"","data":[]});'):
                    my_str = response.text[head_length: -2]
                    my_json = json.loads(my_str)
                    result_list = my_json['data'][0]['result']
                    # 保留一份json全的数据
                   # with open(myConfig.jsonFileName+ '_2', 'a') as f23:
                        #f23.write(str(result_list) + '\n')
                    count,judge_list = parseData(result_list, judge_list)
                    print judge_list
                else:
                    count = 0
            #跳出while循环 记录一下此时next_page的值（if next_page > 800）  敌营的url中提取出iname

            # print(len(result_list))
        else:
            pass
            # with open(myConfig.inameCardNumFileName, 'a') as f:117.21.122.4:5623
            #     f.write('\n')
            # 请求不到数据 这一类cardNum 大于该pn的 全部设置完成
            #cardNum_set = url_set[:4]
            #pn_set = url_set[-4:]
           # spider_queue.complete_set(cardNum_set, pn_set)

    except Exception as e:
        traceback.print_exc()

def parseData(result_list, judge_list):
    try:
        count = 0  # 插入数据计数
        for each in result_list:  # 0的情况也能处理
            name = each['iname']
            cardNum = each['cardNum']

            caseCode = each['caseCode']
           # with open(myConfig.inameCardNumFileName + '_2', 'a') as f:
              #  f.write(name + ', ' + cardNum + '\n')
            print(name + ', ' + cardNum)
            # 插入数据库 如果有新数据 则返回flag=1 否则flag=0 从而判断是否抓>下一页
            # flag = data_insert_queue.dataPush(name + '_' + cardNum)
            # data_insert_queue.dataPush(name + '_' + cardNum)
            # flag = caseCode_judge_queue.dataPush(name + '_' + cardNum+ '_' + caseCode)
            #
            # if flag == 1:  # 插入成功
            #     count = count + 1

            ##################################
            #优化下一页策略  数组存放本次数据  判断 not in 则可以进行下一页 （大于1000页另算）
            item = name + '_' + cardNum+ '_' + caseCode

            if item not  in judge_list:
                count = count + 1

                judge_list.append(item)
            ##################################

    except Exception as e:
        print e
    finally:
        return count, judge_list

def process_crawler():
    process = []
    for i in range(myConfig.processNum):
        p = multiprocessing.Process(target=getInfo)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':

    # process_crawler()
    url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=失信被执行人名单&cardNum=&iname=制品&areaName=上海&pn=0&rn=10&ie=utf-8&oe=utf-8&format=json&t=1514970458551&cb=jQuery110204907454377081921_1514968028687&_=1514968028769'
    #
    get_baidu(url,'')
