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
from getVerifyImg import getImg
from lxml import etree
import re
from myRequest import my_request
import traceback

my_request = my_request()

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',

    }


def crawlMaxPage(key, verifyCode):
    '''
    获取不同关键词的搜索最大页数 然后构造参数放入mongodb
    :return:flag
    '''
    # t_request = my_request()

    # get the verifyCode
    # verifyCode = getImg()  # 判断是否获取&识别成功 否则循环

    #keyWrod-city
    # with open('/Users/liutao/Documents/hmd_lt/file/city.txt') as f:
    #     data = f.read()
    #     eleGroups = data.split('、')
    #     print len(eleGroups)
    #
    # for key in eleGroups:
    #     print key
    #
    #keyword-name
    # with open('/Users/liutao/Documents/hmd_lt/file/name.txt') as f:
    #     data = f.read()
    #     eleGroups = data.split(',')
    #     print len(eleGroups)
    #
    # for key in eleGroups:
    #     print key
    try:
        flag = 0
        url = 'http://shixin.court.gov.cn/findDisNew'
        data = {
            'currentPage': 1,
            'pName': u'%s'%key,
            'pCardNum': None,
            'pProvince': 0,
            'pCode': verifyCode,
            # 'captchaId':'5e1f607aeebf42e4bdfbda7b0c5b18ef'
            'captchaId': '3faa8e1cf8464ff881e083e4c840aaa1'
            # '68064a038e8e40ed8c2acdfd7e1ae952'

        }
        # print data
        response = my_request.PostWithDelegateIP(url, data)
        # print response.text
        pattern = u'共(.*?)条'
        result = re.findall(pattern, response.text)
        if len(result) != 0:
            flag = 1 #返回数据成功
            maxPage = result[0]
            print key, maxPage

            with open('name_maxPage.txt', 'a') as f2:
                f2.write(key + '\t' + maxPage + '\n')

            selector = etree.HTML(response.text)
            all_titles = selector.xpath('//a/@title')
            all_ids = selector.xpath('//a[@class="View"]/@id')

            for i in range(len(all_titles)):
                print(all_titles[i] + '\t' + all_ids[i])
                with open('name02_ID_keyName.txt', 'a') as f:
                    f.write(all_titles[i] + '\t' + all_ids[i] + '\n')

        else:
            #返回数据失败 可能是验证码失效 或者关键词搜索不到数据
            flag = 0

    except Exception as e:
        print e
    finally:
        return flag

#mongodb_queue  get maxPage
from mongodb_queue import MongoQueue
spider_queue = MongoQueue('gaofa','name02')

#
global verifyCode
verifyCode = getImg()

def infoMaxPageCrawler(verifyCode):

    while True:
        try:
            name = spider_queue.pop()
            print name
        except KeyError:
            print('队列咩有数据')
            break
        else:

            flag = crawlMaxPage(name,verifyCode)
            if flag == 1:  #succeed to get maxPage
                spider_queue.complete(name)
            else:
                spider_queue.setWait(name) #方便查看是否有数据
                verifyCode = getImg()
#
# #多进程 用global verifyCode 做全局管理
# import multiprocessing
# def process_crawler():
#     process= []
#     # num_cpus = multiprocessing.cpu_count()
#     # print('将启动进程数为: ', num_cpus)
#     for i in range(5):
#         p = multiprocessing.Process(target=infoMaxPageCrawler(verifyCode))
#         p.start()
#         process.append(p)
#     for p in process:
#         p.join()


def crawlIDs():
    '''
    第一步 先获取有效的ID
    :return:
    '''
    # get the verifyCode
    verifyCode = getImg()  # 判断是否获取&识别成功 否则循环
    for i in range(117, 600):
        time.sleep(1+ random.random())
        try:
            url = 'http://shixin.court.gov.cn/findDisNew'
            data = {
                'currentPage': i,
                'pName': '张文',
                'pCardNum': None,
                'pProvince': 0,
                'pCode': verifyCode,
                # 'captchaId':'5e1f607aeebf42e4bdfbda7b0c5b18ef'
                'captchaId': '3faa8e1cf8464ff881e083e4c840aaa1'
                # '68064a038e8e40ed8c2acdfd7e1ae952'

            }
            response = requests.post(url, data=data, headers=headers, timeout=10)

            #get the maxPage

            # 为空则重新请求验证码
            while len(response.text) < 10:  #这里有问题 会陷入死循环
                verifyCode = getImg()
                data = {
                    'currentPage': i,
                    'pName': '张文',
                    'pCardNum': None,
                    'pProvince': 0,
                    'pCode': verifyCode,
                    # 'captchaId':'5e1f607aeebf42e4bdfbda7b0c5b18ef'
                    'captchaId': '3faa8e1cf8464ff881e083e4c840aaa1'
                    # '68064a038e8e40ed8c2acdfd7e1ae952'

                }
                print len(response.text)
                response = requests.post(url, data=data, headers=headers, timeout=10) #请求不到数据会陷入死循环

            # print(response.text)
            selector = etree.HTML(response.text)
            all_titles = selector.xpath('//a/@title')
            all_ids = selector.xpath('//a[@class="View"]/@id')

            for i in range(len(all_titles)):
                print(all_titles[i] + '\t' + all_ids[i])
                with open('name_ID.txt', 'a') as f:
                    f.write(all_titles[i] + '\t' + all_ids[i] + '\n')

        except Exception as e:
            print trackback.print_exc()




