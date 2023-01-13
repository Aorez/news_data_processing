import pymongo
import os
from gridfs import *

mongodb_client = pymongo.MongoClient('mongodb://localhost:27017/')

dblist = mongodb_client.list_database_names()
if "db_news" in dblist:
    # print("数据库已存在！")
    eval("1+1")

db_news = mongodb_client['db_news']

collection_list = db_news.list_collection_names()
if "try_gridfs" in collection_list:  # 判断 sites 集合是否存在
    # print("集合已存在！")
    eval("1+1")

col = db_news['try_gridfs']
col_name = 'try_gridfs'

filename = os.path.abspath('坐标轴类.png')

file = open(filename, 'rb')
filename = '坐标轴类'
filetype = 'png'

fs = GridFS(db_news)
a = fs.put(file, content_type=filetype, filename=filename, id='0')
dic = {'id': '0'}
dic2 = {'id': '1'}
b = fs.find_one(dic)
c = fs.find_one(a)
d = fs.find_one(dic2)
print(b)
print(c)
print(d)

file.close()
