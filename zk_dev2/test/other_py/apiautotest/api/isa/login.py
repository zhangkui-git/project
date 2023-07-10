'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/3/7 16:05
software: PyCharm
'''
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host


class VulnerabilityConfiguration(BaseApi):
    """ 漏洞匹配开关 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/vuls/match'
        self.method = 'put'
        self.json = {"match": 1}
