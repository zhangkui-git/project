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
    {"host": "192.168.4.153", "port": 9200},
]
# 创建连接
client1 = Elasticsearch(hosts=host_list, http_auth=('elastic', 'changeme'), timeout=20)
print("------------------ES创建连接成功")


def batch_data():
    """ 批量写入数据 """
    action = [{
        "_index": "soc_alarm_info_20230423171211",
        "_type": "base",
        "_id": f"zhangkui_{i}",
        "_score": 1,
        # es6版本以上type默认是_doc
        # "_type": "_doc",
        "_source": {"factory_id":3,"create_time":"2023-04-21T12:05:01.000+08:00","alarm_type":10000000,"alarm_primary_message":"test_alarm","safe_device_ip":"192.168.4.153","effected_desc":"test_alarm","warm_suggest":"test_alarm","alarm_level":2,"merge_count":1,"alarm_start_time":"2023-04-21T12:05:01.000+08:00","action_status":1}
    } for i in range(9999980, 9999988)]
    helpers.bulk(client1, action)


if __name__ == '__main__':
    batch_data()
    print("---------------写入完成---------------")

    time.sleep(60)
    import requests
    url = 'http://elastic:changeme@192.168.4.153:9200/_cat/indices/soc_alarm_info_20230423171211?v'
    res = requests.get(url).text
    print("---------------总数据量如下---------------\n", res)
    stop = datetime.datetime.now()
    jump = datetime.timedelta(seconds=60)
    print("------------------------------消耗时间：",   stop - start - jump)