def crawlDetails(i):
    '''
    抓去详细信息
    :return:
    '''

    global verifyCode



    flag = 0
    # get the verifyCode
    # verifyCode = getImg()  # 判断是否获取&识别成功 否则循环

    # with open('name_ID.txt') as f0:
    #     lines = f0.readlines()
    #
    # for line in lines:
    #     i = line.split('\t')[1]   #因为id后有回车
    #     print i
    # for i in range(701000020, 702000030):
    try:
        #mannual
        # verifyCode = 'ngqy'

        #可以随机生成 captchaId  匹配对应的imgcode
        url = 'http://shixin.court.gov.cn/disDetailNew?id='+str(i)+'&pCode='+ verifyCode +'&captchaId=3faa8e1cf8464ff881e083e4c840aaa2'
        print url
        response = my_request.GetWithDelegateIP(url)
        print response.text
        #为空则重新请求验证码  1. 为空  2。
            # flag = 1
        if len(response.text) < 10:

            verifyCode = getImg()
            url = 'http://shixin.court.gov.cn/disDetailNew?id=' + str(i) + '&pCode=' + verifyCode + '&captchaId=3faa8e1cf8464ff881e083e4c840aaa2'

            response = my_request.GetWithDelegateIP(url)
            print(response.text)

        if len(response.text) > 10:
            flag = 1


        #如果返回空数据则
        # time.sleep(2 + random.random())
    except Exception as e:
        print e
    #         print traceback
    #     finally:
    #         return flag
    return flag

# multiprocessing spider, get json data
# from mongodb_queue import MongoQueue
# import multiprocessing
# spider_queue = MongoQueue('gaofa','ids')




def infoCrawler():
    global verifyCode
    while True:
        try:
            t_id = spider_queue.pop()
            print(t_id)
        except KeyError:
            print('队列咩有数据')
            break
        else:
            print 'start-now the verifyCode is ', verifyCode

            flag= crawlDetails(t_id)  #同一个verifyCode？

            print 'end-now the verifyCode is ', verifyCode
            print 'flag is :',flag

        finally:
            if flag == 1:
                spider_queue.complete(t_id)

            # else:
            #     verifyCode = getImg()

# def process_crawler():
#     process= []
#     # num_cpus = multiprocessing.cpu_count()
#     # print('将启动进程数为: ', num_cpus)
#     for i in range(30):
#         p = multiprocessing.Process(target=infoCrawler())
#         p.start()
#         process.append(p)
#     for p in process:
#         p.join()



############
def countRpeat():
    with open('/Users/liutao/Documents/hmd_lt/city_maxPage.txt') as f:
        lines = f.readlines()
        new_lines = list(set(lines))
        print len(new_lines)

        with open('noRpeat_city_maxPage.txt','a') as f2:
            for each in new_lines:
                f2.write(each)


####
def countItems():
    sum = 0
    with open('noRpeat_city_maxPage.txt') as f2:

        try:
            lines = f2.readlines()
            for each in lines:
                num = each.split('\t')[1]
                sum = sum + int(num)
        except Exception as e:
            print(e)
    print sum







if __name__ == '__main__':

    # countRpeat()
    # countItems()
    # crawl()
    # crawlBySelenium()
    # post_crawl()
    # crawlDetails()
    # crawlIDs()

    # global verifyCode
    # crawlDetails()

    # infoCrawler(verifyCode)


    #
    # verifyCode = getImg()
    # crawlMaxPage(verifyCode)
    infoMaxPageCrawler(verifyCode)

    # process_crawler()

    # infoCrawler()

    # infoMaxPageCrawler()
    # process_crawler()

    #n组 captchaId-verifyCode对
    # cap_ver_dict = {}
    # for j in range(3):
    #     captchaId = 'dabe990a34d54ed9b9f8aa58b898532' + str(j)
    #     verifyCode = getImg(captchaId)
    #     cap_ver_dict[captchaId] = verifyCode
    # print type(cap_ver_dict)
    #
    # print cap_ver_dict
    # print type(cap_ver_dict)
    #
    # for key in cap_ver_dict:
    #     captchaId = key
    #     verifyCode = cap_ver_dict[key]
    #
    #     infoCrawler(verifyCode, captchaId)


    # verifyCode = getImg(captchaId)  # 判断是否获取&识别成功 否则循环
    # infoCrawler(verifyCode, captchaId)

