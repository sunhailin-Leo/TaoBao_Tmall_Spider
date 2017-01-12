# -*- coding:utf-8 -*- #
'''
Created on 2017-1-7
@author: Leo
'''
import re
import json
import time
import random
import numpy as np
import urllib.request as ur
from bs4 import BeautifulSoup
from http import cookiejar
from TaoBao_product_comment_spider.mongodb_writer import insert_into_mongodb
from TaoBao_product_comment_spider.user_agent_pool import user_agent

class Tmall_parser:
    def __init__(self):
        
        self.productId = "41610798823"
        
        self.turnPage = 1
                
    def get_spuId_sellerId(self):
        
        # 入口地址
        Url = "https://detail.tmall.com/item.htm?id=" + self.productId
        cookie = cookiejar.CookieJar()
        opener = ur.build_opener(ur.HTTPCookieProcessor(cookie))
        request = ur.Request(Url)
        html = opener.open(request).read().decode('gbk')
        self.spuId = re.findall("(?<=&spuId=)(.*?)(?=\",)", html)[0]
        self.sellerId = re.findall("(?<=&sellerId=)(.*?)(?=&)", html)[0]
    
    def get_json_maxpage(self):
        # 拼凑Url地址，并通过opener打开json页面
        jsonURL = "https://rate.tmall.com/list_detail_rate.htm?itemId=" + self.productId + "&spuId=" + self.spuId + "&sellerId=" + self.sellerId + "&order=3&currentPage=" + str(self.turnPage) + "&append=0&content=1&tagId=&posi=&picture=&_ksTS=1483710289927_1269"
         
        # 利用
        cookie = cookiejar.CookieJar()
        opener = ur.build_opener(ur.HTTPCookieProcessor(cookie))
        request = ur.Request(jsonURL)
        html = opener.open(request).read().decode('GBK')
        html = re.sub('\'', '\"', re.sub("u'", "\"", html))
        jsonDict = json.loads("{" + html + "}")
        
        jsonMax = jsonDict['rateDetail']['paginator']['lastPage']
        
        return jsonMax
    
    def parser(self, page):
                
        # 循环置空list
        self.datalist = []
         
        # 拼凑Url地址，并通过opener打开json页面
        jsonURL = "https://rate.tmall.com/list_detail_rate.htm?itemId=" + self.productId + "&spuId=" + self.spuId + "&sellerId=" + self.sellerId + "&order=3&currentPage=" + str(page) + "&append=0&content=1&tagId=&posi=&picture=&_ksTS=1483710289927_1269"
         
        # 输出查看URL
        print(jsonURL)
        
        # 1、从agent池中随机获取一条agent
        rand = random.randint(0, len(user_agent) - 1)
        headers = {"user-Agent": user_agent[rand]}
        
        # 利用
        cookie = cookiejar.CookieJar()
        opener = ur.build_opener(ur.HTTPCookieProcessor(cookie))
        request = ur.Request(jsonURL, headers=headers)
        html = opener.open(request).read().decode('GBK')
        html = re.sub('\'', '\"', re.sub("u'", "\"", html))
        jsonDict = json.loads("{" + html + "}")
        
        jsonMax = jsonDict['rateDetail']['paginator']['lastPage']
        
        json_TmallProductComment = jsonDict['rateDetail']['rateList']
         
        for comment_list in json_TmallProductComment:
            self.datalist.append(comment_list['auctionSku'])
            self.datalist.append(self.productId)
            self.datalist.append(comment_list['rateContent'])
            self.datalist.append(comment_list['rateDate'])
            try:
                self.datalist.append(comment_list['appendComment']['commentTime'])
                self.datalist.append(comment_list['appendComment']['content'])
            except:
                self.datalist.append("无追加评论时间")
                self.datalist.append("无追加评论内容")
            self.datalist.append(comment_list['cmsSource'])
            self.datalist.append(comment_list['displayUserNick'])
            self.datalist.append(comment_list['userVipLevel'])
 
        # 将datalist切片 
        datalist = [self.datalist[i:i+9] for i in range(0, len(self.datalist), 9)]
        
        # 切片后传给mongodb 
        for each_list in datalist:
            insert_into_mongodb(each_list, "Tmall")
        
        # json翻页，直到json超过jsonMax页数跳出   
        if self.turnPage > jsonMax:
            return False
        return True
             
            
    def controller(self):
        try:
            self.get_spuId_sellerId()
        except:
            self.get_spuId_sellerId()
            
        maxPage = self.get_json_maxpage()
        page_list = np.arange(2, maxPage + 1, 1).tolist()
        random.shuffle(page_list)
        print(page_list)
        for page in page_list:
            try:
                time.sleep(random.random())
                self.parser(page)
            except:
                time.sleep(10)
                self.parser(page)
                
        

Tmall = Tmall_parser()
Tmall.controller()