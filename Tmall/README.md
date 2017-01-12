# Tmall Spider Project Introduction
#### 天猫爬虫项目介绍
* @(编写者)[Leo]
* @(联系方式)[Leo:Email:379978424@qq.com]

**项目简介**：
* 1、利用Urllib框架请求Json页面或者解析请求html页面返回的代码，解析数据。
* 2、Json页面利用Json库进行解析，提取可用信息
* 3、天猫网页对于网页Url的顺序请求有检测，所以代码使用了一个不巧的办法进行解决

##核心代码实现：
### 代码块 - 1（对于请求顺序的处理）-- [Tmall_Product_Comment.py]
**概述功能**：
* 1、maxPage是利用BeautifulSoup获取商品最大页数（热门商品上限100页，冷门商品会有具体上限）
* 2、这里为了生成页数序号，利用了numpy科学计算库生成从第2页到最大页数的list
* 3、将方法2的list利用random库中的无返回的shuffle方法进行随机排序（经过random.shuffle的list会自动随机排列）
``` python
maxPage = self.get_json_maxpage()
page_list = np.arange(2, maxPage + 1, 1).tolist()
random.shuffle(page_list)
for page in page_list:
    try:
        time.sleep(random.random())
        self.parser(page)
    except:
        time.sleep(10)
        self.parser(page)
```

### 代码块 - 2（Json处理）-- [Tmall_Product_Comment.py]
**概述功能**：
* 1、这里的第二行和第三行代码看上去比较碍眼，因为json页面报过缺少双引号的错误以及头尾缺少花括号的包围
* 2、由于Json涉及的层次较多，所以变量名后面接的的中括号会增多，增加解析时间，降低运行速度
``` python
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
```

### 代码块 - 2（BeautifulSoup处理）-- [Tmall_Product.py]
**概述功能**：
* 1、网页商品链接没有使用Ajax异步请求到前台，所以在网页源代码中可以获取，则利用BeautifulSoup进行节点获取
* 2、但是正由于源代码中有而，有的地方a标签的title和a标签解释的text不一致导致抓取部分商品的名字信息时出现问题
（后续会着手解决）
``` python
link_name = selector.xpath('//div[@class="productTitle productTitle-spu"]/a[1]/@title')
data_list.append(link_name)

link = selector.xpath('//div[@class="productTitle productTitle-spu"]/a[1]/@href')
data_list.append(link)
```
