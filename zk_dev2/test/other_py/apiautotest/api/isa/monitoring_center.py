'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/2/28 10:19
software: PyCharm
'''
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host


# 监控中心

# 大屏管理

class SecurityPostureSecurityNotice(BaseApi):
    """ 综合安全态势安全通告 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/asset/safetynotice/screenList'
        self.method = 'post'



class ThreatTransverse(BaseApi):
    """ 横向威胁态势四个按钮 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/screen/threat/transverse'
        self.method = 'get'
        self.params = {
            "factoryId": 2
        }


class OperationalSituation(BaseApi):
    """ 运行态势五个按钮 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/screen/run/asset/status/count'
        self.method = 'post'
        self.json = {
            "factoryId": 2
        }


class OperationalSituationQuickSearh(BaseApi):
    """ 运行态势6个快速查询 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/screen/run/asset/quickselect'
        self.method = 'post'
        self.json = {"factoryId": 2, "isOnline": ""}


class QuickSearhPage(BaseApi):
    """ 快速查询页 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/screen/run/asset/page'
        self.method = 'post'
        self.json = {"factoryId": 2, "startPage": 1, "pageSize": 50, "isOnline": "", "assetTypeCn": ""}


# 横向威胁态势

class HorizontalThreatPosturePage(BaseApi):
    """ 横向威胁态势页 """

    def __init__(self, factoryId=2):
        BaseApi.__init__(self)
        self.url = host + '/screen/threat/transverse'
        self.method = 'get'
        self.params = {'factoryId': factoryId}


class SafetyNotice(BaseApi):
    """ 安全通告 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/asset/safetynotice/page'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "keyword": ""}


class AddSafetyNotice(BaseApi):
    """ 新增安全通告 """

    def __init__(self, title="test", description='test', cveCode='CVE-2016-3236', operatingSystem='Windows', enable=0):
        BaseApi.__init__(self)
        self.url = host + '/asset/safetynotice/add'
        self.method = 'post'
        self.json = {"title": title, "description": description, "cveCode": cveCode, "operatingSystem": operatingSystem,
                     "enable": enable}


class ModSafetyNotice(BaseApi):
    """ 修改安全通告 """

    def __init__(self, id, title="test", description='test', cveCode='CVE-2016-3236', operatingSystem='Windows', enable=0):
        BaseApi.__init__(self)
        self.url = host + '/asset/safetynotice/update'
        self.method = 'post'
        self.json = {"title": title, "description": description, "cveCode": cveCode, "operatingSystem": operatingSystem,
                     "enable": enable, 'id': id}


class DeleteSafetyNotice(BaseApi):
    """ 删除安全通告 """

    def __init__(self, ids=[1]):
        BaseApi.__init__(self)
        self.url = host + '/asset/safetynotice/batchDel'
        self.method = 'post'
        self.json = {"ids": ids}


class RunMonitoringPage(BaseApi):
    """ 运行监视页面 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/sysmonitor/all'
        self.method = 'get'


class RealTimeCpu(BaseApi):
    """ 实时cpu """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/sysmonitor/realTimeCpu?clientId=3C:EC:EF:20:2F:72'
        self.method = 'get'


class HistoryTimeCpu(BaseApi):
    """ 历史cpu """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/sysmonitor/historyTimeCpu?clientId=3C:EC:EF:20:2F:72'
        self.method = 'get'
