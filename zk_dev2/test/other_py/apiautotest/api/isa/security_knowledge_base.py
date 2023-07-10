'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/2/25 14:25
software: PyCharm
'''
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host

# 安全知识库
from zk_dev2.test.other_py.apiautotest.setting import DIR_NAME


class VulnerabilityLibrary(BaseApi):
    """ 漏洞库 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/vulLib/getVulLibInfoByPage'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10,
                     "paramMap": "{\"vulType\":\"\",\"riskLevel\":\"\",\"ics\":\"\",\"cve\":\"\",\"cnvd\":\"\",\"cnnvd\":\"\",\"searchParam\":\"\"}"}


class SuggestionLibrary(BaseApi):
    """ 处置建议库 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/suggestions/page'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "keyword": ""}


# 威胁情报库
class SecurityAnalysisQuery(BaseApi):
    """ 安全分析查询 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/threat/threatPage'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "keyword": "27.128.201.88"}


class IntelligenceUpdatePage(BaseApi):
    """ 情报更新页 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/setting/page'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1}


class IntelligenceUpdateDetail(BaseApi):
    """ 情报更新详情 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/threat/info'
        self.method = 'post'
        self.json = {"key": "27.128.201.88"}


class IntelligenceAutoUpdate(BaseApi):
    """ 情报自动更新 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/setting/upload'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1}


class IntelligenceUpload(BaseApi):
    """ 情报内容上传 """

    def __init__(self, file='THREAT_20220230.WNT'):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/setting/uploadLocal'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1}
        self.files = {
            'file': (file, open(DIR_NAME + '/data/uploadfile/{}'.format(file), 'rb'))
        }


class IntelligenceUpdate(BaseApi):
    """ 情报内容更新 """

    def __init__(self, file='THREAT_20220230.WNT'):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/setting/uploadLocal'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1}
        self.files = {
            'file': (file, open(DIR_NAME + '/data/uploadfile/{}'.format(file), 'rb'))
        }


class IntelligenceDetail(BaseApi):
    """ 情报内容详情 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/threat/info'
        self.method = 'post'
        self.json = {"key": "83.171.237.173"}


class CommonPortLibrary(BaseApi):
    """ 常见端口库 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/port/page'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "keyword": ""}


class AddCommonPort(BaseApi):
    """ 添加常见端口 """

    def __init__(self, port='1', transportLayer='udp', serviceType='tcpmux1', highRisk=0, remark=''):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/port/add'
        self.method = 'post'
        self.json = {"port": port, "transportLayer": transportLayer, "serviceType": serviceType, "highRisk": highRisk,
                     "remark": remark}


class ModCommonPort(BaseApi):
    """ 修改常见端口 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/port/edit'
        self.method = 'post'
        self.json = {"id": 11251, "port": "2", "transportLayer": "udp", "serviceType": "abcd", "highRisk": 1,
                     "remark": "abcd"}


class DeleteCommonPort(BaseApi):
    """ 删除常见端口 """

    def __init__(self, ids):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/port/delete'
        self.method = 'delete'
        self.json = {"ids": ids}


class AddDisposalAdvice(BaseApi):
    """ 添加处置建议 """

    def __init__(self, alarmType=10000101, content='test1'):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/suggestions/add'
        self.method = 'post'
        self.json = {"alarmType": alarmType, "content": content}


class DeleteDisposalAdvice(BaseApi):
    """ 批量删除处置建议 """

    def __init__(self, ids=[39]):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/suggestions/batchDel'
        self.method = 'post'
        self.json = {"ids": ids}


class EqualProtectionKnowledgeBase(BaseApi):
    """ 等保知识库 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledgeBase/hierarchyProtection/page'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "protectionLevel": 1, "keyword": ""}


class AssetFingerprintQuickSearch(BaseApi):
    """ 资产指纹库快速查询 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledgeBase/fingerprint/fingerprinLibraryCount'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "protectionLevel": 1, "keyword": ""}


class AssetFingerprintLibrary(BaseApi):
    """ 资产指纹库 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/knowledgeBase/fingerprint/fingerprinLibrarylist'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "keyWord": "", "equipmentTypeId": ""}
