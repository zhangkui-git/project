import time

from elasticsearch7 import Elasticsearch
from elasticsearch7 import helpers
import datetime

start = datetime.datetime.now()
#  host_list = [
#     {"host":"10.58.7.190","port":9200},
#     {"host":"10.58.55.191","port":9200},
#     {"host":"10.58.55.192","port":9200},
# ]

host_list = [
    {"host": "192.168.15.8", "port": 9200},
]
# 创建连接
client1 = Elasticsearch(host_list)
print("------------------ES创建连接成功")


def batch_data():
    """ 批量写入数据 """
    action = [{
        "_index": "portal_log",
        # es6版本以上type默认是_doc
        # "_type": "_doc",
        "_source": {
            "name": "zhangkui" + str(i),
            "age": 28,
            "high": 172
        }
    # } for i in range(10000000)]
    } for i in range(21000010, 21000020)]
    helpers.bulk(client1, action)


if __name__ == '__main__':
    batch_data()
    print("---------------写入完成---------------")

    time.sleep(60)
    import requests
    url = 'http://192.168.15.8:9200/_cat/indices/portal_log?v'
    res = requests.get(url).text
    print("---------------总数据量如下---------------\n", res)
    stop = datetime.datetime.now()
    jump = datetime.timedelta(seconds=60)
    print("------------------------------消耗时间：",   stop - start - jump)

