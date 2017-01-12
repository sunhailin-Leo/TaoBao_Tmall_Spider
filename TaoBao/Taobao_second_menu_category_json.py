# -*- coding:utf-8 -*- #
'''
Created on 2017-1-9
@author: Leo
'''
import re
import json
import urllib.request as ur
from http import cookiejar
from TaoBao_product_comment_spider.mongodb_writer import insert_into_mongodb

class Second_menu_Json:
    def __init__(self):
        
        self.mainUrl = "https://www.taobao.com/"
        
        self.JsonUrl = "https://tce.alicdn.com/api/data.htm?ids=222887%2C222890%2C222889%2C222886%2C222906%2C222898%2C222907%2C222885%2C222895%2C222878%2C222908%2C222879%2C222893%2C222896%2C222918%2C222917%2C222888%2C222902%2C222880%2C222913%2C222910%2C222882%2C222883%2C222921%2C222899%2C222905%2C222881%2C222911%2C222894%2C222920%2C222914%2C222877%2C222919%2C222915%2C222922%2C222884%2C222912%2C222892%2C222900%2C222923%2C222909%2C222897%2C222891%2C222903%2C222901%2C222904%2C222916%2C222924"
    
    def mainPage_parser(self):
        cookie = cookiejar.CookieJar()
        opener = ur.build_opener(ur.HTTPCookieProcessor(cookie))
        request = ur.Request(self.mainUrl)
        html = opener.open(request).read().decode('UTF-8')
        data_dataid = re.findall("(?<=data-dataid=\")(.*?)(?=\")", html)
        return data_dataid
        
    def parser(self,data_dataid):
        html = ur.urlopen(self.JsonUrl).read().decode('UTF-8')
        jsonDict = json.loads(html)
        Each_link = []
        for each_dict in data_dataid:
            for each in jsonDict[each_dict]['value']['list']:
                each.pop('h')
                try:
                    each.pop('sys_tce_scene_rule_id')
                    Each_link.append(each)
                except:
                    Each_link.append(each)
       
        insert_into_mongodb(Each_link, "second_menu_json")
   
    def controller(self):
        self.parser(self.mainPage_parser())
    

Second = Second_menu_Json()
Second.controller()