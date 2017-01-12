# -*- coding:utf-8 -*- #
'''
Created on 2017-1-7
@author: Leo,bin
'''
import time
import urllib.request as ur
from bs4 import BeautifulSoup
from TaoBao_product_comment_spider.mongodb_writer import select_from_mongodb
from TaoBao_product_comment_spider.mongodb_writer import insert_into_mongodb

class Second_menu:
    def __init__(self):
        pass         
    
    def parser(self, each_category):
        # 错误网址
        Error_list = []
        
        # UTF-8下正确解析的网站名
        Correct_list_utf_8 = []
        
        # GBK下正确解析的网站名
        Correct_list_gbk = []
        
        # UTF-8下正确解析的URL
        Correct_url_list_utf_8 = []
        
        # GBK下正确解析的URL
        Correct_url_list_gbk = []
        
        print("########### Mode : Start ###########")
        print("Waiting For a minute...............................")
        for each_url in each_category: 
            url = each_url['category']
            try:
                html = ur.urlopen(url).read().decode('utf-8')
                Correct_list_utf_8.append(each_url['category_name'])
                Correct_url_list_utf_8.append(each_url['category'])
            except: 
                try:
                    html = ur.urlopen(url).read().decode('GBK')
                    Correct_list_gbk.append(each_url['category_name'])
                    Correct_url_list_gbk.append(each_url['category'])
                except:
                    print("错误的:" + " ----- " + url)
                    Error_list.append(each_url['category_name'])

       
        try:
            print("########### Mode : UTF-8 Running ###########")
            utf_8_datalist = self.correct_url(Correct_url_list_utf_8,"UTF-8")
        except Exception as err:
            print("########### Mode : Sleeping ###########")
            print(err)
            time.sleep(10)
            self.correct_url(Correct_url_list_utf_8,"UTF-8")
        
        try:
            print("########### Mode : GBK Running ###########")
            GBK_datalist = self.correct_url(Correct_url_list_gbk,"GBK")
        except Exception as err:
            print("########### Mode : Sleeping ###########")
            print(err)
            time.sleep(10)
            self.correct_url(Correct_url_list_gbk,"GBK")   
        
        data_list = [utf_8_datalist[0] + GBK_datalist[0],utf_8_datalist[1] + GBK_datalist[1]]
        insert_into_mongodb(data_list, "second_menu")
        
    def correct_url(self,correct_list,decode_way):
        correct_url = []
        error_url = []
        data = []
        data_url = []
        data_list = []
        for url in correct_list:
            html = ur.urlopen(url).read().decode(decode_way)
            soup = BeautifulSoup(html,'lxml')
            dl = soup.select('div[data-spm-ab="static"] dl')
            if len(dl) == 0:
                error_url.append(url)
            else:
                correct_url.append(url)
                
            for i in dl:
                dt = i.select('dd a')
                for j in dt:
                    data.append(j.get_text())
                    if "http:" not in j.attrs['href']:
                        j.attrs['href'] = "https:" + j.attrs['href']
                    data_url.append(j.attrs['href'])
                           
        data_list.append(data)
        data_list.append(data_url)
        return data_list
        
    def controller(self):
        each_category = select_from_mongodb("menu")
        self.parser(each_category)
        print("########### Mode : Finish ###########")
    
    def test(self):
        data = []
        html = ur.urlopen("https://www.taobao.com/market/mei/hufu2014.php?spm=a21bo.50862.201867-links-4.28.JSiPea").read().decode('gbk')
        soup = BeautifulSoup(html,'lxml')
        dl = soup.select('div[data-spm-ab="static"] dl')
            
        for i in dl:
            dt = i.select('dd a')
            for j in dt:
                data.append(j.get_text())
        print(data)
                
S_menu = Second_menu()
# S_menu.controller()
S_menu.test()
    