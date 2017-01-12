# -*- coding:utf-8 -*- #
'''
Created on 2017-1-6
@author: Leo
'''
import re
import json
import numpy as np
import urllib.request as ur
from TaoBao_product_comment_spider.mongodb_writer import insert_into_mongodb

class Product_parser:
    def __init__(self):
        
        ##
        # 淘宝爬物品需要自己换 ?q 后面的字段
        #
        ##
        self.Url = "https://s.taobao.com/search?q=iphone6&app=detailproduct&through=1&bcoffset=4&p4ppushleft=6%2C48&s="
    
    def get_page(self):
        page = ur.urlopen(self.Url)
        html = page.read().decode('UTF-8')
        page = re.findall("(?<=\"totalPage\":)(.*?)(?=,)", html)[0]
        return page
        
    def parser(self,begin_number):
        
        self.product_detail = []
        
        try:
            page = ur.urlopen(self.Url + str(begin_number))
            html = page.read().decode('UTF-8')
            print(self.Url + str(begin_number))
            get_json = re.findall("(?<=g_page_config = )(.*?)(?=};)", html)
             
            result = get_json[0] + "}"                                                                  
            jsonDict = json.loads(result)
            product_mods = jsonDict['mods']['itemlist']['data']['auctions']
            for each in product_mods:
                self.product_detail.append(each['nid'])
                self.product_detail.append(each['raw_title'])
                self.product_detail.append(each['detail_url'])
                self.product_detail.append(each['view_price'])
                self.product_detail.append(each['item_loc'])
                self.product_detail.append(each['view_sales'])
                try:
                    self.product_detail.append(each['comment_count'])
                except:
                    self.product_detail.append("评论为空")
                self.product_detail.append(each['nick'])
             
            # 将datalist切片 
            datalist = [self.product_detail[i:i+8] for i in range(0, len(self.product_detail), 8)]   
               
            for each_product in datalist:
                insert_into_mongodb(each_product,"TaoBaoProduct")
  
        except Exception as err:
            print(err)
    
    def controller(self):
        page = self.get_page()
        page_list = np.arange(0,44*int(page),44).tolist()
        for page_num in page_list:
            self.parser(page_num)

Products = Product_parser()
Products.controller()

        
