import time
import requests
import pymongo
from lxml import etree
from gridfs import *


# 连接MongoDB数据库
mongodb_client = pymongo.MongoClient('mongodb://localhost:27017/')
dblist = mongodb_client.list_database_names()
if "db_news" in dblist:
    # print("数据库已存在！")
    eval("1+1")
db_news = mongodb_client['db_news']
collection_list = db_news.list_collection_names()
if "news" in collection_list:  # 判断 sites 集合是否存在
    # print("集合已存在！")
    eval("1+1")
col = db_news['news']
# col.delete_many({})

# 设置id
if col.find_one({'_id': '0'}) is None:
    col.insert_one({'_id': '0', 'news_id': 0, 'img_id': 0})

# 待爬网址
base_url = "https://news.china.com/"
# 反反爬
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 "
                  "Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

# 爬取信息
resp = requests.get(url=base_url, headers=headers)
# 设置编码
resp.encoding = "utf-8"
# 把信息通过etree进行赋值
html = etree.HTML(resp.text)

# 要爬取的div的路径
div_wp_left = "/html/body/div[4]/div[1]"

# 分类的标题，[要闻，国内，国际……]
li_list = html.xpath(div_wp_left + '/ul/li')
# 遍历获取分类
classifications = []
for li in li_list:
    # 获取分类的文本，“要闻”
    classification = li.xpath('./a/text()')[0]
    classifications.append(classification)
    time.sleep(1)
print('所有分类：', classifications)

# 所有新闻
ul_list = html.xpath(div_wp_left + '/div/ul')
# 各个分类对应的新闻
for index, ul_item_list in enumerate(ul_list):
    # 当前分类是按顺序的
    classification = classifications[index]
    # 遍历当前分类中的新闻
    for li in ul_item_list:
        # 标题
        title = li.xpath('./h3/a/text()')[0]
        # 新闻链接
        link = li.xpath('./h3/a/@href')[0]
        # 来源
        source = li.xpath('./span/em[1]/text()')[0]
        # 日期
        date = li.xpath('./span/em[2]/text()')[0]

        # 获取id
        doc_id = col.find_one_and_update({'_id': '0'}, {'$inc': {'news_id': 1, 'img_id': 1}})
        news_id = doc_id['news_id']
        img_id = doc_id['img_id']

        # 网页图片保存到本地，再转存到数据库
        filetemp = 'baidu.png'
        # 新闻缩略图
        image_src = li.xpath('./a/img/@data-original')[0]
        print('image_src: ', image_src)
        # 获取网络图片资源
        r = requests.get(image_src, headers=headers)
        # 创建文件保存图片
        with open(filetemp, 'wb') as f:
            # 将图片字节码写入创建的文件中
            f.write(r.content)
        with open(filetemp, 'rb') as f:
            # 文件类型
            filetype = 'png'
            # 打开gridfs存储桶
            fs = GridFS(db_news)
            # 将图片存储到gridfs存储桶中，并设置自定义元数据id
            fs.put(f, content_type=filetype, id=img_id)

        doc = col.insert_one({'id': news_id, 'classification': classification, 'title': title, 'link': link, 'source': source, 'date': date, 'img_id': img_id})
        print(doc)
        time.sleep(1)
