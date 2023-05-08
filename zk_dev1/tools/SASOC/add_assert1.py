import time
import requests
from login import *

token = many_token()


def add_assert(token):
    add_assert_url = "https://192.168.4.107:8440/event/page"
    add_assert_header = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    add_assert_body = {"startPage": 1, "pageSize": 10, "filter": [], "keyword": ""}
    res = requests.post(url=add_assert_url, headers=add_assert_header, json=add_assert_body, verify=False)
    add_assert_result = res.text
    print("操作结果：", add_assert_result)


if __name__ == '__main__':
    add_assert(token[0])
