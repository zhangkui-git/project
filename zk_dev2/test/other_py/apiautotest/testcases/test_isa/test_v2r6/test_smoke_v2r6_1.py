'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/2/23 14:23
software: PyCharm
'''
import datetime
import json
import os
import re
import time

import allure
import pytest
import requests

# from zk_dev2.test.other_py.apiautotest.api.isa.alarm_handling import AlarmRetrieval, AlarmOverview, AlarmOverviewPicture, AlarmRetrievalTraceability, \
#     AlarmTraceabilityList, AlarmTraceabilityEventList, ThreatIntelligenceDetails, ThreatIntelligence
from zk_dev2.test.other_py.apiautotest.api.isa.asset_center import *
# from zk_dev2.test.other_py.apiautotest.api.isa.audit import OperatorLog
# from zk_dev2.test.other_py.apiautotest.api.isa.data_analysis import LogRetrieve
# from zk_dev2.test.other_py.apiautotest.api.isa.login import VulnerabilityConfiguration
# from zk_dev2.test.other_py.apiautotest.api.isa.monitoring_center import SafetyNotice, AddSafetyNotice, DeleteSafetyNotice, ThreatTransverse, \
#     OperationalSituation, OperationalSituationQuickSearh, QuickSearhPage, RunMonitoringPage, RealTimeCpu, HistoryTimeCpu
from zk_dev2.test.other_py.apiautotest.api.isa.policy_config import *
# from zk_dev2.test.other_py.apiautotest.api.isa.report_manage import AddInstantReport, ReportManageChapter, InstantReportList, DeleteInstantReport
# from zk_dev2.test.other_py.apiautotest.api.isa.security_knowledge_base import CommonPortLibrary, ModCommonPort, EqualProtectionKnowledgeBase, \
#     AssetFingerprintLibrary, AssetFingerprintQuickSearch, VulnerabilityLibrary, SuggestionLibrary, \
#     SecurityAnalysisQuery, IntelligenceUpdate, IntelligenceUpdatePage, IntelligenceUpload, IntelligenceDetail
# from zk_dev2.test.other_py.apiautotest.api.isa.system_config import AddDashboard, DashboardPage, DeleteDashboard, AuthorizationManagement, ShowDashboard
# from zk_dev2.test.other_py.apiautotest.api.login_api import login_test, Login
# from zk_dev2.test.other_py.apiautotest.common.dbutil import DB, Linux
# from zk_dev2.test.other_py.apiautotest.common.syslog import syslog
# from zk_dev2.test.other_py.apiautotest.config.config import host, IP, linux_port, linux_user, linux_pass
# from zk_dev2.test.other_py.apiautotest.data.common_data import personal_username, password, audit, admin


@allure.feature('冒烟测试')
class Test_V2R6_Smoke():
    # 前置处理创建数据库对象
    # def setup_class(self):
    #     self.db = DB('database')
    #
    # # 后置处理，断开数据库连接
    # def teardown_class(self):
    #     self.db.close()

    @allure.story('ISA-3119')
    def test_add_field_information(self):
        """
        ISA-3119 : 【已确认资产】新增字段信息为添加资产时填写的信息
        1 点击新增资产	弹出新增资产弹窗
        2 手动输入归属单位，归属专业，归属系统，主机名，物理端口编号，注册时间，资产业务价值，资产机密性，资产完整性，资产可用性、安全责任人 输入其他必填项并保存 查看新增资产信息	列表中： 归属单位，归属专业，归属系统，主机名，物理端口编号，注册时间，资产业务价值，资产机密性，资产完整性，资产可用性，安全责任人 显示为新增资产时手动填写的信息
        """
        # 查看日志源页面，获取id,传入修改日志源接口
        resp = LogSourcePage().send()
        result = resp.json()
        print(1111, result)
        # id = result['data']['logSourceList']['list'][0]['id']
        id = result['data']
        assetIp = result['data']['logSourceList']['list'][0]['assetIp']  # 日志源ip
        print(2222, assetIp)
        # 修改日志源
        mod = ModLogSource()
        mod.json = {"logSourceName": assetIp, "assetIp": assetIp, "factory": 3, "assetType": 101001,
                    "port": '', "protocolType": 1, "snmpVersion": '', "normalizeGroup": [1386, 1393, 1400, 11404],
                    "community": '', "isAnonymousLogin": 0, "userName": '', "password": '', "filePath": '',
                    "originalEncoding": '', "downloadRate": '', "taskInterval": '', "ftpMode": '', "dbType": '',
                    "dbName": '', "customerSqlStatus": 0, "dbTableName": '', "selectSql": '', "isEncryption": 0,
                    "algorithm": 1, "privateKey": "", "id": id}
        resp = mod.send()
        result = resp.json()
        print(result)
        # 勾选所有字段
        resp = SelectAllList().send()

        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        # 新增资产
        resp = AddAsset().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 1001)
        data = result['data']
        id = data['id']  # 已确认资产列表需要使用”id“信息
        pytest.assume(data['ip'] == '192.168.56.3' and data['belongProfessiona'] == 'test1' and data['name'] == 'test1')
        pytest.assume(
            data['belongingSystem'] == 'test1' and data['belongingUnit'] == 'test1' and data['hostName'] == 'test1' and
            data[
                'safetyResponsiblePerson'] == 'test1')
        # 已确认资产列表
        resp = RecognizedAssetsList().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        data_list = result['data']['list']
        print(data_list)
        # 根据id判断新增资产进行断言
        for data in data_list:
            if data['id'] == str(id):
                pytest.assume(
                    data['ip'] == '192.168.56.3' and data['belongProfessiona'] == 'test1' and data['name'] == 'test1')
                pytest.assume(data['belongingSystem'] == 'test1' and data['belongingUnit'] == 'test1' and data[
                    'hostName'] == 'test1' and data[
                                  'safetyResponsiblePerson'] == 'test1')
        # 删除资产
        delete = DeleteAsset()

        delete.json = {
            "ids": [id]
        }
        resp = delete.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 1000)


if __name__ == '__main__':
    Test_V2R6_Smoke().test_add_field_information()


