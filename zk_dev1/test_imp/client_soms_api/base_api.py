"""
基于操作接口实现token公用
"""


from zk_dev1.test_imp.common_soms_tool.common_conf import *
from client import *


class BaseApi(RequestsClient):
    Authorization = login_test(username, password)
    def __init__(self):
        # 首先调用父类初始化
        RequestsClient.__init__(self)
        self.host = host
        self.headers = {
            'Authorization': BaseApi.Authorization

        }

    def a(self):
        print(self.headers)


if __name__ == '__main__':
    BaseApi().a()