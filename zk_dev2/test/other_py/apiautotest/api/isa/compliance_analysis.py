'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/4/19 12:02
software: PyCharm
'''
from api.base_api import BaseApi
from config.config import host


class ComplianceTaskAdd(BaseApi):
    """ 合规评估新增 """

    def __init__(self, checkTime='', complianceName="T1", factoryId=3, isCycle=0):
        BaseApi.__init__(self)
        self.url = host + '/compliance/task/addComplianceTask'
        self.method = 'post'
        self.json = {"checkTime": checkTime, "complianceName": complianceName, "factoryId": factoryId,
                     "isCycle": isCycle}


class ComplianceTaskList(BaseApi):
    """ 查看合规评估列表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/compliance/task/getPageList'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10}


class ComplianceTaskUpdate(BaseApi):
    """ 合规评估结果更新 """

    def __init__(self, assetId=0, id=55, itemCode="1t202", factoryId=3, checkIds="28", flag=3, taskId=3,
                 tabName="安全通信网络", thirdCode="t202g1101101", fourthCode='', result=0):
        BaseApi.__init__(self)
        self.url = host + '/compliance/assest/updateComplianceResult'
        self.method = 'post'
        self.json = {"factoryId": factoryId, "assetId": assetId, "thirdCode": thirdCode, "fourthCode": fourthCode,
                     "result": result,
                     "itemCode": itemCode, "id": id, "checkIds": checkIds, "flag": flag, "taskId": taskId,
                     "tabName": tabName}


class ComplianceTaskDelete(BaseApi):
    """ 合规评估删除 """

    def __init__(self, id=[3]):
        BaseApi.__init__(self)
        self.url = host + '/compliance/task/delComplianceTask'
        self.method = 'delete'
        self.json = {"ids": id}
