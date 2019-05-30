#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: qiChaCha.py 
@time: 2018/01/13 
"""

# 因为有代理 所以测试天眼查 启信宝 失败 repeat
import requests
import json

import sys
reload(sys)
sys.setdefaultencoding("utf8")

headers = {
    # app接口的强大之处 没有cookie拿到数据！
    # 'cookie':'UM_distinctid=160c0f1b20b6b6-026b74380db812-163f6654-fa000-160c0f1b20cc41; zg_did=%7B%22did%22%3A%20%22160c0f1c2544aa-06ad2bdb9b10ac-163f6654-fa000-160c0f1c25514f%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201515673151014%2C%22updated%22%3A%201515673151026%2C%22info%22%3A%201515673151018%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%2C%22cuid%22%3A%20%2250ba3b0cd14154304aa25fc450cc744d%22%7D; acw_tc=AQAAAL6JRkN4UQwAEsBwexmMAuyNenKm',
    # 'upgrade-insecure-requests':'1',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

def crawl():
    try:
        # for page in range(1,2):

            # url = 'https://wxa.qichacha.com/wxa/v1/base/advancedSearch?searchKey={%22name%22%3A%22%E7%AE%A1%E7%90%86%22}&searchIndex=multicondition&province=&cityCode=&sortField=&isSortAsc=&subIndustryCode=&industryCode=&registCapiBegin=&registCapiEnd=&startDateBegin=&startDateEnd=&pageIndex='+str(page)+'&hasPhone=&hasEmail=&token=2b112db2d5ba8048d65504b05c289eda'
            url = 'https://wxa.qichacha.com/wxa/v1/base/advancedSearch?searchKey=%7B%22name%22%3A%22%E8%B4%A2%E5%AF%8C%22%7D&searchIndex=multicondition&province=&cityCode=&sortField=&isSortAsc=&subIndustryCode=&industryCode=&registCapiBegin=&registCapiEnd=&startDateBegin=&startDateEnd=&pageIndex=1&hasPhone=&hasEmail=&token=2b112db2d5ba8048d65504b05c289eda'
            print url
            response = requests.get(url, headers=headers)
            myJson = json.loads(response.text, encoding='utf-8')
            result = myJson['result']['Result']
            for each in result:
                # print each
                name = each['Name']
                No = each['OrgNo']
                print name, No
            # print result


    except Exception as e:
        print e


if __name__ == '__main__':
    crawl()