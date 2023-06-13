"""
基于操作接口实现token公用
"""

from zk_dev1.test_imp.client_soms_api.login_api import *
# from fake_useragent import UserAgent
# ua = UserAgent().chrome


class BaseApi(RequestsClient):
    Authorization = SomsLogin(username, password)
    def __init__(self):
        # 首先调用父类初始化
        RequestsClient.__init__(self)
        self.host = host
        self.headers = {
            'Authorization': BaseApi.Authorization,
        }

    def a(self):
        print(self.headers)


if __name__ == '__main__':
    BaseApi().a()




