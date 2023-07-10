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

from zk_dev2.test.other_py.apiautotest.api.isa.alarm_handling import AlarmRetrieval, AlarmOverview, AlarmOverviewPicture, AlarmRetrievalTraceability, \
    AlarmTraceabilityList, AlarmTraceabilityEventList, ThreatIntelligenceDetails, ThreatIntelligence
from zk_dev2.test.other_py.apiautotest.api.isa.asset_center import *
from zk_dev2.test.other_py.apiautotest.api.isa.audit import OperatorLog
from zk_dev2.test.other_py.apiautotest.api.isa.data_analysis import LogRetrieve
from zk_dev2.test.other_py.apiautotest.api.isa.login import VulnerabilityConfiguration
from zk_dev2.test.other_py.apiautotest.api.isa.monitoring_center import SafetyNotice, AddSafetyNotice, DeleteSafetyNotice, ThreatTransverse, \
    OperationalSituation, OperationalSituationQuickSearh, QuickSearhPage, RunMonitoringPage, RealTimeCpu, HistoryTimeCpu
from zk_dev2.test.other_py.apiautotest.api.isa.policy_config import *
from zk_dev2.test.other_py.apiautotest.api.isa.report_manage import AddInstantReport, ReportManageChapter, InstantReportList, DeleteInstantReport
from zk_dev2.test.other_py.apiautotest.api.isa.security_knowledge_base import CommonPortLibrary, ModCommonPort, EqualProtectionKnowledgeBase, \
    AssetFingerprintLibrary, AssetFingerprintQuickSearch, VulnerabilityLibrary, SuggestionLibrary, \
    SecurityAnalysisQuery, IntelligenceUpdate, IntelligenceUpdatePage, IntelligenceUpload, IntelligenceDetail
from zk_dev2.test.other_py.apiautotest.api.isa.system_config import AddDashboard, DashboardPage, DeleteDashboard, AuthorizationManagement, ShowDashboard
from zk_dev2.test.other_py.apiautotest.api.login_api import login_test, Login
from zk_dev2.test.other_py.apiautotest.common.dbutil import DB, Linux
from zk_dev2.test.other_py.apiautotest.common.syslog import syslog
from zk_dev2.test.other_py.apiautotest.config.config import host, IP, linux_port, linux_user, linux_pass
from zk_dev2.test.other_py.apiautotest.data.common_data import personal_username, password, audit, admin

