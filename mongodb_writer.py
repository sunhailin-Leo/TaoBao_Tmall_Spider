# -*- coding:utf-8 -*- #
'''
Created on 2017-1-6
@author: Leo
'''
import datetime
from pymongo import MongoClient

conn = MongoClient('mongodb://localhost:27017')
db = conn.Taobao


def insert_into_mongodb(data_list, shop):
    if shop == "Taobao":
        comment_dict = {'auction_sku': data_list[0], 'auction_aucNumId': data_list[1], 'user_nick': data_list[2],
                        'user_vipLevel': data_list[3], 'user_rank':data_list[4], 'bidPriceMoney_amount': data_list[5],
                        'content': data_list[6], 'append': data_list[7], 'date': data_list[8]}
        try:
            db.TaobaoComment.insert(comment_dict)
        except Exception as err:
            print("[Error]" + str(datetime.datetime.now()) + "mongodb_writer:" + str(err))

    elif shop == "Tmall":
        comment_dict = {'auctionSku':data_list[0], 'aucNumId': data_list[1], 'rateCount':data_list[2],
                        'rateDate': data_list[3], 'appendCommentTime': data_list[4], 'appendCommentContent': data_list[5],
                        'cmsSource': data_list[6], 'displayUserNick': data_list[7], 'userVipLevel': data_list[8]}
        try:
            db.TmallComment.insert(comment_dict)
        except Exception as err:
            print("[Error]" + str(datetime.datetime.now()) + "mongodb_writer:" + str(err))

    elif shop == "TaoBaoProduct":
        product_dict = {'nid':data_list[0], 'raw_title': data_list[1], 'detail_url': data_list[2],
                        'view_price': data_list[3], 'item_loc': data_list[4], 'view_sales': data_list[5],
                        'comment_count': data_list[6], 'nick': data_list[7]}

        try:
            db.Product.insert(product_dict)
        except Exception as err:
            print("[Error]" + str(datetime.datetime.now()) + "mongodb_writer:" + str(err))

    elif shop == "TmallProduct":
        product_name = data_list[0]
        product_link = data_list[1]

        try:
            for i in range(len(product_name)):
                tmall_product_dict = {"product_name": product_name[i], "product_link": product_link[i]}
                db.TmallProduct.insert(tmall_product_dict)
        except Exception as err:
            print("[Error]" + str(datetime.datetime.now()) + "mongodb_writer:" + str(err))

    elif shop == "menu":
        # 将data_list切片
        data_list = [data_list[i:i+1] for i in range(0, len(data_list), 1)]

        for data in range(len(data_list)):
            if "https:" not in data_list[0 + data]:
                data_list[0 + data][0] = "https:" + data_list[0 + data]
            menu_dict = {"category_name": data_list[3 + data][0], "category": data_list[0 + data][0]}

            db.menu.insert(menu_dict)
            if data == 2:
                break
            print(menu_dict)

    elif shop == "second_menu":
        print("########### Mode : MongoDB Running ###########")
        print("Second Menu Writing.................")
        category = data_list[0]
        category_url = data_list[1]

        try:
            for i in range(len(category)):
                second_menu_dict = {"category_name": category[i], "category_url": category_url[i]}
                db.secondMenu.insert(second_menu_dict)
        except Exception as err:
            print("[Error]" + str(datetime.datetime.now()) + "mongodb_writer:" + str(err))
        print("Second Menu Writing Finish")

    elif shop == "second_menu_json":
        for each_dict in data_list:
            if len(each_dict) == 0:
                continue
            db.secondMenuJson.insert(each_dict)


def select_from_mongodb(select_from_db):
    if select_from_db == "menu":
        data_list = []
        for each_data in db.menu.find({}, {"_id": 0}):
            data_list.append(each_data)
        return data_list
