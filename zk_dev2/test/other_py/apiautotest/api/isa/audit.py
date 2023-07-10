'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/2/28 14:07
software: PyCharm
'''
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host


# audit


class OperatorLog(BaseApi):
    """ 操作日志 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/log/getLogList'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "contentlogcn": ""}
