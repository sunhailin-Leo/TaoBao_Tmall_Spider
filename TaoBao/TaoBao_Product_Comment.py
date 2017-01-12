# -*- coding:utf-8 -*- #
'''
Created on 2017-1-6
@author: Leo
'''

import json
import urllib.request as ur
from bs4 import BeautifulSoup
from http import cookiejar
from TaoBao_product_comment_spider.mongodb_writer import insert_into_mongodb

class TB_parser:
    def __init__(self):
        
        self.productId = "533014247056"
        
        self.turnPage = 0
        
        self.Flag = True
        
    def parser(self, page):
        
        # 循环置空list
        self.datalist = []
        
        # 拼凑Url地址，并通过opener打开json页面
        URL = "https://rate.taobao.com/feedRateList.htm?auctionNumId=" + self.productId + "&currentPageNum=" + str(page) + "&pageSize=20&_ksTS=1483692858553_1441"
        
        # 输出查看URL
        print(URL)
        
        # 利用
        cookie = cookiejar.CookieJar()
        opener = ur.build_opener(ur.HTTPCookieProcessor(cookie))
        request = ur.Request(URL)
        html = opener.open(request).read().decode('gbk').replace("(","").replace(")","")
        jsonDict = json.loads(html)
        json_TaobaoProductComment = jsonDict['comments']
        
        # 计算一页json的评论数的长度
        json_len = len(json_TaobaoProductComment)
        
        # 循环获取一页的评论
        for comment_details in json_TaobaoProductComment:
            self.datalist.append(comment_details['auction']['aucNumId'])
            self.datalist.append(comment_details['auction']['sku'])
            self.datalist.append(comment_details['user']['nick'])
            self.datalist.append(comment_details['user']['vipLevel'])
            self.datalist.append(comment_details['user']['rank'])
            
            try:
                self.datalist.append(comment_details['bidPriceMoney']['amount'])
            except:
                self.datalist.append("无详细数据")
            
            self.datalist.append(comment_details['content'])
            
            try:
                self.datalist.append(comment_details['append']['content'])
            except:
                self.datalist.append("无追加评论")
                
            self.datalist.append(comment_details['date'])
        
        # 将datalist切片 
        datalist = [self.datalist[i:i+9] for i in range(0, len(self.datalist), 9)]
        
        # 
        for each_list in datalist:
            insert_into_mongodb(each_list,"Taobao")
        
        if json_len < 20: 
            return False
        return True
            
    def controller(self):
        while self.Flag:
            try:
                self.turnPage += 1
                print(self.turnPage)
                self.Flag = self.parser(page = self.turnPage)
            except Exception as err:
                self.error_info = str(err)
                break

TB = TB_parser()
TB.controller()