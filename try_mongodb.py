import pymongo

mongodb_client = pymongo.MongoClient('mongodb://localhost:27017/')

dblist = mongodb_client.list_database_names()
if "db_news" in dblist:
    # print("数据库已存在！")
    eval("1+1")

db_news = mongodb_client['db_news']

collection_list = db_news.list_collection_names()
if "collection_news" in collection_list:  # 判断 sites 集合是否存在
    # print("集合已存在！")
    eval("1+1")

col = db_news['news']

# col.insert_one({'_id': '0', 'news_id': 0, 'img_id': 0})
doc = col.find_one_and_update({'_id': '0'}, {'$inc': {'news_id': 1, 'img_id': 1}})
print(doc['news_id'], doc['img_id'])
