import time

import requests
# import pytest
# import allure
from zk_dev1.test_imp.common_soms_tool.logger import GetLogger
# from zk_dev1.test_imp.common_soms_tool.s_mysql import *
# from zk_dev1.test_imp.common_soms_tool.encry_decry import *
from zk_dev1.test_imp.client_soms_api.soms_api import *
from zk_dev1.test_imp.client_soms_api.login_api import *
write_log = GetLogger().get_logger()


class Soms_test_smoke(BaseApi):
    def __init__(self):
        BaseApi.__init__(self)
        BaseApi.Authorization = SomsLogin(username, password)

    @staticmethod
    def start():
        Soms_Login('admin_zk', 'Admin@123').send()
        Soms_AddUser().send()
        Soms_DelUser().send()


if __name__ == '__main__':
    Soms_test_smoke().start()











