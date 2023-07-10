'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/3/7 11:36
software: PyCharm
'''
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host


# 系统设置

class AuthorizationManagement(BaseApi):
    """ 授权管理 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/license'
        self.method = 'get'


class DashboardPage(BaseApi):
    """ 仪表盘页 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/system/dashboard/dashboardlist'
        self.method = 'post'
        self.json = {"dashboardName": "", "pageSize": 10, "startPage": 1}


class AddDashboard(BaseApi):
    """ 新增仪表盘 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/system/dashboard/dashboardadd'
        self.method = 'post'


class ShowDashboard(BaseApi):
    """ 查看仪表盘 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/system/dashboard/dashboardshow'
        self.method = 'post'
        self.json = {"route": 0, "factoryId": 2, "dateRange": 1, "actionStatus": 1, "type": 2, "dashboard_id": 44}


class DeleteDashboard(BaseApi):
    """ 删除仪表盘 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/system/dashboard/dashboarddelete'
        self.method = 'post'
        self.json = {"id": 42}
