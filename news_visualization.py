import pymongo
import matplotlib.pyplot as plt
import datetime

# 连接MongoDB数据库
mongodb_client = pymongo.MongoClient('mongodb://localhost:27017/')
dblist = mongodb_client.list_database_names()
if "db_news" in dblist:
    # print("数据库已存在！")
    eval("1+1")
db_news = mongodb_client['db_news']
collection_list = db_news.list_collection_names()
if "collection_news" in collection_list:
    # print("集合已存在！")
    eval("1+1")
collection_news = db_news['collection_news']

# 获得所有省份名字
province_string = "北京,天津,上海,重庆,河北,河南,云南,辽宁,黑龙江,湖南,安徽,山东,新疆,江苏,浙江,江西,湖北,广西,甘肃,山西,内蒙,陕西,吉林,福建,贵州,广东,青海,西藏,四川,宁夏,海南,台湾," \
                  "香港,澳门"
province_names = province_string.split(sep=",")
# 省份出现的次数
# 初始化为0
province_count_dict = {key: 0 for key in province_names}

# 新闻来源的次数统计
news_source_count_dict = {}

# 定义最大日期和最小日期
min_date = datetime.date(2050, 1, 1)
max_date = datetime.date(1970, 1, 1)

# 获得所有新闻
news_dicts = collection_news.find()
for news_dict in news_dicts:

    # 获得新闻来源
    news_source = news_dict['source']
    # 如果新闻来源在字典中已存在，则加一，否则赋初值为1
    if news_source in news_source_count_dict:
        news_source_count_dict[news_source] += 1
    else:
        news_source_count_dict[news_source] = 1

    # 获得新闻日期
    news_date = news_dict['date']
    # 转为日期对象
    news_date = datetime.datetime.strptime(news_date, '%Y-%m-%d').date()
    # 如果日期比最大日期大，则替换，最小日期同理
    date_differ = news_date - max_date
    if date_differ.days > 0:
        max_date = news_date
    date_differ = news_date - min_date
    if date_differ.days < 0:
        min_date = news_date

    # 遍历新闻内容
    for news in news_dict.values():
        # 遍历所有省份名字，在新闻中出现则加一
        for province in province_names:
            province_count_dict[province] += str(news).count(province)

print(max_date)
print(min_date)

# 排序
news_source_count = sorted(news_source_count_dict.items(), key=lambda x: x[1])
province_count = sorted(province_count_dict.items(), key=lambda x: x[1])
news_source_count = list(zip(*news_source_count))
province_count = list(zip(*province_count))
print(province_count)
print(news_source_count)

# 键用来设置柱状图的横坐标，值用来设置柱状图每一个横坐标的高度
keys1 = news_source_count[0]
values1 = news_source_count[1]
keys2 = province_count[0]
values2 = province_count[1]

# 画布，大小
plt.figure(figsize=(15, 9))
plt.subplots_adjust(wspace=0.5, hspace=0.3)
# 设置了才显示中文
plt.rcParams['font.family'] = 'simhei'
# 默认显示字符
plt.rcParams['axes.unicode_minus'] = False

# 新闻来源统计

plt.subplot(121)
plt.title('新闻来源统计', fontdict={'size': 13})
# 横向柱状图，y有几个项，width每个项的长度，height每个项有多厚，label图例的文本
plt.barh(y=range(len(values1)), width=values1, height=0.8, label='新闻来源')
# 为每一个柱的顶部设置数值
for x, y in enumerate(values1):
    # 横坐标，纵坐标
    plt.text(y + 0.2, x - 0.2, y, ha='center', va='bottom')

# 显示图例，loc图例位置，best自动选取合适的位置
# plt.legend(loc='upper left', bbox_to_anchor=[1, 0, 0.5, 1], fontsize=7)
plt.legend(loc='best', fontsize=10)
plt.yticks(range(len(keys1)), keys1)

# 省份出现次数统计

plt.subplot(122)
plt.title('省份出现次数统计', fontdict={'size': 13})
plt.barh(y=range(len(values2)), width=values2, height=0.8, label='省份')
for x, y in enumerate(values2):
    plt.text(y + 1.0, x - 0.4, y, ha='center', va='bottom')

plt.legend(loc='best', fontsize=10)
plt.yticks(range(len(keys2)), keys2)

plt.show()
