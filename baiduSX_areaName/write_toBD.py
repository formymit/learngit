# -*-coding:utf-8-*-
from mongodb_queue import MongoQueue
from config import basicConfig


myConfig = basicConfig()

spider_queue = MongoQueue(myConfig.databaseName, myConfig.collectionName)

for pn in range(1, myConfig.maxPn):
    for cardNum in range(myConfig.cardNumStart, myConfig.cardNumEnd):  # 4020  重写

        print('pn=' + str(pn) + '---' + str(cardNum))

        for each in ['北京', '天津', '河北', '山西', '内蒙古', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北',
                     '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆', '香港', '澳门','台湾']:
            url = str(cardNum) + '&iname=&areaName=' + each + '&pn=' + str(pn * 10)

            spider_queue.push(url)
