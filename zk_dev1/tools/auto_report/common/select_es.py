import requests
import sys


product = sys.argv[1]
version = sys.argv[2]
host = sys.argv[3]
select_ssh_pwd = sys.argv[4]
select_es_name = sys.argv[5]
select_es_pwd = sys.argv[6]
mem = sys.argv[8]
time1 = int(sys.argv[7])
speed = int(sys.argv[9])

# get请求方式
# 账号密码：elastic:changeme
es_host = f"http://elastic:{select_es_pwd}@{host}:9200"
# es_host = f"http://elastic:changeme@192.168.100.248:9200"

def select_es():
    url = f"{es_host}/soc_event_info_202*/_search"
    res = requests.get(url).json()
    # print(res["hits"]["total"])
    return res["hits"]["total"]


def select_es2():
    url1 = f"{es_host}/soc_event_info_202*/_search"
    url2 = f"{es_host}/soc_ptrecord_audit_log_202*/_search"
    res1 = requests.get(url1).json()
    res2 = requests.get(url2).json()
    sum12 = res1["hits"]["total"] + res2["hits"]["total"]
    # print(sum12)
    return sum12


# if __name__ == '__main__':
#     # host = input("请输入IP：")
#     # select_es_pwd = input("请输入es密码：")
#     select_es2()











