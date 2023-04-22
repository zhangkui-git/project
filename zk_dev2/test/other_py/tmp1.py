
# print(str(datetime.datetime.now())[:11])

a = [1, 2, 3, 4, 5]
print(a[:])
print(a[::])
print(a[3:])
print(a[:3])
print(a[::2])

from elasticsearch import Elasticsearch

es = Elasticsearch("http://192.168.4.153:9200", http_auth=('elastic', 'changeme'), timeout=20)
data = {"factory_id":3,"create_time":"2023-04-21T12:05:01.000+08:00","alarm_type":10000000,"alarm_primary_message":"platform微服务组件异常","safe_device_ip":"192.168.4.153","effected_desc":"platform微服务组件发生异常，导致系统无法访问","warm_suggest":"platform微服务组件发生异常，请及时排查","alarm_level":2,"merge_count":1,"alarm_start_time":"2023-04-21T12:05:01.000+08:00","action_status":1}
result = es.create(index='soc_alarm_info_20230421000000',id='zhangkui_2', body=data)
print(result)





