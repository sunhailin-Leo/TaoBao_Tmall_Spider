# TaoBao - Tmall Spider -- v0.1 beta
* @(编写者)[Leo|Bin]
* @(联系方式)[Leo:Email:379978424@qq.com]


**开发环境**：Python 3.4.1 (IDE:Eclipse PyDev)

**项目简介**：利用爬虫对于淘宝和天猫的首页目录信息，商品目录，以及商品评论信息进行抓取

- **功能** ：支持对于任一商品的评论信息进行提取，支持对于某类商品的所有列表进行抓取获取商品信息
- **不足** ：
    * 1、目前只支持使用MongoDB进行存储，后续将开放多种存储方式
    * 2、对于数据的清洗功能不强，获取回来的数据存在一部分多余数据
    * 3、部功能受限后台服务器的限制，或者测试的网络问题，耗时较长，没有使用多线程爬虫。


**使用说明**：
* 1、目前版本需要使用者有python3.3+的开发环境以及MongoDB的存储环境（后续版本会继续完善）

##交互核心代码实现：
### 代码块 - 1（MongoDB的写入处理）-- [mongodb_writer.py]
**概述功能**：
* 1、编写insert_into_mongodb方法，传入特定参数使用传入到不同的数据库中
* 2、编写select_from_mongodb方法，将一级目录的数据返回给TaoBao_second_menu_spider.py使用
``` python
def insert_into_mongodb(data_list, shop):
    if ...
    elif ...
    elif ...
    elif ...
    ...

def select_from_mongodb(select_from_db):
    if select_from_db == "menu":
        data_list = []
        for each_data in db.menu.find({}, {"_id": 0}):
            data_list.append(each_data)
        return data_list
```

### 代码块 - 2（User—agent池的构建）-- [user_agent_pool.py]
**概述功能**：
* 1、定义一个user-agent的list，里面已经写好了40个user-agent随机使用，只需要设定list索引的随机数即可。
``` python
# 初始化user-agent池
user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)",
              "AppleWebKit/537.36 (KHTML, like Gecko)",
              ...
             ]
```
