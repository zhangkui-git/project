'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/3/2 9:28
software: PyCharm
'''
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host


# 报表管理


# 即时报表


class ReportManageChapter(BaseApi):
    """ 统计分类详情 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/reportManage/chapter'
        self.method = 'get'


class InstantReportList(BaseApi):
    """ 即时报表列表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/reportManage/list'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "keyword": "", "statsType": 0}


class AddInstantReport(BaseApi):
    """ 新增即时报表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/reportManage/add'
        self.method = 'post'
        self.json = {"statsType": 0, "reportName": "test", "reportType": 1, "factoryId": 3, "isEmail": 0,
                     "receiveId": "", "reportDesc": "", "fileType": 0,
                     "statsContent": "100,100-01,100-02,100-03,100-04,100-05,100-06,110,110-01,110-02,110-03,110-04,110-05,110-06,90,90-01,90-02,90-03,90-04,90-05,90-06,130,130-01,130-02,130-03,130-04,120,120-01,120-02",
                     "year": "2022", "month": "3"}


class DeleteInstantReport(BaseApi):
    """ 删除即时报表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/reportManage/delete'
        self.method = 'delete'
        self.json = [1]
