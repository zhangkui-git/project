
from zk_dev2.test.other_py.apiautotest.common.client import RequestsClient
from zk_dev2.test.other_py.apiautotest.config.config import host
from zk_dev2.test.other_py.apiautotest.api.login_api import *


class BaseApi(RequestsClient):
    Authorization = login_test(username, password)
    def __init__(self):
        #首先调用父类初始化
        RequestsClient.__init__(self)
        self.host = host
        self.headers = {
            'Authorization': BaseApi.Authorization

        }

    def a(self):
        print(self.headers)


if __name__ == '__main__':
    BaseApi().a()