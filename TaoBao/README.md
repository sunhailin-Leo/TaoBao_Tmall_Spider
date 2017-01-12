# TaoBao Spider Project Introduction
#### 淘宝爬虫项目介绍
* @(编写者)[Leo]
* @(联系方式)[Leo:Email:379978424@qq.com]

**项目简介**：
* 1、利用Urllib框架请求Json页面或者解析请求html页面返回的代码，解析数据。
* 2、Json页面利用Json库进行解析，提取可用信息
* 3、普通页面分析网页代码结构（淘宝一般把数据丢在页面的Script代码块中），利用正则表达式进行find_all处理

##核心代码实现：
### 代码块 - 1（正则表达式类型）
``` python
page = ur.urlopen(self.Url)
html = page.read().decode('UTF-8')
page = re.findall("(?<=\"totalPage\":)(.*?)(?=,)", html)[0]
```
``` python
page = ur.urlopen(self.Url + str(begin_number))
html = page.read().decode('UTF-8')
get_json = re.findall("(?<=g_page_config = )(.*?)(?=};)", html)
```

### 代码块 - 2（BeautifulSoup类型）
``` python
product_category = selector.xpath('/html/body/div[4]/div[1]/div[1]/div/ul/li[' + str(i) + ']/span/a/@href')
product_category_name = selector.xpath('/html/body/div[4]/div[1]/div[1]/div/ul/li[' + str(i) + ']/span/a/text()')
```

### 代码块 - 3（Json类型）
``` python
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

```

