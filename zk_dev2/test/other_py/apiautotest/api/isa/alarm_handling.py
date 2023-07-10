'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/3/1 14:17
software: PyCharm
'''
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host


# 告警处置

# 告警概览

class AlarmOverview(BaseApi):
    """ 告警概览页面 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/alarm/search/list'
        self.method = 'post'
        self.json = {"route": 2, "factoryId": 2, "dateRange": 1, "actionStatus": 1, "type": 1}


class AlarmOverviewPicture(BaseApi):
    """ 告警概览图表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/system/dashboard/dashboardPanel'
        self.method = 'post'
        self.json = {"route": 2, "factoryId": 2, "dateRange": 1, "actionStatus": 1, "type": 1}


# 告警检索


class AlarmRetrieval(BaseApi):
    """ 告警检索 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/alarm/search/list'
        self.method = 'post'
        self.json = {"keyword": "", "startPage": 1, "pageSize": 10}


class AlarmRetrievalQuery(BaseApi):
    """ 告警检索条件查询 """

    def __init__(self, keyword='', actionStatus='', starttime='', endtime='', alarmType=30000100, factory=2, alarm_filter=True, alarmTypeArr=[30000000, 30000100]):
        BaseApi.__init__(self)
        self.url = host + '/alarm/search/list'
        self.method = 'post'
        self.json = {"keyword": keyword, "alarmStartTime": starttime, "actionStatus": actionStatus, "alarmEndTime": endtime,
                     "alarmType": alarmType, "factory": factory, "alarm_filter": alarm_filter, "alarmTypeArr": alarmTypeArr,
                     "startPage": 1, "pageSize": 10}


class ThreatIntelligenceDetails(BaseApi):
    """ 威胁情报详情 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/alarm/search/info'
        self.method = 'get'


class AlarmRetrievalTraceability(BaseApi):
    """ 告警检索攻击溯源 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/alarm/search/info/AttackAlarm'
        self.method = 'post'
        self.json = {"alarmUuid": "859125bd-9fe3-413c-a1e6-41d134b1a14e"}


class AlarmTraceabilityList(BaseApi):
    """ 告警检索攻击溯源告警列表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/alarm/search/info/alarmList'
        self.method = 'post'
        self.json = {"alarmId": "7eef8443-62d1-4545-af42-62f04373cd69", "alarmStage": 600, "startPage": 1,
                     "pageSize": 10}


class AlarmTraceabilityEventList(BaseApi):
    """ 告警检索攻击溯源日志列表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/alarm/search/info/eventList'
        self.method = 'post'
        self.json = {"alarmId": "7eef8443-62d1-4545-af42-62f04373cd69", "pageSize": 10, "startPage": 1}


# 威胁情报分析

class ThreatIntelligence(BaseApi):
    """ 威胁情报页面 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/threat/statistics/show'
        self.method = 'post'
        self.json = {"factoryId": 2, "actionStatus": 1, "dateRange": 1}