@allure.feature('冒烟测试')
class Test_V2R6_Smoke():
    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

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
        print(result)
        id = result['data']['logSourceList']['list'][0]['id']
        assetIp = result['data']['logSourceList']['list'][0]['assetIp']  # 日志源ip
        print(assetIp)
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

    @allure.story('ISA-3136')
    def test_asset_portrait_add_value(self):
        """
        ISA-3136 : 【已确认资产】资产画像页面新增资产业务价值
        选择新增的资产 进入资产画像查看资产信息	在“资产属性-所属区域”下方新增“资产业务价值” 显示为该资产设置的资产业务价值-3
        """
        # 新增资产
        resp = AddAsset().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 1001)
        data = result['data']
        id = data['id']  # 已确认资产列表需要使用”id“信息
        # 点击新增资产进入资产画像
        portrait = AssetPortrait()
        portrait.url = host + '/assets/situations/base?assetId={}'.format(id)

        resp = portrait.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['data']['assetBusinessValue'] == 3)  # 资产业务价值” 显示为该资产设置的资产业务价值-3
        # 删除资产
        delete = DeleteAsset()

        delete.json = {
            "ids": [id]
        }
        resp = delete.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 1000)

    @allure.story('ISA-3135')
    def test_add_asset_attributes(self):
        """
        ISA-3135 : 【属性管理】新增资产时填写属性字段
        1 点击新增资产，查看页面属性字段	新增资产页面新增名称为“test字符串”和“test数字”的属性字段
        2 test字符串”属性字段输入框输入合法字符，如“test字符串” “test数字”属性字段输入框输入合法字符，如“123456” 输入其他必填项 点击保存	属性字段值为“test字符串”和“123456”的资产添加成功
        """
        # 新增一个属性，名称为“test字符串”，类型为字符串
        attributes = AddAttributes()
        resp = attributes.send()
        result = json.loads(resp.text)
        print('attributes', result)
        pytest.assume(result['statusCode'] == 200)
        # 新增一个属性，名称为“test数字”，类型为数字
        attributes = AddAttributes()
        attributes.json = {"name": "test数字", "type": 2}
        resp = attributes.send()
        result = json.loads(resp.text)
        print('attributes', result)
        pytest.assume(result['statusCode'] == 200)
        # time.sleep(1)
        # 新增资产
        # resp = AssetList().send()
        # result = json.loads(resp.text)
        # print(result)
        # time.sleep(1)
        add = AddAsset()
        add.json = {
            "ip": "192.168.56.3",
            "name": "test1",
            "modelId": "",
            "factoryId": 3,
            "mac": "",
            "alias": "",
            "serialNumber": "",
            "deviceVersion": "",
            "hasGuard": "",
            "operateSystem": "",
            "ipMacs": [

            ],
            "typeId": "",
            "vendorId": "",
            "belongingUnit": "",
            "belongProfessiona": "",
            "belongingSystem": "",
            "hostName": "",
            "physicalPortNumber": "",
            "loginTime": "",
            "assetBusinessValue": "3",
            "assetConfidentiality": "",
            "assetIntegrity": "",
            "assetAvailability": "",
            "safetyResponsiblePerson": "",
            "values": ["test", "123"]
        }
        resp = add.send()
        result = json.loads(resp.text)
        print('新增', result)
        pytest.assume(result['statusCode'] == 1001)
        data = result['data']
        asset_id = data['id']  # 已确认资产列表需要使用”id“信息
        time.sleep(1)
        # 获取资产详情
        # resp = AssetList().send()
        # result = json.loads(resp.text)
        # print(result)
        # time.sleep(1)
        get = GetAsset()
        get.url = host + '/assets/confirm/{}'.format(asset_id)
        print(get.url)
        resp = get.send()
        result = json.loads(resp.text)
        print('get', result)
        value = result['data']['values']
        print(value)
        pytest.assume(value == ['test', '123'])
        # 删除资产
        delete = DeleteAsset(id=[asset_id])

        resp = delete.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 1000)

        # 批量删除属性
        id = self.db.select(
            "select id from soc.soc_asset_attribute where name = 'test数字' or name='test字符串'")  # 查询'test数字'、'test字符串'id
        print(id)
        ids = [id[0]['id'], id[1]['id']]
        print({"ids": ids})
        batch = BatchDeleteAttributes()
        batch.json = {"ids": ids}
        resp = batch.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)

    @allure.story('ISA-3140')
    def test_asset_life_cycle_show(self):
        """
        ISA-3140 : 【资产生命周期】资产生命周期展示框按照资产id通过时间轴展示
        1 进入“资产管理-资产生命周期”查看新增数据    新增一条数据：资产名称，资产IP，区域，更新时间，操作人员，操作内容（XX人员新增XX资产）
        2 选择创建的资产进入资产画像 查看资产生命周期展示框	资产生命周期展示框展示资产“192.168.1.1”的创建和编辑记录 按照时间轴展示
        3 查看时间轴节点信息	资产名称，资产IP，区域，更新时间，操作人员，操作内容 内容参考资产生命周期列表数据
        """
        # 新增资产
        add = AddAsset()
        add.json = {
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
            "ip": "192.168.56.35",
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
        resp = add.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 1001)
        data = result['data']
        asset_id = data['id']  # 已确认资产列表需要使用”id“信息
        time.sleep(5)
        # 查看资产生命周期页
        resp = AssetLifeCycle().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        num = result['data']['total']  # 资产生命周期总数
        print(num)
        asset = AssetLifeCycle()
        asset.json = {
            "pageSize": 10, "startPage": 1, "keyword": ""
        }
        resp = asset.send()
        result = json.loads(resp.text)
        value = result['data']['list'][0]
        pytest.assume(value['name'] == 'test1')
        pytest.assume(value['ip'] == '192.168.56.35')
        pytest.assume(value['factoryName'] == 'XX区域')
        pytest.assume(value['operator'] == 'operator')
        pytest.assume(value['operationContent'] == '[operator]手动添加资产')
        pytest.assume(str(datetime.datetime.now())[:10] in value['updateTime'])
        # if num % 10 == 0:  # 10的整数条
        #     page_num = num / 10  # 页数
        #     print(page_num)
        #     asset = AssetLifeCycle()
        #     asset.json = {
        #         "pageSize": 10, "startPage": page_num, "keyword": ""
        #     }
        #     resp = asset.send()
        #     result = json.loads(resp.text)
        #     value = result['data']['list'][-1]
        #     # assert_value = value['name'] == 'test1' and value['ip'] == '192.168.56.35' and value[
        #     #     'factoryName'] == 'XX区域' and value['operator'] == 'operator' and value[
        #     #                    'operationContent'] == '[operator]手动添加资产' and str(datetime.datetime.now())[:10] in \
        #     #                value['updateTime']
        #     # pytest.assume(assert_value)
        #     pytest.assume(value['name'] == 'test1')
        #     pytest.assume(value['ip'] == '192.168.56.35')
        #     pytest.assume(value['factoryName'] == 'XX区域')
        #     pytest.assume(value['operator'] == 'operator')
        #     pytest.assume(value['operationContent'] == '[operator]手动添加资产')
        #     pytest.assume(str(datetime.datetime.now())[:10] in value['updateTime'])
        # else:
        #     num % 10 != 0  # 非10的整数
        #     page_num = int(num / 10)  # 页数为page_num + 1,强制转换为整数
        #     print(page_num + 1)
        #     asset = AssetLifeCycle()
        #     asset.json = {
        #         "pageSize": 10, "startPage": 1, "keyword": ""
        #     }
        #     resp = asset.send()
        #     result = json.loads(resp.text)
        #     value = result['data']['list'][0]
        #
        #     print(value)
        #     print(str(datetime.datetime.now())[:10])
        #     print(value['name'] == 'test1')
        #     print(value['ip'] == '192.168.56.35')
        #     print(value['factoryName'] == 'XX区域')
        #     print(value['operator'] == 'operator')
        #     print(value['operationContent'] == '[operator]手动添加资产')
        #     # pytest.assume(
        #     #     value['name'] == 'test1' and value['ip'] == '192.168.56.35' and value['factoryName'] == 'XX区域' and
        #     #     value['operator'] == 'operator' and value['operationContent'] == '[operator]手动添加资产' and str(datetime.datetime.now())[:10] == value['updateTime'][:10])
        #     pytest.assume(value['name'] == 'test1')
        #     pytest.assume(value['ip'] == '192.168.56.35')
        #     pytest.assume(value['factoryName'] == 'XX区域')
        #     pytest.assume(value['operator'] == 'operator')
        #     pytest.assume(value['operationContent'] == '[operator]手动添加资产')
        #     pytest.assume(str(datetime.datetime.now())[:10] == value['updateTime'][:10])

        # 资产画像生命周期

        asset = AssetPortraitLifeCycle()
        asset.json = {"assetId": asset_id, "factoryId": 3}
        resp = asset.send()
        result = json.loads(resp.text)
        print(result)
        value = result['data'][0]
        print(value)
        # assert_value = value['name'] == 'test1' and value['ip'] == '192.168.56.3' and value['factoryName'] == 'XX区域' and \
        #                value['operator'] == 'operator' and value['operationContent'] == 'operator手动添加test1资产' and str(datetime.datetime.now())[:10] in str(value['updateTime'])
        # 只能展示十条，且十条后不在更新
        # assert_value = value['name'] == 'test1' and value['ip'] == '192.168.56.35' and value[
        #     'factoryName'] == 'XX区域' and value['operator'] == 'operator'
        print(value['name'] == 'test1')
        print(value['factoryName'] == 'XX区域')
        print(value['operator'] == 'operator')
        print(value['ip'] == '192.168.56.35')
        print(value['operationContent'] == '[operator]手动添加资产')
        pytest.assume(value['name'] == 'test1' and value['ip'] == '192.168.56.35' and value[
            'factoryName'] == 'XX区域' and value['operator'] == 'operator' and value['operationContent'] == '[operator]手动添加资产')
        # 删除资产
        delete = DeleteAsset()
        delete.json = {
            "ids": [asset_id]
        }
        resp = delete.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 1000)

    @allure.story('ISA-3147')
    def test_risk_score(self):
        """
        ISA-3147 : 【合规评估】保存风险评分时按照最新配比重新评估资产
        1 资产漏洞风险权重选择8 资产威胁风险权重选择1 资产合规风险权重选择1 点击保存	  保存成功
        2 查看资产风险评分   按照漏洞：威胁：合规=8:1:1重新进行评分 按照最新的公式计算风险评分
        [ 漏洞风险权重 x 漏洞风险指数 + 威胁风险权重 x 威胁风险指数 + 合规风险权重x (100-合规评分) / 10 ] x ( 资产业务价值 / 5 )
        """
        # todo 增加对应告警 查看资产评分
        # 资产漏洞风险权重
        try:
            risk = RiskScore()
            resp = risk.send()
            result = json.loads(resp.text)
            print(result)
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['param'] == ['8', '1', '1'])  # 权重按8：1：1分配

            pytest.assume(result['data']['score'] == 50)  # 评分
            pytest.assume(result['data']['level'] == 2)  # 等级
            # 新增资产
            resp = AddAsset().send()
            result = json.loads(resp.text)
            print(result)
            pytest.assume(result['statusCode'] == 1001)
            data = result['data']
            asset_id = data['id']  # 已确认资产列表需要使用”id“信息
            time.sleep(1)
            # 发送设备告警
            # syslog('{"originLog":"30|^致命|^2021-06-03 15:23:30|^WIN-PP4LSTF6N3H|^192.168.56.35|^f:\\virus\\virus.win32.sality.gen\\hnth.exe|^ca36ecd2175a13066ce1cb91ab6d2c16|^b6115d3dc9e9c92c2c2a5c78a73662ec69f0d1de|^e73e6da59114deac7ef58b7d93c4ee05e35b45c9345400405322070412f6b647|^未知|^win.virus.sality-1067|^控制模式执行：阻止，白名单校验：未通过|^ClamAV 0.102.4/25980|^59|^1|^","ruleId":"60b9fe9b443f08360cfb801d","deviceIp":"192.168.4.64"}')
            syslog(
                '5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.56.3|^192.168.56.3|^MAC：d0:37:45:1e:8e:07与 IP：192.168.56.3不匹配|^1|^null|^201229008|^')
            time.sleep(40)
            # 获取资产详情,获取评分值
            get = GetAsset()
            get.url = host + '/assets/confirm/{}'.format(asset_id)
            resp = get.send()
            result = json.loads(resp.text)
            risk_score_before = result['data']['riskScore']  # 资产评分
            print('risk_scorebefore', risk_score_before)
            # 资产漏洞风险权重
            risk.json = {"vul": 0, "threat": 10, "compliant": 0}
            resp = risk.send()
            result = json.loads(resp.text)
            print(result)
            pytest.assume(result['statusCode'] == 200)
            time.sleep(5)
            # 获取资产详情，获取评分值
            get = GetAsset()
            get.url = host + '/assets/confirm/{}'.format(asset_id)
            resp = get.send()
            result = json.loads(resp.text)
            print(result)
            risk_after = result['data']['riskScore']  # 资产评分
            print('risk_after', risk_after)
            pytest.assume(risk_score_before != risk_after)
        except Exception:
            raise Exception
        finally:
            # 删除资产
            delete = DeleteAsset()
            delete.json = {
                "ids": [asset_id]
            }
            resp = delete.send()
            result = json.loads(resp.text)
            print(result)
            pytest.assume(result['statusCode'] == 1000)

    # todo  3117 (不做自动化测试)
    @allure.story('ISA-3115 ')
    def test_log_encry(self):
        """
        ISA-3115 : 【日志加密】加密日志解密后可以进行范化
        1 在态势感知系统创建一个接收syslog的日志源并启用加密  日志源创建成功
        2 向日志审计系统发送日志 在态势感知系统查看收到的日志信息  系统收到日志并且范化成功
        """
        try:
            resp = LogSourcePage().send()
            result = resp.json()
            print(result)
            id = result['data']['logSourceList']['list'][0]['id']
            assetIp = result['data']['logSourceList']['list'][0]['assetIp']  # 日志源ip
            # 修改日志源，配置日志源加密
            mod = ModLogSource()
            mod.json = {"logSourceName": assetIp, "assetIp": assetIp, "factory": 3, "assetType": 101001, "port": '',
                        "protocolType": 1, "snmpVersion": '', "normalizeGroup": ["1393", "1386", "1400", "11404"],
                        "community": '',
                        "isAnonymousLogin": 0, "userName": '', "password": '', "filePath": '', "originalEncoding": '',
                        "downloadRate": '', "taskInterval": '', "ftpMode": '', "dbType": '', "dbName": '',
                        "customerSqlStatus": 0, "dbTableName": '', "selectSql": '', "isEncryption": 1, "algorithm": 1,
                        "privateKey": 'Admin@1234567890', "id": id}
            resp = mod.send()
            result = resp.json()
            print(result)
            time.sleep(1)
            # 日志检索，查看第一条数据
            resp = LogRetrieve().send()
            result = resp.json()
            before_total = result['total']
            #  发送加密的数据
            syslog(
                '181CFE736298F1DECB9B6976A5CF08C00B427A4BFC44E75695FF1CEE6630799DDF2F84D8CCDA9D1DFAEB88288C021F4663C1E7796B896D48C7C933C21389E1E17B2A0672AE6313AE9A2422CDA45D752C1BCA36250BBC011BCB3F1B2CD089B4262C7C0BA8D3310AA1F74498035A3F88EE9558845BAB704E4DC3F77A3E5C068BE167FB343D70723F3127B91C77BDB9BF561BA34B74A83F37B3310862CB16ADAB257096F253244C59601A660771A5C590C4FE1EE5E6FCFAEE80CDF243F37C77050AB5601A7AF22EFBD5AD8F080DCE61845FCA1495CA69FD58AF8576A32E23D7B6F2817C47DE09F7563701FA7ABC26B0D12D7F91BBC51B527A6D584F24EDA7EB8FBD4E7931CC7F81C3781598301E4A18C529F574F8E5B4F2D5022F1416530BA3FF51531DD6D59331D578C00EB1F0DF9C3BDCD9F7E3D03DDB018DB3BB3EFBE7AB37B5715112641D3A907F46197930D67B624A')
            time.sleep(30)
            # 日志检索，查看第一条数据
            resp = LogRetrieve().send()
            result = resp.json()
            data = result['dataList'][0]['originlog']
            after_total = result['total']
            # 判断第一条日志
            pytest.assume(
                data == '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.100.124|^Probe201229008|^2021-06-03 16:28:37|^17|^192.168.100.123|^|^64766|^224.0.0.252|^|^5355|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^')
            pytest.assume(int(after_total) - int(before_total) == 1)  # 判断新增一条数据
        except Exception as e:
            raise e
        finally:
            # 修改日志源，取消日志源加密
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

    @allure.story('ISA-3110')
    def test_work_order_status_processing(self):
        """
        ISA-3110 : 【工单管理】非创建人处理工单状态为处理中
        1	选择不是当前登录用户创建的工单，点击“修改”按钮	弹出编辑工单弹窗
        2	工单状态选择处理中 点击保存	工单状态修改成功
        3	通过筛选条件筛选处理中的工单	可筛选到处理中工单
        """
        # tym用户创建工单
        # Authorization = login_test(personal_username, password)  # tym用户登录
        # print(Authorization)
        order = AddWorkOrder()
        # order.headers = Authorization  # tym的登录header
        start_time = str((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")) + ' 23:57:00'  # 开始时间
        end_time = str((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")) + ' 23:59:59'  # 开始时间
        order.json = {
            "workName": "test",
            "workExecutor": "operator",
            "workCreator": "",
            "startTime": start_time,
            "endTime": end_time,
            "workPriority": 1,
            "workStatus": "",
            "workDescription": "开始",
            "workExecuteDescription": "结束"
        }
        resp = order.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        # 工单管理页展示获取id信息，传入修改工单接口
        resp = WorkOrderShow().send()
        result = json.loads(resp.text)
        id = result['data']['list'][-1]['id']
        # print(id)
        # operator用户修改工单
        mod = ModWorkOrder()
        mod.json = {
            "workName": "test",
            "workExecutor": "tym",
            "workCreator": "tym",
            "startTime": start_time,
            "endTime": end_time,
            "workPriority": 1,
            "workStatus": 2,
            "workDescription": "开始",
            "workExecuteDescription": "结束",
            "id": id
        }
        mod.send()
        result = json.loads(resp.text)
        print('mod', result)
        pytest.assume(result['statusCode'] == 200)
        # 筛选处理中的工单
        show = WorkOrderShow()
        show.json = {"pageSize": 10, "startPage": 1, "keyword": "", "workStatus": 2, "workPriority": ""}
        resp = show.send()
        result = json.loads(resp.text)
        print(result['data'])
        print(result['data']['list'])
        print(result['data']['list'][-1]['id'])
        pytest.assume(result['data']['list'][-1]['id'] == id)  # 判断为同一id
        # 删除工单
        show = DeleteWorkOrder()
        show.json = {"ids": [id]}
        resp = show.send()
        result = json.loads(resp.text)
        pytest.assume(result['statusCode'] == 200)

    @allure.story('ISA-3113')
    def test_stop_work_order(self):
        """
        ISA-3113 : 【工单管理】终止工单
        1	选择一个工单数据，点击终止	弹出二次确认弹窗
        2	点击确定	工单终止成功
        3	通过筛选条件筛选已终止状态的工单	筛选出已终止的工单
        """
        # 创建工单
        order = AddWorkOrder()
        start_time = str((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")) + ' 23:57:00'  # 开始时间
        end_time = str((datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")) + ' 23:59:59'  # 开始时间
        order.json = {
            "workName": "test",
            "workExecutor": "operator",
            "workCreator": "",
            "startTime": start_time,
            "endTime": end_time,
            "workPriority": 1,
            "workStatus": "",
            "workDescription": "开始",
            "workExecuteDescription": "结束"
        }
        resp = order.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        # 工单管理页展示获取id信息，传入修改工单接口
        resp = WorkOrderShow().send()
        result = json.loads(resp.text)
        id = result['data']['list'][-1]['id']
        work_executor = result['data']['list'][-1]['workExecutor']
        work_cxecutor = result['data']['list'][-1]['workCreator']
        # print(id,work_executor, work_cxecutor)
        print(result)
        # 终止工单
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        stop = StopWorkOrder()
        stop.json = {
            "id": id,
            "workName": "test",
            "workStatus": 1,
            "workDescription": "开始",
            "workExecuteDescription": "结束",
            "startTime": start_time,
            "endTime": end_time,
            "completeTime": '',
            "workExecutor": work_executor,
            "workCreator": work_cxecutor,
            "workExecutorId": 4,
            "workCreatorId": 2,
            "createTime": time,
            "updateTime": time,
            "workPriority": 1,
            "timeOutFlag": 0
        }
        resp = stop.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        # 筛选处理中的工单
        show = WorkOrderShow()
        show.json = {"pageSize": 10, "startPage": 1, "keyword": "", "workStatus": 4, "workPriority": ""}
        resp = show.send()
        result = json.loads(resp.text)
        print(result['data'])
        print(result['data']['list'])
        print(result['data']['list'][-1]['id'])
        pytest.assume(result['data']['list'][-1]['id'] == id)  # 判断为同一id
        # 删除工单
        show = DeleteWorkOrder()
        show.json = {"ids": [id]}
        resp = show.send()
        result = json.loads(resp.text)
        pytest.assume(result['statusCode'] == 200)

    # todo  3069页面信息校验
    @allure.story('ISA-3469')
    def test_vulnerability_distribution(self):
        """
        ISA-3069 :【漏洞分布】新增菜单资产中心/漏洞管理/漏洞分布
        1	查看漏洞管理下的子菜单	看到了新增的子菜单“漏洞分布”；
        2	查看面包屑导航	面包屑导航为“资产中心>漏洞管理>漏洞分布”；
        3	点击选择“漏洞分布”子菜单	页面显示漏洞分布列表；
        4	查看列表项	列表项包括：漏洞名称、危险级别、CVE编码、CNVD编码、CNNVD编码、漏洞类别、发布时间、是否是工控漏洞、影响主机数、影响主机比例、操作（详情）；
        """
        try:
            # admin打开 匹配漏洞开关
            header = login_test(admin, password)
            config = VulnerabilityConfiguration()
            config.headers = header
            resp = config.send()
            result = json.loads(resp.text)
            print('admin', result)
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '操作成功')
            # 新增资产
            add = AddAsset()
            add.json = {"ip": "192.168.0.202", "name": "192.168.0.202", "modelId": "", "factoryId": 3, "mac": "",
                        "alias": "", "serialNumber": "", "deviceVersion": "", "hasGuard": "",
                        "operateSystem": "Linux Kernel 2.6", "ipMacs": [], "typeId": "", "vendorId": "",
                        "belongingUnit": "", "belongProfessiona": "", "belongingSystem": "", "hostName": "",
                        "physicalPortNumber": "", "loginTime": "", "assetBusinessValue": "3", "assetConfidentiality": "",
                        "assetIntegrity": "", "assetAvailability": "", "safetyResponsiblePerson": "", "values": []}
            resp = add.send()
            result = resp.json()
            print(result)
            id = result['data']['id']
            pytest.assume(result['message'] == '操作成功')

            # 查看漏洞分布
            resp = VulnerabilityDistributionPage().send()
            result = resp.json()
            print(result)
            value = result['data']['values'][0]  # 分布记录第一条
            pytest.assume(
                'vulName' in value and 'vulLevelName' in value and 'cve' in value and 'cnvd' in value and 'cnnvd' in value and 'vulTypeName' in value and 'vulReleaseTime' in value and 'icsName' in value and 'amount' in value and 'proportion' in value)
        except Exception:
            raise Exception
        finally:
            # 关闭漏洞开关
            config.json = {"match": 0}
            resp = config.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '操作成功')
            # 删除资产
            delete = DeleteAsset()
            delete.json = {"ids": [id]}
            resp = delete.send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')

    @allure.story('ISA-3070')
    def test_mod_config_click_confirm_faild(self):
        """
        ISA-3070 : 【配置扫描器】修改配置后不可直接点击确定按钮
        1	修改用户名、密码、扫描器地址中的一个或多个，点击确定按钮	按钮可点击，点击后保存；
        2	输入不正确的用户名，密码输入正确，点击确定按钮	提示“ 扫描器中的用户名或密码错误”；
        3	输入正确的用户名，密码输入错误，点击确定按钮	提示“扫描器中的用户名或密码错误”；
        4	点击测试连接，连接失败    提示“链接服务器失败，请确认漏洞扫描器状态”；
        5   再次执行步骤1后，点击测试连接，连接成功    提示“测试连接成功”；
        """
        # 正确的IP，错误的用户名
        scan = ScanTestConnection()
        scan.json = {
            "user": "admin111",
            "pwd": "Admin@123",
            "ip": "192.168.14.20"
        }
        resp = scan.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '扫描配置中用户名或密码错误')
        # 正确的IP，错误的密码
        scan = ScanTestConnection()
        scan.json = {
            "user": "admin",
            "pwd": "Admin@123111",
            "ip": "192.168.14.20"
        }
        resp = scan.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '扫描配置中用户名或密码错误')
        # 错误的ip
        scan = ScanTestConnection()
        scan.json = {
            "user": "admin111",
            "pwd": "Admin@123",
            "ip": "192.168.14.201"
        }
        resp = scan.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '连接服务器失败，请确认漏洞扫描器状态')
        # 正确的IP，正确的用户名密码
        scan = ScanTestConnection()
        scan.json = {
            "user": "admin",
            "pwd": "Admin@123",
            "ip": "192.168.14.20"
        }
        resp = scan.send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '连接成功！')
        # 点击确定，保存成功
        resp = ScanTestConfirm().send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '操作成功')

    @allure.story('ISA-3071')
    def test_add_common_port_libary(self):
        """
        ISA-3071 : 【新增常见端口库】新增菜单安全知识库/常见端口库概述
        1	查看“安全知识库”下的子菜单	看到了新增的子菜单“常见端口库”；
        2	查看面包屑导航	面包屑导航为“安全知识库>常见端口库”；
        3	点击选择“常见端口库”子菜单	页面显示常见端口知识库列表；
        4	查看列表项	列表项包括端口号、传输层协议、服务、是否高危、操作（编辑、删除）；
        """
        # 常见端口库
        port = CommonPortLibrary()
        resp = port.send()
        result = json.loads(resp.text)
        print(result)
        port_info = result['data']['list'][0]
        pytest.assume(result['statusCode'] == 200)
        # port 端口号、transportLayer 传输协议、serviceType 服务、highRisk 是否高危
        pytest.assume(
            'port' in port_info and 'transportLayer' in port_info and 'serviceType' in port_info and 'highRisk' in port_info)

    @allure.story('ISA-3072')
    def test_mod_common_port(self):
        """
        ISA-3072 : 【编辑常见端口】常见端口页面列表项“操作”中的编辑常见端口页面
        1	点击“编辑”按钮	出现“编辑常见端口”弹窗；
        2	弹出的页面中修改端口号，输入符合校验规则的端口号，如：83 与内置端口号无关，仅限非内置端口	进行重复校验； 不重复则修改成功；
        3	弹出的页面中修改端口号，输入符合校验规则的端口号，输入的端口号与内置端口相同，传输层协议不同
        4	修改其他几项	均可以修改，只要填写合规即可；
        5	填写均符合校验规则，点击确定按钮	可以成功修改；
        """
        # 新增非内置端口
        self.db.update(
            "INSERT INTO soc.soc_ports_library (port,transport_layer,service_type,high_risk,create_user_id,is_custom,remark,create_time,update_time) VALUES('1','tcp','abc',0,4,1,'abc','2022-02-25 11:12:50','2022-02-25 11:12:50');")
        # 查看常见端口库第一页第一条
        port = CommonPortLibrary()
        resp = port.send()
        result = json.loads(resp.text)
        print(result)
        id = result['data']['list'][0]['id']
        port_info = result['data']['list'][0]
        # print('port',port_info['port']== '1')
        # print('transportLayer',port_info['transportLayer'] == 'TCP')
        # print('serviceType',port_info['serviceType'] == 'abc')
        # print('highRisk',port_info['highRisk'] == 0)
        pytest.assume(
            port_info['port'] == '1' and port_info['transportLayer'] == 'TCP' and port_info['serviceType'] == 'abc' and
            port_info['highRisk'] == 0)  # 判断新增
        # 编辑端口
        mod = ModCommonPort()
        mod.json = {
            "id": id, "port": "2", "transportLayer": "udp", "serviceType": "abcd", "highRisk": 1, "remark": "abcd"
        }
        resp = mod.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200 and result['message'] == '端口修改成功')
        # 查看常见端口库修改后的第一页第一条
        port = CommonPortLibrary()
        resp = port.send()
        result = json.loads(resp.text)
        print(result)
        port_info = result['data']['list'][0]
        pytest.assume(
            port_info['port'] == '2' and port_info['transportLayer'] == 'UDP' and port_info['serviceType'] == 'abcd' and
            port_info['highRisk'] == 1)  # 判断修改后信息
        # 删除数据
        self.db.update("delete from  soc.soc_ports_library where port = 2 and is_custom = 1")

    @allure.story('ISA-3074')
    def test_equal_protection_knowledge(self):
        """
        ISA-3074 : 【新增等保知识库】新增菜单安全知识库/等保知识库描述
        1	查看“安全知识库”下的子菜单	看到了新增的子菜单“等保知识库”；
        2	查看面包屑导航	面包屑导航为“安全知识库>等保知识库”；
        3	点击选择“等保知识库”子菜单	页面显示等保一级知识库列表；
        4	查看列表项	列表项包括：检查范围、检查内容、检查项、等保级别、操作（查看）等；
        """
        equal = EqualProtectionKnowledgeBase()
        resp = equal.send()
        result = json.loads(resp.text)
        value = result['data']['list']  # 所有数据
        print(result)
        # inspectionScope 检查范围 inspectionContent 检查内容 inspectionItem 检查项 inspectionResults 等保级别
        pytest.assume(result['statusCode'] == 200)
        pytest.assume('inspectionScope' in value[0] and 'inspectionContent' in value[0] and 'inspectionItem' in value[
            0] and 'inspectionResults' in value[0])
        for i in value:
            # print(i['protectionLevel'])
            pytest.assume(i['protectionLevel'] == 1)  # 判断等保等级为1级

    @allure.story('ISA-3075')
    def test_asset_fingerprint_library(self):
        """
        ISA-3075 : 【新增资产指纹库】新增菜单安全知识库/资产指纹库描述
        1	查看“安全知识库”下的子菜单	看到了新增的子菜单“资产指纹库”；
        2	查看面包屑导航	面包屑导航为“安全知识库>资产指纹库”；
        3	点击选择“资产指纹库”子菜单	页面显示快速查询导航栏、资产指纹库列表、关键字查询框及旁边的“i”和刷新按钮；
        4	查看列表项	列表项包括：厂商（中文）、厂商（英文）、型号、传输层协议、服务、设备类型、涉及领域、操作（查看）；
        """
        # 快速查询接口
        search = AssetFingerprintQuickSearch()
        resp = search.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['failKeyEnum'] == 'SUCCESS')
        # 资产指纹库接口
        finger = AssetFingerprintLibrary()
        resp = finger.send()
        result = json.loads(resp.text)
        print(result)
        values = result['data']['values']  # 所有数据
        pytest.assume(result['statusCode'] == 200)
        # manufacturerCn 厂商（中文）、manufacturer_en 厂商（英文）、model 型号、transportLayer 传输层协议、serviceType 服务、equipmentType 设备类型、areasInvolved 涉及领域
        pytest.assume('manufacturerCn' in values[0] and 'manufacturer_en' in values[0] and 'model' in values[
            0] and 'transportLayer' in values[0] and 'serviceType' in values[0] and 'equipmentType' in values[
                          0] and 'areasInvolved' in values[0])

    @allure.story('ISA-3076')
    def test_vulnerability_library(self):
        """
        ISA-3076 : 【新增漏洞库】新增菜单安全知识库/漏洞库概述
        1 查看“安全知识库”下的子菜单	看到了新增的子菜单“漏洞库”；
        2 查看面包屑导航	面包屑导航为“安全知识库>漏洞库”；
        3 点击选择“漏洞库”子菜单	页面显示漏洞库列表；
        4 查看漏洞库页面	页面显示手动更新、自动更新、安检站配置、筛选按钮，关键字搜索框（i、刷新按钮）以及漏洞列表；
        5 查看列表项	列表项包括：漏洞名称、漏洞类型、危险级别、CVE编码、CNVD编码、CNNVD编码、发布时间、是否是工控漏洞、操作（详情）；
        """
        # 漏洞库展示
        resp = VulnerabilityLibrary().send()
        result = json.loads(resp.text)
        print(result)
        values = result['data']['values']
        pytest.assume(result['statusCode'] == 200)
        # 'vulName' 漏洞名称、'vulType' 漏洞类型、'riskLevel' 危险级别、'cve' CVE编码、'cnvd' CNVD编码、'cnnvd' CNNVD编码、'releaseTime' 发布时间、'riskLevelName' 是否是工控漏洞
        pytest.assume(
            'vulName' in values[0] and 'vulType' in values[0] and 'riskLevel' in values[0] and 'cve' in values[
                0] and 'cnvd' in values[0] and 'cnnvd' in values[0] and 'releaseTime' in values[
                0] and 'riskLevelName' in values[0])

    @allure.story('ISA-3077 ')
    def test_suggestion_library(self):
        """
        ISA-3077 : 【新增处置建议库】新增菜单安全知识库/处置建议库
        1	查看“安全知识库”下的子菜单	看到了新增的子菜单“处置建议库”；
        2	查看面包屑导航	面包屑导航为“安全知识库>处置建议库”
        3	点击选择“处置建议库”子菜单	页面显示处置建议库列表；
        4	查看列表项	列表项包括：“告警类型”、“处置建议”、“操作(编辑、删除)”；
        """
        # 处置建议库
        resp = SuggestionLibrary().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        data = result['data']['data'][0]
        # alarmTypeCn 告警类型、content 处置建议
        pytest.assume('alarmTypeCn' in data and 'content' in data)

    # todo 3079页面操作查看 暂不做自动化
    @allure.story('ISA-3079、3125')
    def test_cpu_tab_page(self):
        """
        ISA-3079 : 【计划自动化】【CPU占有率】新增CPU占有率tab页
        1	查看页面最右侧	新增设备状态统计tab页，显示为流量、CPU、内存，鼠标悬浮显示为小手；
        2	点击“CPU”tab选项	可以成功切换到“CPU”tab页； 可以选择切换显示“实时占有率”和“历史占有率”；
        ISA-3125 : 【计划自动化】【对内存绘制占有率曲线】 内存占有率标签的显示
        1	在指针变为小手指示标志时，点击“内存”标签	下方展示两个标签为"实时占有率"与历史占有率，
        2	查看实时占有率标签	占有率为曲线，实时占有率横轴是时间时分秒，纵轴是占有率
        3	1.在“内存占有率”标签页中点击“历史占有率”标签 2.查看历史占有率标签	历史占有率横轴是月日，纵轴是当前日期平均值
        4	滚动鼠标滚轮	可以切换横坐标时间范围
        """
        # 运行监视页面获取 mac，传到cpu接口
        resp = RunMonitoringPage().send()
        result = resp.json()
        print(result)
        data = result['data']

        key_list = []
        for i in data.keys():
            key_list.append(i)
        ethmac =key_list[0].split('r')[1]

        #  实时cpu
        real = RealTimeCpu()
        real.url = host + '/sysmonitor/realTimeCpu?clientId={}'.format(ethmac)
        resp = real.send()

        result = resp.json()
        print(result)
        series = result['data']['series']
        xAxis = result['data']['xAxis']
        print(series)
        print(xAxis)
        value = re.findall("\d{2}[:]\d{2}[:]\d{2}", xAxis[0])  # 正则表达式满足HH:MM:SS
        print(value)  # ['10:30:49']
        pytest.assume(value[0] == xAxis[0])
        pytest.assume(0 <= float(series[0]) <= 100)  # y轴cpu百分比 大于等于0 小于等于100
        # 时间和数据长度不为0 且 时间和数据的长度相同
        pytest.assume(len(series) != 0 and len(series) == len(xAxis))
        #  历史cpu
        resp = HistoryTimeCpu().send()
        result = resp.json()
        series = result['data']['series']
        xAxis = result['data']['xAxis']
        print(series)
        print(xAxis)
        result = re.findall("\d{4}[-]\d{2}[-]\d{2}", xAxis[0])
        pytest.assume(result[0] == xAxis[0])
        pytest.assume(0 <= float(series[0]) <= 100)  # y轴cpu百分比 大于等于0 小于等于100
        # 时间和数据长度不为0 且 时间和数据的长度相同
        pytest.assume(len(series) == len(xAxis))

    @allure.story('ISA-3087')
    def test_safety_notice(self):
        """
        ISA-3087 : 【新增安全通告】新增菜单监控中心/大屏管理/安全通告概述
        1	查看大屏管理下的子菜单	看到了新增的子菜单“安全通告”；
        2	查看面包屑导航	面包屑导航为“监控中心>大屏管理>安全通告”；
        3	点击“安全通告”子菜单	页面显示安全通告列表；
        4	查看安全通告页面上的列表项	看到的列表项为：标题、漏洞编号、影响的操作系统、启用状态、描述信息、操作（编辑、删除）；
        """
        # 添加安全通告，添加后可显示"标题、漏洞编号等信息"
        add = AddSafetyNotice()
        resp = add.send()
        # print(resp)
        result = json.loads(resp.text)
        pytest.assume(result['statusCode'] == 200)
        # 安全通告页面
        safe = SafetyNotice()
        resp = safe.send()
        result = json.loads(resp.text)
        data = result['data']['data'][0]
        id = data['id']  # 删除接口需要调用
        # title 标题、cveCode 漏洞编号、 operatingSystem 影响的操作系统、enable 启用状态、description 描述信息
        pytest.assume(
            'title' in data and 'cveCode' in data and 'operatingSystem' in data and 'enable' in data and 'description' in data)
        # 删除安全通告
        detele = DeleteSafetyNotice()
        detele.json = {"ids": [id]}
        resp = detele.send()
        result = json.loads(resp.text)
        pytest.assume(result['statusCode'] == 200)

    @allure.story('ISA-3120')
    def test_add_schedule(self):
        """
        ISA-3120 : 【新增值班表】点击“新增值班表”页面“确定”按钮，通过内容校验，新增值班表数据
        1	页面填入不合规内容，点击“确定”按钮	不合规内容在输入框下有提示信息
        2	页面填入合规内容，点击“确定”按钮，查看值班列表	1.提示“操作成功” 2.新增一条值班表数据
        3	使用audit用户登录系统，查看系统操作日志	该操作记录系统操作日志
        """
        # 新增不合规值班表
        attendance = AddAttendanceMangagement()
        attendance.json = {"workDutyName": "test", "todayAlarmCount": "6", "noProcessCount": "7",
                           "todayProcessCount": "2",
                           "assetCount": "3", "normalAssetCount": "-1", "abnormalAssetCount": "2",
                           "dangerAssetCount": "1",
                           "offlineAssetCount": "8", "unknownAssetCount": "3", "remnantWorkSituation": "",
                           "completedWork": "", "noCompletedWork": "", "workSummary": ""}
        resp = attendance.send()
        result = json.loads(resp.text)
        print('message', result)
        pytest.assume(result['message'] == 'normalAssetCount需要在0和200000之间')
        # 新增合规值班表
        resp = AddAttendanceMangagement().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        # audit 该操作记录系统操作日志
        header = login_test(audit, password)
        operator_log = OperatorLog()
        operator_log.headers = header
        resp = operator_log.send()
        result = json.loads(resp.text)
        print('audit', result)
        context = result['data']['list'][0]['context']  # 增加值班表：test成功
        context1 = result['data']['list'][1]['context']  # 增加值班表：test成功
        pytest.assume(context == '增加值班表[test]成功' or context1 == '增加值班表[test]成功')
        # 查看值班管理
        resp = AttendanceMangagement().send()
        result = json.loads(resp.text)
        id = result['data']['list'][0]['id']  # 删除接口使用id
        time.sleep(3)
        # 删除值班表
        delete = DeleteAttendanceMangagement()
        delete.json = {"ids": [id]}
        resp = delete.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)

    # todo ISA-3121 : 后台接口无返回图片，通过前台直接返回
    # def test_export_attendance_schedule(self):
    #     resp = ExportAttendanceSchedule().send()
    #     img = resp.content
    #     print(ImportAttendanceSchedule().url)
    #     result = json.loads(resp.text)
    # with open(img, 'wb') as f:

    @allure.story('ISA-3123')
    def test_delete_attendance_schedule(self):
        """
        ISA-3123 : 【修改值班表与删除值班表】任选一条“值班表”进行修改操作
        1	任选一条值班表，点击"编辑"按钮	进入“编辑值班表”页面
        2	修改该“值班表”内容，修改后的内容不合规，点击页面下方“确定”按钮	修改不合规内容的下方出现红字提示
        3	修改该“值班表”内容，修改后的内容合规，点击页面下方“确定”按钮	提示“操作成功”
        4	查看刚刚修改的值班表内容	内容被修改
        5	使用audit用户登陆系统，查看系统操作日志	修改值班表操作被记录
        6 在值班表列表任选一条值班表数据，点击"删除"操作  有弹窗提示：”是否确认删除“
        7 在弹窗内点击”确认“按钮 提示”  操作成功“
        8 在值班列表中查看该值班表  该值班表在值班列表中被删除
        9 使用audit用户登陆系统，查看系统操作日志  删除值班表操作被记录
        """
        # 新增值班表
        resp = AddAttendanceMangagement().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        # 查看值班管理
        resp = AttendanceMangagement().send()
        result = json.loads(resp.text)
        id = result['data']['list'][0]['id']  # 删除接口使用id
        # 修改值班表不合规
        mod = ModAttendanceMangagement()
        mod.json = {"workDutyName": "test", "todayAlarmCount": "-1", "noProcessCount": 7, "todayProcessCount": 2,
                    "assetCount": 3, "normalAssetCount": 7, "abnormalAssetCount": 2, "dangerAssetCount": 1,
                    "offlineAssetCount": 1, "unknownAssetCount": 3, "remnantWorkSituation": "", "completedWork": "",
                    "noCompletedWork": "", "workSummary": "", "id": id}
        resp = mod.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['message'] == 'todayAlarmCount需要在0和10000000000之间')
        # 修改值班表合规
        mod = ModAttendanceMangagement()
        mod.json = {"workDutyName": "test", "todayAlarmCount": "50", "noProcessCount": 7, "todayProcessCount": 2,
                    "assetCount": 3, "normalAssetCount": 7, "abnormalAssetCount": 2, "dangerAssetCount": 1,
                    "offlineAssetCount": 1, "unknownAssetCount": 3, "remnantWorkSituation": "", "completedWork": "",
                    "noCompletedWork": "", "workSummary": "", "id": id}
        resp = mod.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        # 查看值班管理
        resp = AttendanceMangagement().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['data']['list'][0]['todayAlarmCount'] == 50)  # 判断修改的内容
        time.sleep(1)
        # audit 该操作记录系统操作日志
        header = login_test(audit, password)
        operator_log = OperatorLog()
        operator_log.headers = header
        resp = operator_log.send()
        result = json.loads(resp.text)
        print('audit', result)
        context = result['data']['list'][0]['context']  # 修改值班表：test成功
        context1 = result['data']['list'][1]['context']  # 修改值班表：test成功
        pytest.assume(context == '修改值班表[test]成功' or context1 == '修改值班表[test]成功')
        # 删除值班表
        delete = DeleteAttendanceMangagement()
        delete.json = {"ids": [id]}
        resp = delete.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        # 查看查看值班管理
        resp = AttendanceMangagement().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['data']['total'] == 0)  # 删除后总数为0
        # audit 该操作记录系统操作日志
        header = login_test(audit, password)
        operator_log = OperatorLog()
        operator_log.headers = header
        resp = operator_log.send()
        result = json.loads(resp.text)
        print('audit', result)
        context = result['data']['list'][0]['context']  # 删除值班表：test成功
        context1 = result['data']['list'][1]['context']  # 删除值班表：test成功
        pytest.assume(context == '删除值班表[test]成功' or context1 == '删除值班表[test]成功')

    # todo 3125 cpu相关曲线的显示 暂时不做自动化

    @allure.story('ISA-3126')
    def test_lateral_threat_posture(self):
        """
        ISA-3126 : 【横向威胁态势】页面顶部显示资产数、正常，异常访问连接数、非法外联数等数量按钮，点击可跳转到对应页面
        1	页面顶部展示四个新增按钮	依次为“已确认资产数、正常横向访问连接数、异常横向访问连接数、非法外联数”按钮
        2	点击“已确认资产数”按钮,	页面跳转至平台的【已确认资产】页面，页面中已确认资产数量和大屏<已确认资产数>按钮上的数量一致
        3	点击“正常横向访问连接数”按钮	1.页面跳转至【逻辑拓扑】页面 2.页面展示的逻辑拓扑信息个数和大屏中按钮上的数据一致
        4	点击“异常横向访问连接数”按钮	1.页面跳转至【逻辑拓扑】页面 2.页面展示的逻辑拓扑信息个数和大屏中按钮上的数据一致
        5	点击“非法外联数量”按钮	1.页面跳转至【告警检索】页面 2.该页面中只展示类型为“非法外联”的告警信息 3.该页面中展示的告警信息条数和大屏中按钮上的数据一致
        """

        # 横向威胁态势四个按钮
        resp = ThreatTransverse().send()
        result = json.loads(resp.text)
        print(result)
        data = result['data']
        assetCount = data['assetCount']  # 已确认资产数
        normalConn = data['normalConn']  # 正常横向访问连接数
        abnormalConn = data['abnormalConn']  # 异常横向访问连接数
        unknownConn = data['unknownConn']  # 非法外联数
        # assetCount 已确认资产数、'normalConn' 正常横向访问连接数、 'abnormalConn' 异常横向访问连接数、 'unknownConn' 非法外联数
        pytest.assume(
            'assetCount' in data and 'normalConn' in data and 'abnormalConn' in data and 'unknownConn' in data)
        # 已确认资产列表
        resp = RecognizedAssetsList().send()
        result = json.loads(resp.text)
        pytest.assume(result['data']['total'] == assetCount)  # 判断已确认资产数一致
        # 正常逻辑拓扑数
        resp = LogicTopo().send()
        result = json.loads(resp.text)
        pytest.assume(result['data']['total'] == normalConn)  # 判断正常横向访问连接数一致
        # 异常逻辑拓扑数
        topo = LogicTopo()
        topo.json = {"pageSize": 10, "startPage": 1, "ip": "", "factoryId": 2, "status": "", "exceptOk": 'true'}
        resp = topo.send()
        result = json.loads(resp.text)
        pytest.assume(result['data']['total'] == abnormalConn)  # 判断异常横向访问连接数一致
        # 告警检索页面
        alarm = AlarmRetrieval()
        alarm.json = {"keyword": "", "factory": 2, "alarmType": 30000100, "alarmTypeArr": [30000000, 30000100],
                      "alarm_filter": 'true', "actionStatus": '', "startPage": 1, "pageSize": 10}
        resp = alarm.send()
        result = json.loads(resp.text)
        pytest.assume(result['data']['total'] == unknownConn)  # 判断非法外联数一致

    # @allure.story('ISA-3128')  # 运行态势五个按钮
    # def test_operational_situation(self):
    #     """
    #     ISA-3128 : 【快速查询按钮】 运行态势大屏页，新增多个快速查询按钮
    #     1	运行态势大屏页顶部新增6个快速查询按钮	1.设备类型为“网络设备、安全设备、主机设备、工控设备、物联网设备、其他设备” 2.快速查询按钮，根据数值大小，依次从左到右显示
    #     2	点击“网络设备”	1.页面筛选出所有的类型为“网络设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
    #     3	点击“安全设备”	1.页面筛选出所有的类型为“安全设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
    #     4	点击“主机设备”	1.页面筛选出所有的类型为“主机设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
    #     5	点击“工控设备”	1.页面筛选出所有的类型为“工控设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
    #     6	点击“物联网设备”	1.页面筛选出所有的类型为“物联网设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
    #     7	点击“其他设备”	1.页面筛选出所有的类型为“其他设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
    #     """
    #     #  运行态势五个按钮
    #     resp = OperationalSituation().send()
    #     result = json.loads(resp.text)
    #     print(result)
    #     data = result['data']
    #     offLine = data['offLine']  # 离线
    #     normal = data['normal']  # 正常
    #     abnormal = data['abnormal']  # 异常
    #     danger = data['danger']  # 危险
    #     unknown = data['unknown']  # 未知
    #     # offLine 离线、 normal 正常、 abnormal 异常、 danger 危险、 unknown 未知
    #     pytest.assume(
    #         'offLine' in data and 'normal' in data and 'abnormal' in data and 'danger' in data and 'unknown' in data)
    #     # 未知
    #     asset = RecognizedAssetsList()
    #     asset.json = {"routeName": "runningPosture", "factoryId": 2, "isOnline": 2, "pageSize": 10, "startPage": 1,
    #                   "keyword": ""}
    #     resp = asset.send()
    #     result = json.loads(resp.text)
    #     pytest.assume(result['data']['total'] == unknown)
    #     # 离线
    #     asset = RecognizedAssetsList()
    #     asset.json = {"routeName": "runningPosture", "factoryId": 2, "isOnline": 0, "pageSize": 10, "startPage": 1,
    #                   "keyword": ""}
    #     resp = asset.send()
    #     result = json.loads(resp.text)
    #     pytest.assume(result['data']['total'] == offLine)
    #     # 正常
    #     asset = RecognizedAssetsList()
    #     asset.json = {"routeName": "runningPosture", "factoryId": 2, "isOnline": 1, "pageSize": 10, "startPage": 1,
    #                   "keyword": ""}
    #     resp = asset.send()
    #     result = json.loads(resp.text)
    #     pytest.assume(result['data']['total'] == normal)
    #     # 异常
    #     asset = RecognizedAssetsList()
    #     asset.json = {"routeName": "runningPosture", "factoryId": 2, "isOnline": 3, "pageSize": 10, "startPage": 1,
    #                   "keyword": ""}
    #     resp = asset.send()
    #     result = json.loads(resp.text)
    #     pytest.assume(result['data']['total'] == abnormal)
    #     # 危险
    #     asset = RecognizedAssetsList()
    #     asset.json = {"routeName": "runningPosture", "factoryId": 2, "isOnline": 4, "pageSize": 10, "startPage": 1,
    #                   "keyword": ""}
    #     resp = asset.send()
    #     result = json.loads(resp.text)
    #     pytest.assume(result['data']['total'] == danger)

    @allure.story('ISA-3128')
    def test_operational_situation(self):
        """
        ISA-3128 : 【快速查询按钮】 运行态势大屏页，新增多个快速查询按钮
        1	运行态势大屏页顶部新增6个快速查询按钮	1.设备类型为“网络设备、安全设备、主机设备、工控设备、物联网设备、其他设备” 2.快速查询按钮，根据数值大小，依次从左到右显示
        2	点击“网络设备”	1.页面筛选出所有的类型为“网络设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
        3	点击“安全设备”	1.页面筛选出所有的类型为“安全设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
        4	点击“主机设备”	1.页面筛选出所有的类型为“主机设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
        5	点击“工控设备”	1.页面筛选出所有的类型为“工控设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
        6	点击“物联网设备”	1.页面筛选出所有的类型为“物联网设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
        7	点击“其他设备”	1.页面筛选出所有的类型为“其他设备”的资产 2.筛选后页面展示的设备数量和按钮上显示的数值一致
        """
        # 运行态势6个快速查询
        resp = OperationalSituationQuickSearh().send()
        result = json.loads(resp.text)
        data = result['data']
        asset_list = []  # 列表存放6个快速查询名称
        num_list = []  # 列表存放6个快速查询数值
        for i in data:
            asset_list.append(i['assetTypeCn'])
            num_list.append(i['totalCount'])
        for i in asset_list:
            pytest.assume(i in ['其他设备', '安全设备', '网络设备', '主机设备', '工控设备', '物联网设备'])
        # pytest.assume(
        #     '其他设备' in asset_list and '安全设备' in asset_list and '网络设备' in asset_list and '主机设备' in asset_list and '工控设备' in asset_list and '物联网设备' in asset_list)
        # 快速查询页
        for i in range(len(asset_list)):
            quick = QuickSearhPage()
            quick.json = {"factoryId": 2, "startPage": 1, "pageSize": 50, "isOnline": "", "assetTypeCn": asset_list[i]}
            resp = quick.send()
            result = json.loads(resp.text)
            print(result['data']['total'], num_list[i] and num_list[i] != 0)
            pytest.assume(result['data']['total'] == num_list[i] and num_list[i] != 0)

    # todo 3127、3149、3151 不做自动化
    @allure.story('ISA-3131')
    def test_asset_add_status(self):
        """
        ISA-3131 : 【计划自动化】【资产画像新增运行状态】CPU利用率、内存利用率、磁盘利用率的数据和实际设备上的数据一致
        1	远程连接该设备，使用top命令，计算出CPU的利用率	数值和页面CPU利用率显示的数值相等
        2	输入“free”命令，查看内存数据，算出used/total的值，得出内存利用率	数值和页面内存利用率显示的数值相等
        3	输入“df -h”命令，计算出磁盘利用率的值	数值和页面磁盘利用率显示的数值相等
        """
        # 模拟usm同步资产
        syslog(
            '100103|^Firewall210127007|^192.168.100.164|^|^低|^202004|^未知|^|^WOS|^0|^无|^2022-03-15 17:22:06.0|^默认区域|^2|^')
        time.sleep(15)
        # 发送192.168.100.164资产的cpu、内存、硬盘值
        syslog('1006|^210127007|^192.168.100.164|^1|^1|^40.92|^58.62|^25.35|^45.0|^1|^1|^')
        time.sleep(120)
        # 查看已确认资产列表
        resp = RecognizedAssetsList().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        list = result['data']['list']  # 资产生命周期总数
        # asset_id = ''
        id = ''
        print(list)
        print(len(list))
        for i in range(len(list)):
            print(list[i]['ip'])
            if list[i]['ip'] == '192.168.100.164':
                id = list[i]['id']
        # 查看资产画像中的cpu、内存、硬盘值
        portrait = AssetPortrait()
        portrait.url = host + '/assets/situations/base?assetId={}'.format(id)

        resp = portrait.send()
        result = json.loads(resp.text)
        print(result)
        cpu = result['data']['cpuUsage']
        memory = result['data']['memoryUsage']
        hardDist = result['data']['hardDistUsage']
        print(cpu, memory, hardDist)
        pytest.assume(float(cpu) == 40.92 and float(memory) == 58.62 and float(hardDist) == 25.35)
        pytest.assume(result['statusCode'] == 200)
        # 删除资产
        delete = DeleteAsset()
        print(id)
        delete.json = {"ids": [id]}
        resp = delete.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '操作成功')

    @allure.story('ISA-3492')
    def test_import_vulnerability_scan(self):
        """
        ISA-3492 : 【漏洞以导入的漏扫报告为准】导入漏扫报告后，涉及到的资产的漏洞以报告 为准，已匹配的漏洞会自动进行删除
        1	1.点击<新增资产>按钮，输入添加的资产 ip：192.168.4.193，操作系统：microsoft windows server 2008 sp2 2.其他参数合规，点击<确定>按钮	【漏洞记录】页面，该资产匹配对应的漏洞信息
        2	【已确认资产】页面，点击<导入数据>，“上传类型”选择“工控漏洞扫描”，选择相同区域下，192.168.4.193资产的漏扫文件	【漏洞记录】页面，只显示漏扫文件中的漏洞，其他已存在的漏洞信息会自动进行删除
        3	进入192.168.4.193的资产画像页面，	该页面显示最新的漏洞信息，和【漏洞记录】页面显示的该资产的漏洞信息保持一致
        4	关闭“匹配漏洞开关”按钮，重复步骤1,2,3	和步骤2,3的预期结果一致
        """
        # admin打开 匹配漏洞开关
        header = login_test(admin, password)
        config = VulnerabilityConfiguration()
        config.headers = header
        resp = config.send()
        result = json.loads(resp.text)
        print('admin', result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '操作成功')
        # 新增资产
        add = AddAsset()
        add.json = {"ip": "192.168.0.202", "name": "192.168.0.202", "modelId": "", "factoryId": 3, "mac": "",
                    "alias": "", "serialNumber": "", "deviceVersion": "", "hasGuard": "",
                    "operateSystem": "Linux Kernel 2.6", "ipMacs": [], "typeId": "", "vendorId": "",
                    "belongingUnit": "", "belongProfessiona": "", "belongingSystem": "", "hostName": "",
                    "physicalPortNumber": "", "loginTime": "", "assetBusinessValue": "3", "assetConfidentiality": "",
                    "assetIntegrity": "", "assetAvailability": "", "safetyResponsiblePerson": "", "values": []}
        resp = add.send()
        result = resp.json()
        print(result)
        id = result['data']['id']
        pytest.assume(result['message'] == '操作成功')
        # time.sleep(2)
        # 查看漏洞记录
        record = VulnerabilityRecord()
        resp = record.send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['data']['total'] == 1)  # 仅一条

        # 导入漏扫报告
        resp = ImportAsset().send()
        result = resp.json()
        print(result)
        # time.sleep(3)
        pytest.assume(result['message'] == '文件导入成功!')

        # 查看漏洞记录
        record = VulnerabilityRecord()
        resp = record.send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['data']['total'] == 2)  # 变为两条
        # 资产画像
        asset_vul = AssetPortraitVuls()
        asset_vul.json = {"startPage": 1, "pageSize": 5, "assetId": id}
        resp = asset_vul.send()
        result = resp.json()
        print(result)
        pytest.assume(result['data']['total'] == 2)
        # 关闭漏洞开关
        config.json = {"match": 0}
        resp = config.send()
        result = resp.json()
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '操作成功')
        # 关闭开关后执行2、3
        # 导入漏扫报告
        resp = ImportAsset().send()
        result = resp.json()
        print(result)
        # time.sleep(3)
        pytest.assume(result['message'] == '文件导入成功!')
        # 查看漏洞记录
        record = VulnerabilityRecord()
        resp = record.send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['data']['total'] == 2)  # 变为两条
        # 资产画像
        asset_vul = AssetPortraitVuls()
        asset_vul.json = {"startPage": 1, "pageSize": 5, "assetId": id}
        resp = asset_vul.send()
        result = resp.json()
        print(result)
        pytest.assume(result['data']['total'] == 2)
        # 删除资产
        delete = DeleteAsset()
        delete.json = {"ids": [id]}
        resp = delete.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '操作成功')

    @allure.story('ISA-3207')
    def test_statistical_classification(self):
        """
        ISA-3207 : 【新增报表】新增报表时统计分类的选择
        1	点击“新增报表”按钮	出现“新增报表”弹窗；
        2	查看“统计分类”选择框	按照章节展示，章节包括：资产、资产脆弱性、告警、安全事件、安全合规； 章节下还包括具体的统计图表； 章节及章节下的图表内容默认展开；
        3	点击全选按钮	成功选到了所有章节；
        4	选择任意一个统计图表	成功选中了图表； 图表所在的章节也被选中；
        5	不选择统计分类，其他项合规	提示“请选择系统分类”；
        """
        # 统计分类详情
        resp = ReportManageChapter().send()
        result = json.loads(resp.text)
        print(result)
        label = []
        print(result['data'])
        for i in range(len(result['data'])):
            label.append(result['data'][i]['label'])
            for s in range(len(result['data'][i]['children'])):
                label.append(result['data'][i]['children'][s]['label'])
        print(label)
        pytest.assume(
            label == ['资产', '资产区域分布', '资产风险指数TOP10', '资产漏洞数量TOP10', '资产的设备类型分布', '资产的设备厂商分布', '资产活跃度统计', '资产脆弱性',
                      '漏洞区域分布', '漏洞级别分布', '漏洞类型TOP10', '漏洞的设备类型TOP10', '漏洞列举TOP100', '漏洞的设备厂商TOP10', '告警', '告警区域分布',
                      '告警级别分布', '告警异常统计TOP10', '告警类型统计TOP10', '告警攻击链统计', '未处理告警TOP100', '安全事件', '事件趋势分析', '事件类型统计TOP10',
                      '安全事件排名TOP100', '安全事件区域分布', '安全合规', '主机合规级别分布', '不合规主机TOP10'])
        # 新增统计报表成功
        add = AddInstantReport()
        resp = add.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '您的任务已下发，请在报表管理-即时报表中下载')
        # 即时报表列表查询id
        resp = InstantReportList().send()
        result = json.loads(resp.text)
        id = result['data']['list'][0]['reportId']
        # 新增统计报表失败
        # add = AddInstantReport()  #todo 接口的处理方式于实际页面不同
        # add.json = {"statsType": 0, "reportName": "test", "reportType": 1, "factoryId": 3, "isEmail": 0,
        #              "receiveId": "", "reportDesc": "", "fileType": 0,
        #              "statsContent": "",
        #              "year": "2022", "month": "3"}
        # resp = add.send()
        # result = json.loads(resp.text)
        # print(result)
        # 删除报表
        delete = DeleteInstantReport()
        delete.json = [id]
        resp = delete.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)

    # todo 3152、3156\3159\3161逻辑拓扑暂时不做自动化
    # todo  3157 主机卫士资产同步失败

    @allure.story('ISA-3157')
    def test_usm_send_asset(self):
        """
        ISA-3157 :【由USM上报的主机卫士、监测审计资产，不允许修改区域 】USM syslog上报的主机卫士、监测审计资产，是不允许修改资产
        1	1. 进入“资产中心-资产管理-已确认资产”页面 2. 勾选通过USM syslog上报的主机卫士资产 3. 点击上方“修改资产”的按钮	厂区的修改位置无法修改
        2	勾选通过USM syslog上报的工业防火墙资产	厂区的修改位置无法修改
        3	勾选通过USM syslog上报的监测审计资产	厂区的修改位置无法修改
        """
        # 模拟usm同步资产
        syslog('100103|^Firewall210127007|^192.168.100.164|^|^低|^202004|^未知|^|^WOS|^0|^无|^2022-03-15 17:22:06.0|^默认区域|^2|^')  # 防火墙
        syslog('100103|^Probe201229002|^192.168.4.67|^|^无|^202007|^未知|^|^WOS|^0|^无|^2022-03-15 16:28:13.0|^默认区域|^2|^')  # 审计检测
        syslog('100103|^hostguardian|^192.168.20.137|^00:0C:29:A6:02:01|^中|^302099|^未知|^|^Microsoft Windows Server 2012 R2 Datacenter 6.3.9600 N/A Build 9600|^1|^有|^2022-03-15 16:21:21.0|^默认区域|^2|^')  # 主机卫士
        time.sleep(40)
        # 由于就一个区域，新增一个区域
        resp = AddAera().send()
        result = resp.json()
        print(result)
        #  查询 区域，删除接口调用id
        resp = AeraQuery().send()
        result = resp.json()
        print(result)
        value = result['data'][0]['children'][1]['value'] # 区域 厂区
        # 查看已确认资产列表
        resp = RecognizedAssetsList().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        list = result['data']['list']  # 资产生命周期总数
        fire_id = ''  # 防火墙id
        probe_id = ''  # 审计检测id
        host_id = ''  # 主机卫士id
        print(list)
        print(len(list))
        for i in range(len(list)):
            print(list[i]['ip'])
            if list[i]['ip'] == '192.168.100.164':
                fire_id = list[i]['id']
            if list[i]['ip'] == '192.168.4.67':
                probe_id = list[i]['id']
            if list[i]['ip'] == '192.168.20.137':
                host_id = list[i]['id']
        # 修改资产防火墙 区域
        mod = ModAsset()
        mod.json = {"id": fire_id, "ip": "192.168.100.164", "name": "Firewall210127007", "modelId": '', "factoryId": value,
                    "mac": '', "alias": '', "serialNumber": '', "deviceVersion": "unknown", "hasGuard": 0,
                    "operateSystem": "WOS", "ipMacs": [], "typeId": "", "vendorId": "", "belongingUnit": '',
                    "belongProfessiona": '', "belongingSystem": '', "hostName": '', "physicalPortNumber": '',
                    "loginTime": '', "assetBusinessValue": 3, "assetConfidentiality": '', "assetIntegrity": '',
                    "assetAvailability": '', "safetyResponsiblePerson": '', "values": []}
        resp = mod.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '资产：Firewall210127007由USM上报，不允许修改区域')
        # 修改资产审计检测 区域
        mod.json = {"id": probe_id, "ip": "192.168.4.67", "name": "Firewall210127007", "modelId": '', "factoryId": value,
                    "mac": '', "alias": '', "serialNumber": '', "deviceVersion": "unknown", "hasGuard": 0,
                    "operateSystem": "WOS", "ipMacs": [], "typeId": "", "vendorId": "", "belongingUnit": '',
                    "belongProfessiona": '', "belongingSystem": '', "hostName": '', "physicalPortNumber": '',
                    "loginTime": '', "assetBusinessValue": 3, "assetConfidentiality": '', "assetIntegrity": '',
                    "assetAvailability": '', "safetyResponsiblePerson": '', "values": []}
        resp = mod.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '资产：Probe201229002由USM上报，不允许修改区域')
        # 修改资产主机卫士 区域
        mod.json = {"id": host_id, "ip": "192.168.20.137", "name": "hostguardian", "modelId": '', "factoryId": value,
                    "mac": '', "alias": '', "serialNumber": '', "deviceVersion": "unknown", "hasGuard": 0,
                    "operateSystem": "WOS", "ipMacs": [], "typeId": "", "vendorId": "", "belongingUnit": '',
                    "belongProfessiona": '', "belongingSystem": '', "hostName": '', "physicalPortNumber": '',
                    "loginTime": '', "assetBusinessValue": 3, "assetConfidentiality": '', "assetIntegrity": '',
                    "assetAvailability": '', "safetyResponsiblePerson": '', "values": []}
        resp = mod.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '资产：hostguardian由USM上报，不允许修改区域')

        # 删除区域
        delete = DeleteAera()
        delete.json = {"ids": [value]}
        resp = delete.send()
        result = resp.json()
        pytest.assume(result['message'] == '操作成功')

        # 删除资产
        delete = DeleteAsset()
        print(fire_id, probe_id, host_id)
        delete.json = {"ids": [fire_id, probe_id, host_id]}
        resp = delete.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '操作成功')

    @allure.story('ISA-3162')
    def test_ip_analys(self):
        """
        ISA-3162 : 【威胁情报-安全分析页面】 ”安全分析“页面，进行IP分析功能
        1	输入IP"27.128.201.88",点击"放大镜"按钮，查看安全分析列表。	显示该IP的相关信息
        2	多次输入该IP进行分析	每次分析的数据结果显示相同
        """
        # 多次安全分析查询结果一致
        secure = SecurityAnalysisQuery()
        for i in range(3):
            resp = secure.send()
            result = json.loads(resp.text)
            print(result)
            pytest.assume(result['data']['total'] == 1)
            pytest.assume(result['data']['list'][0]['type'] == 'IP威胁库')
            pytest.assume(result['data']['list'][0]['value'] == '27.128.201.88')
            pytest.assume(result['data']['list'][0]['sourceRef'] == 'Emergingthreats,ThreatWeb')
            pytest.assume(result['data']['list'][0]['category'] == '扫描器节点,僵尸网络')

    # todo 3164 在线更新威胁情报库无法做自动化
    @allure.story('ISA-3164')
    def test_update_threat_intelligence(self):
        """
        ISA-3164 : 【情报更新】使用文件或联网进行威胁情报离线更新
        1	在"更新情报"页面，点击"点击上传"按钮，在弹出的文件选择框中，选择要导入的文件，点击确定。	上传按钮右侧显示“更新中”小图标，同时页面按钮都置灰不可点击。
        2 导入成功后	"点击上传"按钮右侧的状态变为"更新完毕"页面按钮恢复
        3 查看下方的更新记录列表	显示最新的更新记录。
        4 使用audit用户登陆系统，查看操作日志	 离线更新威胁情报库操作已被记录
        5 在"更新情报"页面，点击"点击上传"按钮，在弹出的文件选择框中，选择要导入的文件，点击确定  上传按钮右侧显示“更新中”小图标，同时页面按钮都置灰不可点击。
        6 导入成功后   "点击上传"按钮右侧的状态变为"更新完毕"页面按钮恢复
        7 查看下方的更新记录列表  显示最新的更新记录
        8 使用audit用户登陆系统，查看操作日志  离线更新威胁情报库操作已被记录
        """
        linux = Linux()
        linux.remoteConnect(IP, linux_port, linux_user, linux_pass)
        # select_result = linux.exec_command('ls /usr/local/soc/upgrade/cert/')  # 查询服务器此路径下是否存在alpha.pem文件
        local_path = DIR_NAME + '/data/uploadfile'
        remote_path = '/usr/local/soc/upgrade/cert/'
        local_file_path = os.path.join(local_path, 'alpha.pem')
        remote_file_path = os.path.join(remote_path, 'alpha.pem')
        linux.upload(local_file_path, remote_file_path)  # 讲alpha.pem文件放到指定目录下
        self.db.update(
            "UPDATE `soc`.`soc_system_config` SET `sys_value`='1' WHERE  `sys_key`='knowledge_threat_version';")  # 数据库修改威胁情报值，修改后可导入
        # 查询情报更新页存在条数
        resp = IntelligenceUpdatePage().send()
        result = resp.json()
        total_before = result['data']['total']  # 更新前条数
        print(total_before)
        # 更新安全情报
        resp = IntelligenceUpload().send()
        result = resp.json()
        pytest.assume(result['statusCode'] == 200)
        # 查询情报更新页存在条数
        resp = IntelligenceUpdatePage().send()
        result = resp.json()
        total_after = result['data']['total']  # 更新后条数
        print(total_after)
        pytest.assume(int(total_after) - int(total_before) == 1)
        # audit 查看操作日志
        header = login_test(audit, password)
        operator_log = OperatorLog()
        operator_log.headers = header
        resp = operator_log.send()
        result = json.loads(resp.text)
        print(result)
        log_list = result['data']['list']
        context_list = []
        for i in log_list:
            print(i['context'])
            context_list.append(i['context'])
        pytest.assume('离线更新威胁情报库(更新文件[THREAT_20220230.WNT]，[527262]条)成功' in context_list[:3])  # 判断audit前三条新增成功

    @allure.story('ISA-3165')
    def test_alarm_overview_show(self):
        """
        ISA-3165 : 【告警详情页面展示威胁情报】威胁情报标签中，内容展示
        1	在告警列表任选一个告警信息，点击操作中的“详情”操作	进入"告警详情"页面
        2	点击”威胁情报“标签	进入”威胁情报”标签
        3	查看威胁情报标签内容	显示内容包括：威胁值，地理位置（国家-省-市）威胁分类，威胁标签，威胁来源。
        4	如果有多个IP需要展示威胁情报	显示为：
        威胁值：（受影响ip地址）
        地理位置：（受影响IP所在的国家-省-市）
        威胁分类：（受影响IP的威胁分类）
        威胁标签：（受影响IP的威胁标签）
        威胁来源：（受影响IP的威胁来源）
        威胁值：（源ip地址）
        地理位置：（源IP所在的国家-省-市）
        威胁分类：（源IP的威胁分类）
        威胁标签：（源IP的威胁标签）
        威胁来源：（源IP的威胁来源）
        威胁值：（目的ip地址）
        地理位置：（目的IP所在的国家-省-市）
        威胁分类：（目的IP的威胁分类）
        威胁标签：（目的IP的威胁标签）
        威胁来源：（目的IP的威胁来源）
        """
        # 发送两条告警
        syslog(
            '<1>Jul 12 14:59:18 D12;530000000119051342010751;ipv4;3; servconn_policy: time=2019-07-12 14:59:18;policy_name=out;server_addr=27.128.201.88;out_addr=222.118.183.131;proto=UDP;port=137;action=1')
        time.sleep(40)
        # 告警概览页面
        resp = AlarmOverview().send()
        result = json.loads(resp.text)
        print(result)
        # 两条告警对应的id
        id0 = result['data']['list'][0]['id']

        # 第一条数据
        threat = ThreatIntelligenceDetails()
        threat.url = host + '/alarm/search/info/{}'.format(id0)
        resp = threat.send()
        result = resp.json()
        print(result)
        data = result['data']['threatInfoVO'][0]
        data1 = result['data']['threatInfoVO'][1]
        # value 威胁值、sourceRef 威胁来源、category 威胁分类、geo 地理位置、service 威胁标签
        print(data)
        # assert_data1 = data['value'] == '27.128.201.88' and data['sourceRef'] == 'Emergingthreats' and data[
        #     'category'] == '扫描器节点' and data['geo'] == '中国-河北-保定' and data['threatTagVO']['service'] == ["ssh"]
        # assert_data2 = data1['value'] == '27.128.201.88' and data1['sourceRef'] == 'Emergingthreats' and data1[
        #     'category'] == '扫描器节点' and data1['geo'] == '中国-河北-保定' and data1['threatTagVO']['service'] == ["ssh"]
        # assert_data3 = data['value'] == '27.128.201.88' and data['sourceRef'] == 'ThreatWeb' and data['category'] == '僵尸网络' and data['geo'] == '中国-河北-保定'
        # assert_data4 = data1['value'] == '27.128.201.88' and data1['sourceRef'] == 'ThreatWeb' and data1['category'] == '僵尸网络' and data1['geo'] == '中国-河北-保定'
        pytest.assume(data['value'] == '27.128.201.88' and data['sourceRef'] == 'Emergingthreats' and data[
            'category'] == '扫描器节点' and data['geo'] == '中国-河北-保定' and data['threatTagVO']['service'] == ["ssh"])
        pytest.assume(
            data1['value'] == '27.128.201.88' and data1['sourceRef'] == 'ThreatWeb' and data1['category'] == '僵尸网络' and
            data1['geo'] == '中国-河北-保定')
        # pytest.assume('value' in data[1].values and 'sourceRef' in data and 'category' in data and 'geo' in data and 'service' in data)
        intel_detail = IntelligenceDetail()
        intel_detail.json = {"key": "27.128.201.88"}
        resp = intel_detail.send()
        result = resp.json()
        print(result)
        data = result['data'][0]
        # data1 = result['data'][1]
        # 判断  # 威胁值:27.128.201.88 威胁来源:Emergingthreats 威胁分类:扫描器节点 地理位置:中国-河北-保定 ssh
        pytest.assume(data['value'] == '27.128.201.88' and data['sourceRef'] == 'Emergingthreats' and data[
            'category'] == '扫描器节点' and data['geo'] == '中国-河北-保定' and data['threatTagVO']['service'] == ["ssh"])
        pytest.assume(
            data1['value'] == '27.128.201.88' and data1['sourceRef'] == 'ThreatWeb' and data1['category'] == '僵尸网络' and
            data1['geo'] == '中国-河北-保定')
        # 第二条数据
        syslog(
            '<1>Jul 12 14:59:18 D12;530000000119051342010751;ipv4;3; servconn_policy: time=2019-07-12 14:59:18;policy_name=out;server_addr=83.171.237.173;out_addr=27.128.201.88;proto=UDP;port=137;action=1')
        time.sleep(40)
        # 告警概览页面
        resp = AlarmOverview().send()
        result = json.loads(resp.text)
        id1 = result['data']['list'][0]['id']
        print(result)
        threat = ThreatIntelligenceDetails()
        threat.url = host + '/alarm/search/info/{}'.format(id1)
        resp = threat.send()
        result = resp.json()
        print(result)
        data = result['data']['threatInfoVO'][0]
        pytest.assume(data['value'] == '83.171.237.173' and data['sourceRef'] == 'TianJi Partners' and data[
            'category'] == 'APT情报' and data['geo'] == '德国-德国')
        # 威胁情报详情
        intel_detail = IntelligenceDetail()
        intel_detail.json = {"key": "83.171.237.173"}
        resp = intel_detail.send()
        result = resp.json()
        print(result)
        data = result['data'][0]
        pytest.assume(data['value'] == '83.171.237.173' and data['sourceRef'] == 'TianJi Partners' and data[
            'category'] == 'APT情报' and data['geo'] == '德国-德国')
        # intel_result = result['data'][0][:5]
        # intel_ssh = result['data'][0]['service']
        # pytest.assume(threat_result == intel_result and threat_ssh == intel_ssh)

    @allure.story('ISA-3166')
    def test_add_three_picture(self):
        """
        ISA-3166 : 【告警概览页面增加威胁情报统计】 查看”告警概览“页面，新增三幅统计图
        1	查看该页面	新增"威胁数量趋势折线图"、"威胁分类统计饼图（TOP10）"、"威胁数量分布柱形图(TOP10)"
        """
        # 查看新增图形
        # resp = AlarmOverviewPicture().send()
        # result = json.loads(resp.text)
        # print(result)
        # panel_list = result['data']['panelList'][-3:]  # 最后三幅图
        # print(panel_list)
        # result_list = []  # 存放新增三幅图的名称
        # for i in panel_list:
        #     result_list.append(i['panelName'])
        # print(result_list)
        # pytest.assume(result_list == ['威胁趋势', '威胁数量分布TOP10', '威胁分类TOP10'])
        # 接口 、 功能位置改变后的case
        resp = ThreatIntelligence().send()
        result = resp.json()
        print(result)
        data =result['data']
        # threatIp 数量分布TOP10、threatType 分类TOP10、threatTrend 趋势
        pytest.assume('threatIp' in data and 'threatType' in data and 'threatTrend' in data)


    @allure.story('ISA-3174')
    def test_traceability(self):
        """
        ISA-3174 : 【攻击溯源】告警信息中“攻击链阶段”有值且有受影响ip，操作列中增加“溯源”操作
        1 点击“告警处置”-“告警检索”，点击右上角的“筛选”按钮，告警类型选择“攻击行为告警”  下方的告警列表中，全部显示告警类型为“攻击行为告警”的告警信息
        2 再点击“筛选”，从“攻击链阶段”中任选一箱，查看下方的告警信息列表。如果一条告警信息中“受影响IP”列中显示有IP信息并且“攻击链阶段”显示有值，最后的操作列中显示的操作命令  在操作列中都有“溯源”，蓝色字体，可点击
        3 查看“攻击行为告警”告警信息，如果“受影响IP”列中未显示IP信息或者“攻击链阶段”未显示有值，最后的操作列中显示的操作命令  在操作列中未有“溯源”操作命令
        4 点击溯源  进入攻击溯源页面   页面右上角“返回”，点击可以返回告警检索页面
        """
        # 发送告警信息 19存在溯源 6无溯源
        syslog(
            '19|^06454202DF0743C4B961CF6CD323EC43|^192.168.100.123|^192.168.100.255|^1|^5|^192.168.100.124|^Firewall201229008|^2021-06-03 16:19:13.463|^0|^201229008|^0|^null|^')
        syslog(
            '<6>Nov 29 14:09:52 HOST;110103300117111310721344;ipv4;3; device_health: CPU使用=96；内存使用=57；磁盘使用=1；温度=0；会话数=79')
        time.sleep(40)
        # 筛选 攻击行为告警 攻击生效
        alarm = AlarmRetrieval()
        alarm.json = {"keyword": "", "alarmStartTime": "", "alarmLevel": "", "safeDeviceIp": "", "actionStatus": "",
                      "alarmStage": 600, "alarmEndTime": "", "alarmType": 20000000, "factory": "",
                      "alarm_filter": 'true',
                      "alarmTypeArr": [20000000], "threatType": "", "startPage": 1, "pageSize": 10}
        resp = alarm.send()
        result = json.loads(resp.text)
        data_list = result['data']['list']  # 数据列表
        id = result['data']['list'][0]['id']  # 第一行数据id 供溯源接口使用
        for i in data_list:
            pytest.assume('攻击行为告警' in i['alarmSecondaryType'])  # 判断每一行的告警都是工具行为告警
        # 告警检索攻击溯源
        traceability = AlarmRetrievalTraceability()
        traceability.json = {"alarmUuid": id}
        resp = traceability.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['data'] != [])  # 溯源接口 data不为[]
        # 获取告警检索页面告警
        resp = AlarmRetrieval().send()
        result = json.loads(resp.text)
        # 判断第一第二行数据如果alarmPrimaryMessage = 健康日志，无溯源调用溯源接口
        data_list = result['data']['list']  # 数据列表
        alarm_id = ''
        for i in data_list:
            if i['alarmPrimaryMessage'] == '健康日志':
                print(i['id'])
                alarm_id = i['id']
                break
        # 无溯源按钮，告警检索攻击溯源
        traceability = AlarmRetrievalTraceability()
        traceability.json = {"alarmUuid": alarm_id}
        resp = traceability.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['data'] == [])  # 无溯源按钮，数据为空

    @allure.story('ISA-3493')
    def test_traceability_page(self):
        """
        ISA-3493 : 【攻击溯源页面】攻击溯源页面信息查验
        1 在“告警处理”—“告警检索”告警列表中，选择一条操作列中有“溯源”命令的告警，点击“溯源”
        进入该条告警的攻击溯源页面
        2 溯源页面分成三部分
        页面最上方，显示所有告警类型，其中攻击告警细化为6个攻击链阶段的告警类型
        中间是点击“溯源”的这一条告警信息的列表
        下方是产生这一溯源告警的原始日志的集合
        3查看上方区域的告警显示，包括攻击链阶段
        凡是受影响ip产生的所有告警信息，显示在各告警类型的右上角，显示方式为红色圆圈内白色数字。没有相应类型的告警，数字显示为0。
        用户行为告警和业务异常告警，按这两种大分类显示告警数。
        攻击行为告警则按照6种攻击链阶段来显示告警数。
        举例说明。例如涉及受影响ip为1.1.1.1，告警类型为业务异常—>流量异常的告警为5个，告警类型为用户行为—>可疑用户登录为3个，告警类型为攻击行为告警—>扫描探测 2个，攻击行为告警—>下载植入3个 。那么在上方的攻击链阶段显示区域，用户行为右上角数字为3，扫描探测右上角数字为2，下载植入右上角数字为3，业务异常右上角数字为5，其余图标右上角数字均为0
        4 查看中间区域列表显示的该条告警
        该条告警和“告警检索”中显示的信息一致，告警列表的显示项会不同，在溯源页面中，告警信息列表中显示项为：告警产生时间、告警级别、告警类型、所属区域、受影响ip、告警描述、发生次数、威胁类型、处置时间、攻击链阶段、处理状态
        该列表区域有向前翻页按钮、向后翻页按钮、当前页页码、每页显示条数的选择下拉框
        5 查看下方区域的日志列表
        下方的日志列表，显示的是这一时间段内触发该条告警的所有原始日志，可能1条日志，也可能多条日志。时间段由触发告警的关联分析规则中设置的时间，默认是5分钟。
         该列表区有向前翻页按钮、向后翻页按钮、当前页页码、每页显示条数的选择下拉框
        """
        # 筛选 攻击行为告警 攻击生效(目的获取有溯源的告警)
        alarm = AlarmRetrieval()
        alarm.json = {"keyword": "", "alarmStartTime": "", "alarmLevel": "", "safeDeviceIp": "", "actionStatus": "",
                      "alarmStage": 600, "alarmEndTime": "", "alarmType": 20000000, "factory": "",
                      "alarm_filter": 'true',
                      "alarmTypeArr": [20000000], "threatType": "", "startPage": 1, "pageSize": 10}
        resp = alarm.send()
        result = json.loads(resp.text)
        id = result['data']['list'][0]['id']  # 第一行数据id 供溯源接口使用
        # time = result['data']['list'][0]['alarmStartTime']  # 告警产生时间
        # alarm_tpye = result['data']['list'][0]['alarmSecondaryType']  # 告警类型
        # 告警检索攻击溯源
        traceability = AlarmRetrievalTraceability()
        traceability.json = {"alarmUuid": id}
        resp = traceability.send()
        result = json.loads(resp.text)
        data = result['data']  # 攻击溯源的8种类型列表
        for i in data:
            # 告警检索攻击溯源告警列表
            alarm_list = AlarmTraceabilityList()
            code = i['code']
            alarm_list.json = {"alarmId": id, "alarmStage": code, "startPage": 1,
                               "pageSize": 10}
            resp = alarm_list.send()
            result = json.loads(resp.text)
            pytest.assume(result['data']['total'] == i['totalAlarmNum'])  # 判断两个数量值相等
            if i['totalAlarmNum'] != 0:  # 类型告警数不为零，日志区域接口
                value = result['data']['list'][0]  # 第一条告警数据
                # alarmStartTime 告警产生时间、alarmLevel 告警级别、alarmSecondaryType 告警类型、factoryName 所属区域、safeDeviceIp 受影响ip、alarmPrimaryMessage 告警描述
                # mergeCount 发生次数、threatType 威胁类型、alarmEndTime 处置时间、alarmStageName 攻击链阶段、actionStatusName 处理状态
                pytest.assume(
                    'alarmStartTime' in value and 'alarmLevel' in value and 'alarmSecondaryType' in value and 'factoryName' in value and 'safeDeviceIp' in value and
                    'actionStatusName' in value and 'mergeCount' in value and 'threatType' in value and 'alarmEndTime' in value and 'alarmStageName' in value and 'actionStatusName' in value)
                event = AlarmTraceabilityEventList()
                event.json = {"alarmId": id, "pageSize": 10, "startPage": 1}
                resp = event.send()
                result = json.loads(resp.text)
                pytest.assume(result['data']['total'] >= 1)  # 日志数最少一条

    # todo 3175接口只能导出二进制流

    @allure.story('ISA-3176')
    def test_import_correlation_analysis(self):
        """
        ISA-3176 : 【导入关联分析规则】 导入关联分析规则文件
        1 在关联分析页面，点击“导入”按钮。在弹出的文件选择框中，选择要导入的规则文件，点击确定。  导入成功，有弹窗消息提示用户操作成功。
        2 查看关联分析页面
        导入的关联分析规则为增量导入，系统已有的关联分析规则未被删除和破坏。
        新导入的规则也显示在关联分析页面。能够查找到新导入的规则，显示正确，增加的规则数量和文件中的规则一致，无错漏，无乱码。
        3 导入关联分析规则文件，记录操作日志
        audit权限用户登录系统，查看操作日志，有“导入关联分析文件xxxx 失败/成功”的日志记录信息，描述内容完整，语句通顺，无乱码
        """
        # 导入关联分析规则文件
        import_analysis = ImportCorrelationAnalysis()
        # import_analysis.headers = {
        #     'Content-Disposition': 'form-data'
        # }
        resp = import_analysis.send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '导入成功')
        # 关联分析页查看新增关联分析
        resp = CorrelationAnalysisPage().send()
        result = json.loads(resp.text)
        print(result)
        name = result['data']['ruleBaseList'][0]['name']  # 第一行的规则名称
        id = result['data']['ruleBaseList'][0]['id']  # 第一行的规则id 删除接口使用
        print('id', id)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(name == '漏洞防护告警1')
        # audit登录查看日志
        header = login_test(audit, password)
        operator_log = OperatorLog()
        operator_log.headers = header
        resp = operator_log.send()
        result = json.loads(resp.text)
        print(result)
        log_list = result['data']['list']
        context_list = []
        for i in log_list:
            print(i['context'])
            context_list.append(i['context'])
        pytest.assume('导入[关联分析20220303192735.xlsx]成功' in context_list[:3])  # 判断audit前三条新增成功
        # 删除关联分析文件
        time.sleep(1)
        delete = DeleteCorrelationAnalysis()
        delete.json = {
            "ids": [id]
        }
        resp = delete.send()
        result = json.loads(resp.text)
        print(result['message'])
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '1条数据已删除！')

    @allure.story('ISA-3177')
    def test_add_dashboard(self):
        """
        ISA-3177 : 【自定义仪表盘】 新建仪表盘
        1 点击“系统配置”，在左侧导航栏中有“自定义仪表盘”命令，点击该命令   右侧出现自定义仪表盘主页面
        2 在“自定义仪表盘”主页面，点击“+新建仪表盘”   弹窗弹出“新建仪表盘”，
        3 在仪表盘名称中，输入超过64个字符长度的名称    输入框只能输入64个字符，无法输入到65个字符
        4 在仪表盘名称中，输入不符合规则的字符（例如特殊字符！@#@）    在名称输入框下方显示红色字体，提示名称规则
        5 输入符合规则的仪表盘名称（例如：仪表盘1），点击确定（说明：仪表盘名称长度不超过64个字符，支持数字、大小写字母、中文和-_.特殊字符）
        右侧出现仪表1的设计页面，可以对仪表盘1的页面进行设计：选择仪表盘的图表、图表形式和定制仪表盘整体查询条件。
        6 在编辑仪表盘的页面中，点击右上角的“返回”按钮，在弹窗提示是否确认离开点击“确认”
        返回到“自定义仪表盘”主页面，新建的仪表盘（例如：仪表盘1）显示在自定义仪表盘列表中
        """
        # 新增入不符合规则的字符（例如特殊字符！@#@）
        add = AddDashboard()
        add.json = {"dashboardName": "！@#@"}
        resp = add.send()
        print(resp.json())
        print(resp.text)
        result = resp.json()
        pytest.assume(result['message'] == '[！@#@]名称不合法，可输入英文、数字、中文、空格和特殊字符(_-.)，范围1~64')
        # 新增仪表盘(数字、大小写字母、中文和-_.特殊字符，超过64字符)
        add1 = AddDashboard()
        add1.json = {"dashboardName": "123Aa-_.test测试仪表盘-_.123Aa-_.test测试仪表盘-_.123Aa-_.test测试仪表盘-_.123Aadfes"}
        resp = add1.send()
        result = json.loads(resp.text)
        print(result)
        # id = result['data']['id']  # 新增仪表盘id
        pytest.assume(result[
                          'message'] == '[123Aa-_.test测试仪表盘-_.123Aa-_.test测试仪表盘-_.123Aa-_.test测试仪表盘-_.123Aadfes]名称不合法，可输入英文、数字、中文、空格和特殊字符(_-.)，范围1~64')
        # 新增仪表盘(数字、大小写字母、中文和-_.特殊字符，64字符)
        add1 = AddDashboard()
        add1.json = {"dashboardName": "123Aa-_.test测试仪表盘-_.123Aa-_.test测试仪表盘-_.123Aa-_.test测试仪表盘-_.123A"}
        resp = add1.send()
        result = json.loads(resp.text)
        print(result)
        id = result['data']['id']  # 新增仪表盘id
        pytest.assume(result['message'] == '操作成功')
        # 查看界面新增
        resp = DashboardPage().send()
        result = json.loads(resp.text)
        print(result)
        pytest.assume(result['statusCode'] == 200)
        print(result['data']['values'][0]['dashboardName'])
        pytest.assume(result['data']['values'][0][
                          'dashboardName'] == '123Aa-_.test测试仪表盘-_.123Aa-_.test测试仪表盘-_.123Aa-_.test测试仪表盘-_.123A')  # 新增仪表盘显示64字符
        # 删除仪表盘
        delete = DeleteDashboard()
        delete.json = {"id": id}
        print(delete.json)
        resp = delete.send()
        # result = json.loads(resp.text)
        result = resp.json()
        print(resp.json())
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '删除仪表盘成功')

    # def test_design(self):
    #     # 新增仪表盘
    #     add1 = AddDashboard()
    #     add1.json = {"dashboardName": "123"}
    #     resp = add1.send()
    #     result = json.loads(resp.text)
    #     print(result)
    #     id = result['data']['id']  # 新增仪表盘id
    #     #  查看仪表盘
    #     show = ShowDashboard()
    #     show.json = {"route": 0, "factoryId": 2, "dateRange": 1, "actionStatus": 1, "type": 2, "dashboard_id": id}
    #     resp = show.send()
    #     result = resp.json()
    #     print(result)


    @allure.story('ISA-3183')
    def test_generate_port_baseline(self):
        """
        ISA-3183 : 【端口基线】用“自动生成基线”生成所有已确认设备的端口基线
        1 点击策略配置—基线配置—端口基线  右侧出现端口基线主页面
        2 点击端口基线列表上方的“生成基线”  开始生成端口基线，在“生成基线”按钮后出现提示信息“生成基线中，请勿操作……”
        3 在生成基线过程中，点击页面上的新增或者删除按钮  提示正在生成基线中，稍候操作
        4 等待基线生成完成，查看端口基线列表
        所有已确认资产生成端口基线，每一个设备排列在端口基线页面的列表中。
        所有已确认资产的设备名称都显示在端口基线列表中。
        在每个设备的“端口基线”列中，显示有端口（为该设备开放的端口）。多个端口之间用,进行分隔显示。
        如果有设备没有开放的端口，则“端口基线”列中显示空
        """
        # 生成端口基线
        resp = GenerateBaseline().send()
        result = resp.json()
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '开始生成端口基线')
        # 已确认资产列表
        resp = RecognizedAssetsList().send()
        result = resp.json()
        print(result)
        total = result['data']['total']  # 资产总数
        # 基线列表页
        resp = BaselinePage().send()
        result = resp.json()
        print(result)
        first_port = result['data']['values'][0]['ports']  # 第一个端口
        totalSize = result['data']['totalSize']  # 基线总数
        id_list = []
        for i in result['data']['values']:
            id_list.append(i['id'])
        pytest.assume(total == totalSize)
        pytest.assume(first_port == None)
        # 删除端口基线
        delete = DeleteGenerateBaseline()
        delete.json = {"ids": id_list}
        resp = delete.send()
        result = resp.json()
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('ISA-3185')
    def test_add_generate_port_baseline(self):
        """
        ISA-3185 : 【端口基线】用“新建”来新建新确认资产的端口基线
        1	在“基线配置”—“端口基线”页面上，点击“新增”	弹出“新增端口基线”窗口
        2	点击“新增端口基线”窗口上的按钮“请选择设备”	弹出“资产列表”的面板，显示所有未设置端口基线的已确认资产。
        3	如果需要新建端口基线的设备显示在设备列表中，直接勾选	可以选中
        4	资产设备太多的话，可以在“资产列表”页面用“筛选”或者“搜索”功能搜索设备，来选择需要新增端口基线的设备，一次只能选择一个设备	可搜索到所需的已确认资产设备，勾选选中
        5	在“新增端口基线”页面，点击确定	返回端口基线主页面，新建的端口基线显示在基线列表中
        6	新增端口基线，记录操作日志	以audit权限用户登录系统，查看操作日志，能查看到新增端口基线的操作日志
        """
        # 端口基线设备列表查询，获取新增端口基线的id
        query = AssetListQuery()
        resp = query.send()
        result = resp.json()
        # 根据关键字ip查询
        first_ip = result['data']['list'][0]['ip']
        first_name = result['data']['list'][0]['name']
        query.json = {"startPage": 1, "pageSize": 10, "keyword": first_ip}
        resp = query.send()
        result = resp.json()
        first_id = result['data']['list'][0]['id']
        print(first_id)
        print(result)
        # 新增端口基线
        add = AddGenerateBaseline()
        add.json = {"assetId": first_id}
        resp = add.send()
        result = resp.json()
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '新增端口基线成功')
        # 基线列表页
        resp = BaselinePage().send()
        result = resp.json()
        totalSize = result['data']['totalSize']  # 基线总数
        id = result['data']['values'][0]['id']  # 基线id
        # id_list = []
        # for i in result['data']['values']:
        #     id_list.append(i['id'])
        pytest.assume(totalSize == 1)
        time.sleep(1)
        # audit 查看操作日志
        header = login_test(audit, password)
        operator_log = OperatorLog()
        operator_log.headers = header
        resp = operator_log.send()
        result = json.loads(resp.text)
        print(result)
        log_list = result['data']['list']
        context_list = []
        for i in log_list:
            print(i['context'])
            context_list.append(i['context'])
        pytest.assume('新增资产[{}]的端口基线成功'.format(first_name) in context_list[:3])  # 判断audit前三条新增成功
        # 删除端口基线
        delete = DeleteGenerateBaseline()
        delete.json = {"ids": [id]}
        print(delete.json)
        resp = delete.send()
        result = resp.json()
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('ISA-3186')
    def test_port_detail_page(self):
        """
        ISA-3186 : 【端口基线】端口明细列表页面
        1	在“端口基线”主页面中，点击任一端口基线操作列中的“查看明细”	进入“端口基线明细列表”页面
        2	在端口明细列表页面，显示该设备的端口基线中所有的端口	显示每一个基线端口的端口号，传输层协议，服务，创建时间
        3	在端口明细列表页面中，有新增、删除、编辑操作按钮。	新增和删除按钮，在页面左上方，在每一个端口的操作列，有编辑和删除操作按钮。这些按钮均可以点击。
        4	点击“新增”增加基线端口	新增按钮可以点击，弹出“新增端口”弹窗
        5	勾选一个，多个或者全选端口，点击“删除”	删除按钮可以点击，删除基线端口
        6	点击端口操作列中的“编辑”	进入编辑端口页面，对已加端口进行修改
        7	端口明细列表可以分页显示	下方有页面总数，前一页，后一页跳转按钮，还有每页显示数量的下拉选框。
        """
        # 端口基线设备列表查询，获取新增端口基线的id
        query = AssetListQuery()
        resp = query.send()
        result = resp.json()
        # 根据关键字ip查询
        first_ip = result['data']['list'][0]['ip']
        first_name = result['data']['list'][0]['name']
        query.json = {"startPage": 1, "pageSize": 10, "keyword": first_ip}
        resp = query.send()
        result = resp.json()
        first_id = result['data']['list'][0]['id']
        print(first_id)
        print(result)
        # 新增端口基线
        add = AddGenerateBaseline()
        add.json = {"assetId": first_id}
        resp = add.send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '新增端口基线成功')
        # 查看端口基线列表，获取id值
        resp = BaselinePage().send()
        result = resp.json()
        id = result['data']['values'][0]['id']  # 为端口基线明细提供参数
        # 查看端口明细
        port_details = PortBaselineDetails()
        port_details.json = {"pageSize": 10, "startPage": 1, "keyword": "", "portsBaselineId": id}
        resp = port_details.send()
        result = resp.json()
        print(result)
        totalSizeBefore = result['data']['totalSize']
        # 添加基线端口
        add_port = AddBaselinePort()
        add_port.json = {"portsBaselineId": id, "ports": "60", "agreement": 1, "service": "service"}
        resp = add_port.send()
        result = resp.json()
        pytest.assume(result['message'] == '添加端口基线详情成功')
        # 查看端口明细
        port_details = PortBaselineDetails()
        port_details.json = {"pageSize": 10, "startPage": 1, "keyword": "", "portsBaselineId": id}
        resp = port_details.send()
        result = resp.json()
        print(result)
        totalSizeAfter = result['data']['totalSize']
        port_id = result['data']['values'][0]['id']  # 修改删除接口使用
        pytest.assume(totalSizeAfter - totalSizeBefore == 1)  # 新增一个端口
        # 查看端口基线列表，一个端口时的端口值
        resp = BaselinePage().send()
        result = resp.json()
        print(result)
        print(result['data']['values'][-1]['ports'])
        # pytest.assume(result['data']['values'][-1]['ports'] == '60')
        pytest.assume(result['data']['values'][0]['ports'][-2:] == '60')
        # 添加第二个基线端口
        add_port = AddBaselinePort()
        add_port.json = {"portsBaselineId": id, "ports": "70", "agreement": 1, "service": "service"}
        resp = add_port.send()
        result = resp.json()
        pytest.assume(result['message'] == '添加端口基线详情成功')
        # 查看端口基线列表，一个端口时的端口值
        resp = BaselinePage().send()
        result = resp.json()
        print(result)
        print(result['data']['values'][-1]['ports'])
        pytest.assume(result['data']['values'][0]['ports'][-5:] == '60,70')  # ISA-3183 第四步
        # 修改第一个端口
        edit_port = EditBaselinePort()
        edit_port.json = {"id": port_id, "portsBaselineId": id, "ports": "61", "agreement": 1, "service": ""}
        resp = edit_port.send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '修改端口基线详情成功')
        # 删除第一个端口
        delete_port = DeleteBaselinePort()
        delete_port.json = {"ids": [port_id]}
        resp = delete_port.send()
        result = resp.json()
        print('edit', result)
        pytest.assume(result['message'] == '删除端口基线详情成功')
        # 删除端口基线
        delete = DeleteGenerateBaseline()
        delete.json = {"ids": [id]}
        print(delete.json)
        resp = delete.send()
        result = resp.json()
        pytest.assume(result['statusCode'] == 200)
        pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('ISA-3187')
    def test_add_baseline_port(self):
        """
        ISA-3187 : 【端口基线】新增基线端口
        1 在“端口基线”页面，点击某个端口基线列表操作列中“查看明细”   进入“端口基线明细列表”
        2 在“端口明细列表”页面左上方点击“新增”   弹出“新增端口”弹窗
        3 在新增端口页面，有三个输入框，端口号和传输层协议为必填项，服务可以不输。端口号输入框后的有“i”图标   输入置于‘i’上，显示端口号的输入规则
        4 传输层协议为下拉框，可以选择tcp和udp   可选择
        5 服务为输入框，最多输入64个字符，支持字母，汉字，数字和._-特殊字符，输入符合规则的服务名称   输入成功
        6 在“常用端口知识库”中，有步骤2中输入的端口号，并且和步骤3中的协议有绑定（例如常用端口库中，端口22协议tcp对应了服务ftp），那么服务输入框中会自动出现“ftp”，可以直接点击选中   点击选中成功
        7 根据步骤3/4/5的规则，输入端口号，选择协议，输入服务名称，点击确定
        新增基线端口成功，端口号显示在“端口基线明细列表”中，协议和服务也显示正确
        """
        try:
            # 端口基线设备列表查询，获取新增端口基线的id
            query = AssetListQuery()
            resp = query.send()
            result = resp.json()
            # 根据关键字ip查询
            first_ip = result['data']['list'][0]['ip']
            first_name = result['data']['list'][0]['name']
            query.json = {"startPage": 1, "pageSize": 10, "keyword": first_ip}
            resp = query.send()
            result = resp.json()
            first_id = result['data']['list'][0]['id']
            print(first_id)
            print(result)
            # 新增端口基线
            add = AddGenerateBaseline()
            add.json = {"assetId": first_id}
            resp = add.send()
            result = resp.json()
            print(result)
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '新增端口基线成功')
            # 查看端口基线列表，获取id值
            resp = BaselinePage().send()
            result = resp.json()
            id = result['data']['values'][0]['id']  # 为端口基线明细提供参数
            # 查看端口明细
            port_details = PortBaselineDetails()
            port_details.json = {"pageSize": 10, "startPage": 1, "keyword": "", "portsBaselineId": id}
            resp = port_details.send()
            result = resp.json()
            print(result)
            total_before = result['data']['totalSize']
            # 添加基线端口
            add_port = AddBaselinePort()
            add_port.json = {"portsBaselineId": id, "ports": "60", "agreement": 0,
                             "service": "123Aa-_.test测试端口线-_.123Aa-_.test测试端口线-_.123Aa-_.test测试端口线-_.123A"}  # udp
            resp = add_port.send()
            result = resp.json()
            pytest.assume(result['message'] == '添加端口基线详情成功')
            # 查看端口明细
            port_details = PortBaselineDetails()
            port_details.json = {"pageSize": 10, "startPage": 1, "keyword": "", "portsBaselineId": id}
            resp = port_details.send()
            result = resp.json()
            value = result['data']['values'][0]
            value1 = result['data']['values'][-1]
            assert_value = value['ports'] == '60' and value['agreement'] == 0 and value['service'] == '123Aa-_.test测试端口线-_.123Aa-_.test测试端口线-_.123Aa-_.test测试端口线-_.123A'
            assert_value1 = value1['ports'] == '60' and value1['agreement'] == 0 and value1['service'] == '123Aa-_.test测试端口线-_.123Aa-_.test测试端口线-_.123Aa-_.test测试端口线-_.123A'
            print(result)
            total_after = result['data']['totalSize']
            # port_id = result['data']['values'][0]['id']  # 修改删除接口使用
            pytest.assume(total_after - total_before == 1)  # 新增一个端口
            pytest.assume(assert_value or assert_value1)  # 新增一个端口
        except Exception:
            raise Exception
        finally:
            pass
            # 删除端口基线
            delete = DeleteGenerateBaseline()
            delete.json = {"ids": [id]}
            print(delete.json)
            resp = delete.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('ISA-3190')
    def test_confirm_asset_add_strange_port(self):
        """
        ISA-3190 : 【端口基线】与网络会话实时对比，对已知资产的新增陌生端口进行告警
        1 设备1已经生成端口基线
        在端口基线列表中可以查看到该端口基线
        2 生成端口基线后，如果有USM接入，系统会对比USM上报的网络会话和端口基线。如果网络会话中的IP地址（源ip或者目的ip或者受影响ip）为生成了端口基线的设备，而网络会话中的端口又是该设备端口基线中没有的端口
        会触发一条可疑端口告警。
        3 在告警检索中，查看可疑端口告警
        能找到步骤2中的可疑端口告警，且告警端口号不在端口基线中
        4 查看“可疑端口”告警信息
        告警描述：网络中出现了已确认资产的可疑端口通讯。
        影响 ：可能是非法应用开启了该端口通讯，具有一定的安全隐患。
        建议：网络中出现了已确认资产的可疑端口通讯，请尽快检查网络中该IP地址对应的端口应用。
        """
        try:
            # 端口基线设备列表查询，获取新增端口基线的id
            query = AssetListQuery()
            resp = query.send()
            result = resp.json()
            print(result)
            name = result['data']['list'][0]['name']
            ip = result['data']['list'][0]['ip']
            # 根据关键字ip查询
            first_ip = result['data']['list'][0]['ip']
            first_name = result['data']['list'][0]['name']
            query.json = {"startPage": 1, "pageSize": 10, "keyword": first_ip}
            resp = query.send()
            result = resp.json()
            first_id = result['data']['list'][0]['id']
            print(first_id)
            print(result)
            # 新增端口基线
            add = AddGenerateBaseline()
            add.json = {"assetId": first_id}
            resp = add.send()
            result = resp.json()
            print(result)
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '新增端口基线成功')
            # 查看端口基线列表，获取id值
            resp = BaselinePage().send()
            result = resp.json()
            id = result['data']['values'][0]['id']  # 为端口基线明细提供参数
            # 查看端口明细
            port_details = PortBaselineDetails()
            port_details.json = {"pageSize": 10, "startPage": 1, "keyword": "", "portsBaselineId": id}
            resp = port_details.send()
            result = resp.json()
            print(result)
            total_before = result['data']['totalSize']
            # 添加基线端口
            add_port = AddBaselinePort()
            add_port.json = {"portsBaselineId": id, "ports": "60", "agreement": 1, "service": "service"}
            resp = add_port.send()
            result = resp.json()
            pytest.assume(result['message'] == '添加端口基线详情成功')
            # 查看端口明细
            port_details = PortBaselineDetails()
            port_details.json = {"pageSize": 10, "startPage": 1, "keyword": "", "portsBaselineId": id}
            resp = port_details.send()
            result = resp.json()
            print(result)
            total_after = result['data']['totalSize']
            pytest.assume(total_after - total_before == 1)  # 新增一个端口
            # 查看端口基线列表，一个端口时的端口值
            resp = BaselinePage().send()
            result = resp.json()
            print(result)
            ports_list = [value['ports'] for value in result['data']['values']]
            port = eval(ports_list[0])
            print(port)
            if port != 60:
                print(port, port[0], port[-1])
                # pytest.assume(result['data']['values'][0]['ports'] == '60' or result['data']['values'][-1]['ports'] == '60')
                pytest.assume(port[-1] == 60)
            else:
                pytest.assume(port == 60)
            # 发送网络会话端口
            # syslog('<8>Sep 10 16:26:07 usmadmin1 12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.4.173|^192.168.4.173|^2021-06-03 16:28:37|^17|^192.168.4.173|^|^64760|^192.168.4.173|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^')
            syslog('12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^{}|^2021-06-03 16:28:37|^17|^{}|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(ip,name,ip,ip))
            time.sleep(30)
            # 获取告警检索页面告警
            resp = AlarmRetrieval().send()
            result = json.loads(resp.text)
            value = result['data']['list'][0]
            # 判断告警信息
            pytest.assume(value['alarmSecondaryType'] == '用户行为告警/可疑端口' and (value['alarmPrimaryMessage'] == '网络中出现了已确认资产的可疑端口通讯，端口为64760' or value['alarmPrimaryMessage'] == '网络中出现了已确认资产的可疑端口通讯，端口为5350') and value['warmSuggest'] == '网络中出现了已确认资产的可疑端口通讯，请尽快检查网络中该IP地址对应的端口应用')
        except Exception:
            raise Exception
        finally:
            # 删除端口基线
            delete = DeleteGenerateBaseline()
            delete.json = {"ids": [id]}
            print(delete.json)
            resp = delete.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('ISA-usm发送日志产生告警')
    def test_usm_log_alarm(self):
        # 发送网络会话产生的日志
        # syslog(' 7|^null|^|^2|^1|^0|^|^|^2021-06-03 14:29:42|^2021-06-03 14:29:42|^way-rh5.5|^192.168.3.135|^192.168.3.135|^/sbin/umount-uscs-pub.sh|^非白名单程序报警，控制模式执行：阻止，白名单校验：未通过|^/sbin/udevd|^-|^-|^-|^1|^root|^1|^0|^0|^null|^0|^')
        syslog('7|^null|^|^2|^1|^0|^|^|^2021-06-03 14:29:42|^2021-06-03 14:29:42|^way-rh5.5|^192.168.3.135|^{}|^/sbin/umount-uscs-pub.sh|^非白名单程序报警，控制模式执行：阻止，白名单校验：未通过|^/sbin/udevd|^-|^-|^-|^1|^root|^1|^0|^0|^null|^0|^'.format(IP))
        time.sleep(30)
        # 查看日志检索产生的日志信息
        resp = LogRetrieve().send()
        result = resp.json()
        print(result)
        #  原始日志
        pytest.assume(result['dataList'][0]['originlog'] == '7|^null|^|^2|^1|^0|^|^|^2021-06-03 14:29:42|^2021-06-03 14:29:42|^way-rh5.5|^192.168.3.135|^{}|^/sbin/umount-uscs-pub.sh|^非白名单程序报警，控制模式执行：阻止，白名单校验：未通过|^/sbin/udevd|^-|^-|^-|^1|^root|^1|^0|^0|^null|^0|^'.format(IP))
        pytest.assume(result['dataList'][0]['eventlevel'] == '严重')  # 级别
        pytest.assume(result['dataList'][0]['eventcategory'] == '业务异常/非法程序启动')  # 类型
        # 查看告警检索中产生日志
        resp = AlarmRetrieval().send()
        result = resp.json()
        print(result)
        pytest.assume(result['data']['list'][0]['alarmLevel'] == '一般')
        pytest.assume(result['data']['list'][0]['alarmSecondaryType'] == '攻击行为告警/非法程序启动')
        pytest.assume(result['data']['list'][0]['safeDeviceIp'] == IP)
        pytest.assume(result['data']['list'][0]['alarmPrimaryMessage'] == '非白名单程序报警，控制模式执行：阻止，白名单校验：未通过，程序路径为/sbin/umount-uscs-pub.sh')
