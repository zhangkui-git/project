'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/3/16 9:54
software: PyCharm
'''
from api.base_api import BaseApi
from config.config import host


#  数据分析页面


# 日志检索


class LogRetrieve(BaseApi):
    """ 日志检索 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/event/page'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "filter": [], "keyword": ""}


class SecondaryNormalize(BaseApi):
    """ 二次范化 ISA"""

    def __init__(self, rawLogStr, sourceIp, normalizeGroup=[1399]):
        BaseApi.__init__(self)
        self.url = host + '/event/secondaryNormalize'
        self.method = 'post'
        self.json = [{"protocolType": "Syslog协议",
                      "rawLogStr": rawLogStr,
                      "sourceIp": sourceIp, "esIndexName": "soc_event_info_20220409000012",
                      "_id": "AYAL3meQTdHXtYvPIQGv", "receiptdate": "2022-04-09 09:09:24", "normalizeGroup": normalizeGroup}]


class GetGroup(BaseApi):
    """ 获取分组 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/search/filter/group'
        self.method = 'get'