import threading
from zk_dev2.test.many_login.login import *
import time
from add_assert import *


data_list = many_token()


class SelectNum(object):
    suc_num = 0
    fail_num = 0

    def __init__(self, token):
        self.token = token

    def select_1(self, name):
        create_file_url = "https://192.168.100.159:8440/event/page"
        create_file_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{self.token}'}
        create_file_body = {"startPage":1,"pageSize":20,"filter":[],"keyword":"192.168.0.60"}
        create_file_res = requests.post(url=create_file_url, headers=create_file_headers, json=create_file_body, verify=False)
        if create_file_res.json()["total"] == 0:
            SelectNum.suc_num += 1
        else:
            SelectNum.fail_num += 1
        print("成功：", SelectNum.suc_num, "失败：", SelectNum.fail_num)


def many_threads():
    threads = []
    # for x, name in enumerate(data_list):
    for x in range(10):
        # threads.append(threading.Thread(target=SelectNum(name).select_1, args=(x,)))
        threads.append(threading.Thread(target=add_many_assert, args=(x,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    while True:
        many_threads()
        # time.sleep(0.05)







