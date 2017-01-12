# -*- coding:utf-8 -*- #
'''
Created on 2017-1-7
@author: Leo
'''
import re
import numpy as np
import urllib.request as ur
import urllib
from lxml import etree
from mongodb_writer import insert_into_mongodb


class Tmall_product:
    def get_page(self, page, product_name):
        page = ur.urlopen("https://list.tmall.com/search_product.htm?s=" + str(page) + "&q=" + product_name + "&sort=s&style=g&type=pc#J_Filter")
        html = page.read().decode('GBK')
        page = re.findall("(?<=共)(.*?)(?=页)", html)[0]
        return page

    def parser(self, page, product_name):
        data_list = []
        try:
            URL = "https://list.tmall.com/search_product.htm?s=" + str(page) + "&q=" + product_name + "&sort=s&style=g&type=pc#J_Filter"
            print(URL)
            page = ur.urlopen(URL)
            html = page.read().decode('GBK')
            selector = etree.HTML(html)
        except Exception as err:
            print(err)
        
        link_name = selector.xpath('//div[@class="productTitle productTitle-spu"]/a[1]/@title')
        data_list.append(link_name)
        
        link = selector.xpath('//div[@class="productTitle productTitle-spu"]/a[1]/@href')
        data_list.append(link)
        
        insert_into_mongodb(data_list, "TmallProduct")

    def controller(self):
        data = urllib.parse.quote("耳机", encoding = "GBK")
        page = self.get_page(page=0, product_name=data)
        page_list = np.arange(0, 60*int(page), 60).tolist()
        for page in page_list:
            self.parser(page=page, product_name=data)
        #self.parser(0, data)

Tmall = Tmall_product()
Tmall.controller()
