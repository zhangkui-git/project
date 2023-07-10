'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/2/24 15:33
software: PyCharm
'''
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host, local_ip
from zk_dev2.test.other_py.apiautotest.setting import DIR_NAME


# 策略配置
class AddAera(BaseApi):
    """ 新增区域 """

    def __init__(self, name='test', factoryAddress='', factoryIpScope=''):
        BaseApi.__init__(self)
        self.url = host + '/factory/add'
        self.method = 'post'
        self.json = {"factoryName": name, "factoryAddress": factoryAddress, "factoryIpScope": factoryIpScope,
                     "factoryRegion": ["110000", "110100", "110101"], "longitude": "116.41005", "latitude": "39.93157",
                     "description": "", "level": 1, "parentId": 2, "regionMap": "110000", "userConfirmed": 'false'}


class AeraQuery(BaseApi):
    """ 查看区域管理列表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/kvenum/factoryTree'
        self.method = 'get'


class ModAera(BaseApi):
    """ 修改区域 """

    def __init__(self, value, factoryIpScope="192.168.4.10-192.168.4.200"):
        BaseApi.__init__(self)
        self.url = host + '/factory/edit/' + str(value)
        self.method = 'put'
        self.json = {"factoryName": "XX区域", "factoryAddress": "", "factoryIpScope": factoryIpScope,
                     "factoryRegion": ["110000", "110100", "110108"], "longitude": 116.29812, "latitude": 39.95931,
                     "description": "", "homePageChat": 1, "regionMap": "110000", "userConfirmed": "false"}


class DeleteAera(BaseApi):
    """ 删除区域 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/factory/delete'
        self.method = 'delete'
        self.json = {"ids": [4]}


class LogSourceImport(BaseApi):
    """ 日志源导入 """

    def __init__(self, file):
        BaseApi.__init__(self)
        self.url = host + '/log/source/uploadLogSource'
        self.method = 'post'
        self.files = {
            'file': (file, open(DIR_NAME + '/data/uploadfile/{}'.format(file), 'rb'),
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }


class AutoFindLogSource(BaseApi):
    """ 自发现日志源开关 """

    def __init__(self, flag='false'):
        BaseApi.__init__(self)
        self.url = host + '/log/source/automaticFindLogSource'
        self.method = 'post'
        self.params = {
            'flag': flag
        }


class LogSourcePage(BaseApi):
    """ 查看日志源列表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/log/source/list'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10}


class AddLogSource(BaseApi):
    """ 新增日志源 """

    def __init__(self, name=local_ip, ip=local_ip, factory=3, protocolType=1, community='', assetType=101001,
                 normalizeGroup=[1386], isEncryption=0, ftpMode=1):
        BaseApi.__init__(self)
        self.url = host + '/log/source/add'
        self.method = 'post'
        self.json = {"logSourceName": name, "assetIp": ip, "factory": factory, "assetType": assetType,
                     "port": '', "protocolType": protocolType, "snmpVersion": 1, "normalizeGroup": normalizeGroup,
                     "community": community,
                     "isAnonymousLogin": 0, "userName": "", "password": "", "filePath": "", "originalEncoding": "UTF-8",
                     "downloadRate": 1000, "taskInterval": 300, "ftpMode": ftpMode, "dbType": "MySQL", "dbName": "",
                     "customerSqlStatus": 0, "dbTableName": "", "selectSql": "", "isEncryption": isEncryption,
                     "algorithm": 1,
                     "privateKey": ""}


class ModLogSource(BaseApi):
    """ 修改日志源 """

    def __init__(self, name="192.168.4.174", ip="192.168.4.174", factory=3, protocolType=1, community='',
                 assetType=101001, normalizeGroup=['1386'], ftpMode='',
                 isEncryption=0, id="622c66b7561ee66ca874cad4"):
        BaseApi.__init__(self)
        self.url = host + '/log/source/update'
        self.method = 'put'
        self.json = {"logSourceName": name, "assetIp": ip, "factory": factory, "assetType": assetType,
                     "port": '', "protocolType": protocolType, "snmpVersion": '', "normalizeGroup": normalizeGroup,
                     "community": community, "isAnonymousLogin": 0, "userName": '', "password": '', "filePath": '',
                     "originalEncoding": '', "downloadRate": '', "taskInterval": '', "ftpMode": ftpMode, "dbType": '',
                     "dbName": '', "customerSqlStatus": 0, "dbTableName": '', "selectSql": '',
                     "isEncryption": isEncryption,
                     "algorithm": 1, "privateKey": "", "id": id}


class DeleteLogSource(BaseApi):
    """ 删除日志源 """

    def __init__(self, ids):
        BaseApi.__init__(self)
        self.url = host + '/log/source/delete/batch'
        self.method = 'delete'
        # self.json = {"ids": ["6245a3a4561ee616598fd7b0"]}
        self.json = {"ids": ids}


class LogSourceFilter(BaseApi):
    """ 日志源过滤 """

    def __init__(self, id, srcIp='', destIp='', eventCategory='', eventLevel='', keyWord=''):
        BaseApi.__init__(self)
        self.url = host + '/logFilterConfig/update'
        self.method = 'put'
        self.json = {"id": id, "srcIp": srcIp, "destIp": destIp, "eventCategory": eventCategory,
                     "eventLevel": eventLevel,
                     "keyWord": keyWord}


# 日志范化


class FieldGroupShow(BaseApi):
    """ 查看字段分组 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/normalize/fieldGroup/list'
        self.method = 'get'


class GroupFieldShow(BaseApi):
    """ 查看分组下字段 """

    def __init__(self, fieldGroupId='1', fieldName=''):
        BaseApi.__init__(self)
        self.url = host + '/normalize/field/list'
        self.method = 'post'
        self.json = {"fieldGroupId": fieldGroupId, "fieldName": fieldName, "page": {"startPage": 1, "pageSize": 10}}


class FieldGroupAdd(BaseApi):
    """ 新增字段组 """

    # def __init__(self, groupId='', groupName='test_group', groupDescription='', parentId=1, parentPath='/1'):
    def __init__(self, name='test_group', id='', mark=''):
        BaseApi.__init__(self)
        self.url = host + '/normalize/fieldGroup/add'
        self.method = 'post'
        self.json = {"id": id, "name": name, "mark": mark}
        # self.json = {"groupId": groupId, "groupName": groupName, "groupDescription": groupDescription,
        #              "parentId": parentId,
        #              "parentPath": parentPath}


class FieldGroupMod(BaseApi):
    """ 修改字段组 """

    # def __init__(self, groupId=21418, groupName='test_group', groupDescription='', parentId=1, parentPath='/1/21418'):
    def __init__(self, id="1001", name='test_group1', mark=''):
        BaseApi.__init__(self)
        self.url = host + '/normalize/fieldGroup/update/'
        self.method = 'put'
        self.json = {"id": id, "name": name, "mark": mark}
        # self.json = {"groupId": groupId, "groupName": groupName, "groupDescription": groupDescription,
        #              "parentId": parentId,
        #              "parentPath": parentPath}


class FieldGroupDelete(BaseApi):
    """ 删除字段组 """

    def __init__(self, id='1', name='日志公共字段'):
        BaseApi.__init__(self)
        self.url = host + '/normalize/fieldGroup/delete'
        self.method = 'delete'
        self.json = {"id": id, "name": name}


class FieldAdd(BaseApi):
    """ 字段新增 """

    def __init__(self, fieldName='test', fieldAlias='testtest', fieldGroup='1'):
        BaseApi.__init__(self)
        self.url = host + '/normalize/field/add'
        self.method = 'post'
        self.json = {"fieldName": fieldName, "fieldAlias": fieldAlias, "fieldGroup": fieldGroup, "fieldDescription": "",
                     "fieldType": "1",
                     "fieldLength": 1, "fkNormalizeDictId": "", "containType": ""}


class FieldDelete(BaseApi):
    """ 字段删除 """

    def __init__(self, id=["62538ca8561ee6421e547f15"]):
        BaseApi.__init__(self)
        self.url = host + '/normalize/field/delete/batch'
        self.method = 'delete'
        self.json = {"ids": id}


class SnmpOidAdd(BaseApi):
    """ SNMP OID新增 """

    def __init__(self, oid=".12.2", name='test', description='', fkNormalizeFieldId='5df74db19b479292ee57e63f',
                 fkNormalizeFieldAlias="HTTP状态码", isCustom=1):
        BaseApi.__init__(self)
        self.url = host + '/normalize/snmpoid/add'
        self.method = 'post'
        self.json = {"id": "", "oid": oid, "name": name, "description": description,
                     "fkNormalizeFieldId": fkNormalizeFieldId, "fkNormalizeFieldAlias": fkNormalizeFieldAlias,
                     "isCustom": isCustom}


class SnmpOidDelete(BaseApi):
    """ SNMP OID删除 """

    def __init__(self, ids):
        BaseApi.__init__(self)
        self.url = host + '/normalize/snmpoid/delete'
        self.method = 'delete'
        self.json = {"ids": ids}


class SnmpOidQuery(BaseApi):
    """ SNMP OID查询 """

    def __init__(self, keywordContent=".1.2.3.4"):
        BaseApi.__init__(self)
        self.url = host + '/normalize/snmpoid/list'
        self.method = 'post'
        self.json = {"page": {"startPage": 1, "pageSize": 10}, "keywordContent": keywordContent}


class SnmpOidCheck(BaseApi):
    """ SNMP OID查看 """

    def __init__(self, id):
        BaseApi.__init__(self)
        self.url = host + '/normalize/snmpoid/list'
        self.method = 'post'
        self.json = {"id": id}


# 关联分析

class CorrelationAnalysisPage(BaseApi):
    """ 查看管理分析页 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/associateAnalyze/rule'
        self.method = 'post'
        self.json = {"gid": "", "name": "", "startPage": 1, "pageSize": 10}


class ImportCorrelationAnalysis(BaseApi):
    """ 上传关联分析 """

    def __init__(self, file='uploadfile\\关联分析20220303192735.xlsx'):
        BaseApi.__init__(self)
        self.url = host + '/associateAnalyze/rule/upload'
        self.method = 'post'
        self.files = {
            'file': (file, open(DIR_NAME + '\\data\\{}'.format(file), 'rb'),
                     'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }


class DeleteCorrelationAnalysis(BaseApi):
    """ 删除关联分析 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/associateAnalyze/rule/del'
        self.method = 'post'
        self.json = {"ids": [193]}


# 基线配置


class AddNetworkBaseline(BaseApi):
    """添加网络基线"""

    def __init__(self, name='test', fromTime='2022-05-05 16:55:24', toTime='2022-05-12 00:00:00'):
        BaseApi.__init__(self)
        self.url = host + '/networkBaseLine/add'
        self.method = 'post'
        self.json = {"name": name, "fromTime": fromTime, "toTime": toTime}


class NetworkBaseline(BaseApi):
    """ 开启网络基线 """

    def __init__(self, id="default_base_line_id", status=1):
        BaseApi.__init__(self)
        self.url = host + '/networkBaseLine/status'
        self.method = 'post'
        self.json = {"id": id, "status": status}


class BaselineDetailsList(BaseApi):
    """ 网络基线明细列表 """

    def __init__(self, baseId="default_base_line_id", assetName='', ip=''):
        BaseApi.__init__(self)
        self.url = host + '/networkBaseLine/item/list'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "assetName": assetName, "ip": ip, "baseId": baseId}


class BaselineDetails(BaseApi):
    """ 添加网络基线明细 """

    def __init__(self, srcIp, dstIp, baseId="default_base_line_id", srcFactoryId=3, dstFactoryId=3):
        BaseApi.__init__(self)
        self.url = host + '/networkBaseLine/item/add'
        self.method = 'post'
        self.json = {"baseId": baseId, "srcFactoryId": srcFactoryId, "srcIp": srcIp, "dstFactoryId": dstFactoryId,
                     "dstIp": dstIp}


class DeleteBaselineDetails(BaseApi):
    """ 删除网络基线明细 """

    def __init__(self, ids, baseId="default_base_line_id"):
        BaseApi.__init__(self)
        self.url = host + '/networkBaseLine/item/del'
        self.method = 'delete'
        self.json = {"ids": ids, "baseId": baseId}


class GenerateBaseline(BaseApi):
    """ 生成端口基线 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/strategy/baseLine/portBaseLine/automaticGenerate'
        self.method = 'post'


class BaselinePage(BaseApi):
    """ 端口基线列表页 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/strategy/baseLine/portBaseLine/portBaseLinelist'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "keyword": ""}


class DeleteGenerateBaseline(BaseApi):
    """ 批量删除端口基线 """

    def __init__(self, ids=[20, 19, 18]):
        BaseApi.__init__(self)
        self.url = host + '/strategy/baseLine/portBaseLine/portBaseLinedelete'
        self.method = 'delete'
        self.json = {"ids": ids}


class AssetListQuery(BaseApi):
    """ 端口基线设备列表查询 """

    def __init__(self, keyword=''):
        BaseApi.__init__(self)
        self.url = host + '/assets/confirm/pageForPortsBaseLine'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "keyword": keyword}


class AddGenerateBaseline(BaseApi):
    """ 新增端口基线 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/strategy/baseLine/portBaseLine/portBaseLineadd'
        self.method = 'post'
        self.json = {"assetId": 88}


class PortBaselineDetails(BaseApi):
    """ 端口基线明细 """

    def __init__(self, portId=59, keyword=''):
        BaseApi.__init__(self)
        self.url = host + '/strategy/baseLine/portBaseLine/portBaseLineInfolist'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "keyword": keyword, "portsBaselineId": portId}


class PortBaselineQuery(BaseApi):
    """ 端口基线查询 """

    def __init__(self, keyword=''):
        BaseApi.__init__(self)
        self.url = host + '/strategy/baseLine/portBaseLine/portBaseLinelist'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "keyword": keyword}


class AddBaselinePort(BaseApi):
    """ 添加基线端口 """

    def __init__(self, portId=59, ports="60"):
        BaseApi.__init__(self)
        self.url = host + '/strategy/baseLine/portBaseLine/portBaseLineInfoadd'
        self.method = 'post'
        self.json = {"portsBaselineId": portId, "ports": ports, "agreement": 1, "service": "service"}


class EditBaselinePort(BaseApi):
    """ 修改基线端口 """

    def __init__(self, id=4, portId=68, ports="61"):
        BaseApi.__init__(self)
        self.url = host + '/strategy/baseLine/portBaseLine/portBaseLineInfoedit'
        self.method = 'post'
        self.json = {"id": id, "portsBaselineId": portId, "ports": ports, "agreement": 1, "service": ""}


class DeleteBaselinePort(BaseApi):
    """ 删除基线端口 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/strategy/baseLine/portBaseLine/portBaseLineInfodelete'
        self.method = 'delete'
        self.json = {"ids": [8]}


# 工单管理

class WorkOrderShow(BaseApi):
    """ 工单管理页 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/workOrder/page'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "keyword": ""}


class AddWorkOrder(BaseApi):
    """ 新增工单 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/workOrder/add'
        self.method = 'post'
        self.json = {"workName": "test",
                     "workExecutor": "tym",
                     "workCreator": "",
                     "startTime": "2022-02-25 00:00:00",
                     "endTime": "2022-02-28 00:00:00",
                     "workPriority": 1,
                     "workStatus": "",
                     "workDescription": "开始",
                     "workExecuteDescription": "结束"}


class WorkOrderAdd(BaseApi):
    """ 新增工单 """

    def __init__(self, startTime, endTime, workName='test', workExecutor='tym', workPriority=1, workDescription='开始',
                 workExecuteDescription='结束'):
        BaseApi.__init__(self)
        self.url = host + '/workOrder/add'
        self.method = 'post'
        self.json = {"workName": workName,
                     "workExecutor": workExecutor,
                     "workCreator": "",
                     "startTime": startTime,
                     "endTime": endTime,
                     "workPriority": workPriority,
                     "workStatus": "",
                     "workDescription": workDescription,
                     "workExecuteDescription": workExecuteDescription}


class ModWorkOrder(BaseApi):
    """ 修改工单 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/workOrder/update'
        self.method = 'put'
        self.json = {"workName": "test",
                     "workExecutor": "tym",
                     "workCreator": "tym",
                     "startTime": "2022-02-24 22:00:00",
                     "endTime": "2022-02-24 23:59:59",
                     "workPriority": 1,
                     "workStatus": 2,
                     "workDescription": "开始",
                     "workExecuteDescription": "结束",
                     "id": 5}


class WorkOrderMod(BaseApi):
    """ 修改工单 """

    def __init__(self, id, startTime, endTime, workCreator='', workStatus=2, workName='test', workExecutor='tym',
                 workPriority=1, workDescription='开始', workExecuteDescription='结束'):
        BaseApi.__init__(self)
        self.url = host + '/workOrder/update'
        self.method = 'put'
        self.json = {"workName": workName,
                     "workExecutor": workExecutor,
                     "workCreator": workCreator,
                     "startTime": startTime,
                     "endTime": endTime,
                     "workPriority": workPriority,
                     "workStatus": workStatus,
                     "workDescription": workDescription,
                     "workExecuteDescription": workExecuteDescription,
                     "id": id}


class DeleteWorkOrder(BaseApi):
    """ 批量删除工单 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/workOrder/delete'
        self.method = 'delete'
        self.json = {"ids": [5]}


class StopWorkOrder(BaseApi):
    """ 终止工单 """

    def __init__(self, id=14, workName="test", workExecutor='tym', createTime="2022-02-25 09:22:57",
                 updateTime="2022-02-25 09:22:57"):
        BaseApi.__init__(self)
        self.url = host + '/workOrder/stop'
        self.method = 'put'
        self.json = {"id": id,
                     "workName": workName,
                     "workStatus": 1,
                     "workDescription": "开始",
                     "workExecuteDescription": "结束",
                     "startTime": "2022-02-25 22:00:00",
                     "endTime": "2022-02-25 23:59:59",
                     "completeTime": '',
                     "workExecutor": workExecutor,
                     "workCreator": "operator",
                     "workExecutorId": 4,
                     "workCreatorId": 2,
                     "createTime": createTime,
                     "updateTime": updateTime,
                     "workPriority": 1,
                     "timeOutFlag": 0}


# 值班管理
class AttendanceMangagement(BaseApi):
    """ 查看值班管理 """

    def __init__(self, keyword=''):
        BaseApi.__init__(self)
        self.url = host + '/workDuty/page'
        self.method = 'post'
        self.json = {"pageSize": 10, "startPage": 1, "keyword": keyword}


class AddAttendanceMangagement(BaseApi):
    """ 新增值班管理 """

    def __init__(self, name='test', alarm_count='6', noProcessCount='7', todayProcessCount='2', assetCount='3',
                 normalAssetCount='7', abnormalAssetCount='2', dangerAssetCount='1', offlineAssetCount='1',
                 unknownAssetCount='3', remnant='', completed='', noCompleted='', workSummary=''):
        BaseApi.__init__(self)
        self.url = host + '/workDuty/add'
        self.method = 'post'
        self.json = {"workDutyName": name, "todayAlarmCount": alarm_count, "noProcessCount": noProcessCount,
                     "todayProcessCount": todayProcessCount,
                     "assetCount": assetCount, "normalAssetCount": normalAssetCount,
                     "abnormalAssetCount": abnormalAssetCount, "dangerAssetCount": dangerAssetCount,
                     "offlineAssetCount": offlineAssetCount, "unknownAssetCount": unknownAssetCount,
                     "remnantWorkSituation": remnant,
                     "completedWork": completed, "noCompletedWork": noCompleted, "workSummary": workSummary}


class ModAttendanceMangagement(BaseApi):
    """ 修改值班表 """

    def __init__(self, id=10, name='test', alarm_count='50', noProcessCount='7', todayProcessCount='2', assetCount='3',
                 normalAssetCount='7', abnormalAssetCount='2', dangerAssetCount='1', offlineAssetCount='1',
                 unknownAssetCount='3', remnant='', completed='', noCompleted='', workSummary=''):
        BaseApi.__init__(self)
        self.url = host + '/workDuty/update'
        self.method = 'put'
        self.json = {"workDutyName": name, "todayAlarmCount": alarm_count, "noProcessCount": noProcessCount,
                     "todayProcessCount": todayProcessCount,
                     "assetCount": assetCount, "normalAssetCount": normalAssetCount,
                     "abnormalAssetCount": abnormalAssetCount, "dangerAssetCount": dangerAssetCount,
                     "offlineAssetCount": offlineAssetCount, "unknownAssetCount": unknownAssetCount,
                     "remnantWorkSituation": remnant, "completedWork": completed,
                     "noCompletedWork": noCompleted, "workSummary": workSummary, "id": id}


class DeleteAttendanceMangagement(BaseApi):
    """ 删除值班管理 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/workDuty/delete'
        self.method = 'delete'


class DeleteWorkMangagement(BaseApi):
    """ 删除值班管理 """

    def __init__(self, id=[2]):
        BaseApi.__init__(self)
        self.url = host + '/workDuty/delete'
        self.method = 'delete'
        self.json = {"ids": id}


class CheckNoCompleteWork(BaseApi):
    """ 删除值班管理 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/workDuty/noCompleteWork'
        self.method = 'get'


class ExportAttendanceSchedule(BaseApi):
    """ 导出值班管理 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/workDuty/download?workDutyName='
        self.method = 'get'
        # self.params = {
        #     'workDutyName':''
        # }


class KnowledgeUpdateConfig(BaseApi):
    """ 知识库更新配置 """

    def __init__(self, ip="180.76.136.243"):
        BaseApi.__init__(self)
        self.url = host + '/knowledge/setting/update'
        self.method = 'post'
        self.json = {"ip": ip}


