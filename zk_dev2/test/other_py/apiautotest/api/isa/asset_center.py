'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/2/23 12:26
software: PyCharm
资产中心模块
'''

# 资产管理
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host
from zk_dev2.test.other_py.apiautotest.setting import DIR_NAME


class SelectAllList(BaseApi):
    """选择所有列"""

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/selectField/save'
        self.method = 'post'
        self.json = {
            "selectFields": ["name", "ip", "alias", "mac", "riskLevel", "riskScore", "assetBusinessValue", "typeName",
                             "vendorName", "modelName", "autoMessage", "operateSystem", "serialNumber", "hasGuard",
                             "hasVul", "updateTime", "factoryName", "port", "assetConfidentiality", "assetIntegrity",
                             "assetAvailability", "isActive", "isOnline", "cpuUsage", "memoryUsage", "hardDistUsage",
                             "flow", "belongingUnit", "belongProfessiona", "belongingSystem", "hostName",
                             "physicalPortNumber", "firstDiscoveryTime", "loginTime", "safetyResponsiblePerson",
                             "complianceScore", "riskPortCn"],
            "type": "confirmAssetList"
        }


class AssetList(BaseApi):
    """ 获取属性列表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/asset/attribute/list'
        self.method = 'post'


class ImportAssetExcel(BaseApi):
    """ 导入资产 """

    def __init__(self, file):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm/upload'
        self.method = 'post'
        self.files = {
            'file': (file, open(DIR_NAME + '/data/uploadfile/{}'.format(file), 'rb'),
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }


class GetAsset(BaseApi):
    """ 获取资产详情 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm/page'
        self.method = 'get'


class GetList(BaseApi):
    """ 获取资产详情 """

    def __init__(self, keyword=''):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm/page'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "keyword": keyword}


class GetAssetList(BaseApi):
    """ 获取资产详情 """

    def __init__(self, routeName='vulnerabilitySituation', factoryId=2):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm/page'
        self.method = 'post'
        self.json = {"routeName": routeName, "factoryId": factoryId, "startPage": 1, "pageSize": 10,
                     "keyword": ""}


class AddAsset(BaseApi):
    """ 新增资产 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm'
        self.method = 'post'
        self.json = {
            "alias": "",
            "assetAvailability": 1,
            "assetBusinessValue": "3",
            "assetConfidentiality": 1,
            "assetIntegrity": 1,
            "belongProfessiona": "test1",
            "belongingSystem": "test1",
            "belongingUnit": "test1",
            "deviceVersion": "",
            "factoryId": 3,
            "hasGuard": "",
            "hostName": "test1",
            "ip": "192.168.56.3",
            "ipMacs": [],
            "loginTime": "2022-02-01 00:00:00",
            "mac": "",
            "modelId": "",
            "name": "test1",
            "operateSystem": "",
            "physicalPortNumber": "23",
            "safetyResponsiblePerson": "test1",
            "serialNumber": "",
            "typeId": "",
            "values": [],
            "vendorId": ""
        }


class AddAssetParam(BaseApi):
    """ 新增资产 """

    def __init__(self, name, ip, factoryId=3, hostName='test1'):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm'
        self.method = 'post'
        self.json = {
            "alias": "",
            "assetAvailability": 1,
            "assetBusinessValue": "3",
            "assetConfidentiality": 1,
            "assetIntegrity": 1,
            "belongProfessiona": "test1",
            "belongingSystem": "test1",
            "belongingUnit": "test1",
            "deviceVersion": "",
            "factoryId": factoryId,
            "hasGuard": "",
            "hostName": hostName,
            "ip": ip,
            "ipMacs": [],
            "loginTime": "2022-02-01 00:00:00",
            "mac": "",
            "modelId": "",
            "name": name,
            "operateSystem": "",
            "physicalPortNumber": "23",
            "safetyResponsiblePerson": "test1",
            "serialNumber": "",
            "typeId": "",
            "values": [],
            "vendorId": ""
        }


class ModAsset(BaseApi):
    """ 修改资产 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm'
        self.method = 'put'


class AssetFilter(BaseApi):
    """ 资产筛选 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm/page'
        self.method = 'post'


class DeleteAsset(BaseApi):
    """ 删除资产 """

    def __init__(self, id=[id]):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm'
        self.method = 'delete'
        self.json = {"ids": id}


class ImportAsset(BaseApi):
    """ 导入资产 """

    def __init__(self, file='漏洞导入test.xml'):
        BaseApi.__init__(self)
        self.url = host + '/assets/vuls/upload'
        self.method = 'post'
        self.data = {
            'factoryId': 3
        }
        self.files = {
            'file': (file, open(DIR_NAME + '/data/uploadfile/{}'.format(file), 'rb'), 'text/xml')
        }






class AssetPortrait(BaseApi):
    """ 资产画像 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/situations/base'
        self.method = 'get'


class AssetPortraitVuls(BaseApi):
    """ 资产画像漏洞 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/vuls/page'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 5, "assetId": 176}


class AssetPortraitLifeCycle(BaseApi):
    """ 资产画像生命周期 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/life/assetPortrait'
        self.method = 'post'
        self.json = {
            "assetId": 3, "factoryId": 3
        }


class RecognizedAssetsList(BaseApi):
    """已确认资产列表"""

    def __init__(self, keyword=''):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm/page'
        self.method = 'post'
        self.json = {
            "startPage": 1,
            "pageSize": 10,
            "keyword": keyword
        }


# 属性管理


class AttributesList(BaseApi):
    """属性列表页"""

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/asset/attribute/list'
        self.method = 'post'


class AddAttributes(BaseApi):
    """新增属性"""

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/asset/attribute/add'
        self.method = 'post'
        self.json = {
            "name": "test字符串",
            "type": 1
        }


class ModAttributes(BaseApi):
    """修改属性"""

    def __init__(self, id, name='test1', type=1):
        BaseApi.__init__(self)
        self.url = host + '/asset/attribute/update'
        self.method = 'post'
        self.json = {"id": id, "name": name, "type": type}


class BatchDeleteAttributes(BaseApi):
    """批量删除属性"""

    def __init__(self, id=[1]):
        BaseApi.__init__(self)
        self.url = host + '/asset/attribute/batchDelete'
        self.method = 'post'
        self.json = {
            "ids": id
        }


# 资产生命周期

class AssetLifeCycle(BaseApi):
    """ 资产生命周期页 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/life/list'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "keyword": ""}


# 风险评分

class RiskScore(BaseApi):
    """ 风险评分配置 """

    def __init__(self, vul=8, threat=1, compliant=1):
        BaseApi.__init__(self)
        self.url = host + '/assets/risk/weight'
        self.method = 'put'
        self.json = {"vul": vul, "threat": threat, "compliant": compliant}


class RiskScoreReset(BaseApi):
    """ 风险评分恢复默认 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/risk/weight/recover'
        self.method = 'put'


# 拓扑管理

# 逻辑拓扑

class LogicTopoUsual(BaseApi):
    """ 逻辑拓扑无编辑 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/logicTopo/list'
        self.method = 'post'


class LogicTopo(BaseApi):
    """ 逻辑拓扑 """

    def __init__(self, pageSize=10, factoryId=2, ip='', status=''):
        BaseApi.__init__(self)
        self.url = host + '/logicTopo/list'
        self.method = 'post'
        self.json = {"pageSize": pageSize, "startPage": 1, "ip": ip, "factoryId": factoryId, "status": status}


class LogicTopoEcxept(BaseApi):
    """ 异常逻辑拓扑 """

    def __init__(self, pageSize=10, factoryId=2, ip='', status='', exceptOk=True):
        BaseApi.__init__(self)
        self.url = host + '/logicTopo/list'
        self.method = 'post'
        self.json = {"pageSize": pageSize, "startPage": 1, "ip": ip, "factoryId": factoryId, "status": status,
                     'exceptOk': exceptOk}


class AddToBaseline(BaseApi):
    """ 加入基线 """

    def __init__(self, srcIp="192.168.4.173", srcFactoryId=-1, dstIp="192.168.100.71", dstFactoryId=3, linkId=25):
        BaseApi.__init__(self)
        self.url = host + '/logicTopo/addNetworkBaseLine'
        self.method = 'post'
        self.json = [
            {"srcIp": srcIp, "srcFactoryId": srcFactoryId, "dstIp": dstIp, "dstFactoryId": dstFactoryId,
             "linkId": linkId}]


# 漏洞管理

class ScanTestConnection(BaseApi):
    """ 扫描配置测试连接 """

    def __init__(self, user='admin', pwd='Admin@123', ip='192.168.14.20'):
        BaseApi.__init__(self)
        self.url = host + '/assets/vulnerability/testConnect'
        self.method = 'post'
        self.json = {
            "user": user,
            "pwd": pwd,
            "ip": ip
        }


class ScanTestConfirm(BaseApi):
    """ 扫描配置确定 """

    def __init__(self, user='admin', pwd='Admin@123', ip='192.168.14.20'):
        BaseApi.__init__(self)
        self.url = host + '/assets/vulnerability/scanConfig'
        self.method = 'post'
        self.json = {
            "user": user,
            "pwd": pwd,
            "ip": ip
        }


class VulnerabilityRecord(BaseApi):
    """ 漏洞记录页 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/vuls/page'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "keyword": "", "vulName": "", "onlySelf": 'false'}


class VulnerabilityDistributionPage(BaseApi):
    """ 漏洞分布页 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/assets/vuls/vulDistribution'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "searchKey": ""}
