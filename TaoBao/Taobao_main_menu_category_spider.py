# -*- coding:utf-8 -*- #
'''
Created on 2017-1-6
@author: Leo
'''
import urllib.request as ur
from lxml import etree
from bs4 import BeautifulSoup
from TaoBao_product_comment_spider.mongodb_writer import insert_into_mongodb

class Menu_sppider:
    def __init__(self):
        self.Url = "https://www.taobao.com/"
        
    def parser(self):
        try:
            page = ur.urlopen(self.Url)
            html = page.read().decode('UTF-8')
            selector = etree.HTML(html)
        except Exception as err:
            print(err)
        
        product_category_menu_len = selector.xpath('/html/body/div[4]/div[1]/div[1]/div/ul/li')
        for i in range(1, len(product_category_menu_len) + 1):
            product_category = selector.xpath('/html/body/div[4]/div[1]/div[1]/div/ul/li[' + str(i) + ']/span/a/@href')
            product_category_name = selector.xpath('/html/body/div[4]/div[1]/div[1]/div/ul/li[' + str(i) + ']/span/a/text()')
            self.dict_maker(product_category, product_category_name)

    
    def dict_maker(self,category,category_name):
        category_dict_list = category + category_name
        insert_into_mongodb(category_dict_list,"menu") 
        

    def controller(self):
        
        self.parser()
    
    
Spider = Menu_sppider()
Spider.controller()
