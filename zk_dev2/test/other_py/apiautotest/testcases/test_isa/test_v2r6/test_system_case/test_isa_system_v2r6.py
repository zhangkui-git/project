'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/3/29 11:29
software: PyCharm
'''
import datetime
import json
import logging

import time

import allure
import pytest

from api.isa.alarm_handling import AlarmRetrieval, AlarmRetrievalQuery
from api.isa.asset_center import *
from api.isa.audit import OperatorLog
from api.isa.compliance_analysis import ComplianceTaskAdd, ComplianceTaskUpdate, ComplianceTaskList, \
    ComplianceTaskDelete
from api.isa.data_analysis import LogRetrieve
from api.isa.login import VulnerabilityConfiguration
from api.isa.monitoring_center import *
from api.isa.policy_config import *
from api.isa.security_knowledge_base import IntelligenceAutoUpdate, SecurityAnalysisQuery, IntelligenceUpdateDetail, \
    AddCommonPort, DeleteCommonPort, AddDisposalAdvice, DeleteDisposalAdvice
from api.login_api import login_test
from common.dbutil import DB
from common.logger import GetLogger
from common.syslog import syslog
from config.config import local_ip, IP
from data.common_data import audit, password, admin, small_field, last_week, today


@allure.feature('系统案例-资产中心')
class TestAssetCenter:
    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    @allure.story('拓扑管理-逻辑拓扑')
    @allure.title('逻辑拓朴产生告警及状态-ISA-2841、ISA-2842、ISA-2843、ISA-2844、ISA-2845、ISA-2846、ISA-2847、ISA-2848')
    def test_logical_topo(self):
        try:
            self.logging.info('查看区域管理列表')
            resp = AeraQuery().send()
            result = resp.json()
            print(result)
            value = result['data'][0]['children'][0]['value']  # xx区域value值
            self.logging.info('修改xx区域')
            mod = ModAera(value)
            resp = mod.send()
            result = resp.json()
            print(result)
            pytest.assume(result['statusCode'] == 200)
            self.logging.info('开启默认网络基线')
            resp = NetworkBaseline().send()
            result = resp.json()
            print(result)
            # pytest.assume(result['status'] == True)
            # logging.info('添加网络基线明细')
            # base = BaselineDetails(srcIp=local_ip, dstIp=IP)
            # resp = base.send()  # srcIp本地电脑ip， dstIp服务器地址
            # result = resp.json()
            # print(base.json)
            # print(result)
            # pytest.assume(result['status'] == True)
            self.logging.info('非法外联')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.10.65|^网络会话|^2021-06-03 16:28:37|^17|^192.168.10.65|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    IP))
            time.sleep(30)
            self.logging.info('查看逻辑拓扑列表')
            resp = LogicTopo().send()
            result = resp.json()
            print(result)
            # pytest.assume(result['data']['list'][0]['status'] == 1)
            self.logging.info('查看告警检索-产生日志')
            resp = AlarmRetrieval().send()
            result = resp.json()
            print(result)
            data = result['data']['list'][0]
            pytest.assume(
                data['alarmStartTime'].split(' ')[0] == str(datetime.datetime.now().strftime("%Y-%m-%d")))  # 判断时间
            pytest.assume(data['alarmLevel'] == '一般')  # 告警级别
            pytest.assume(data['alarmSecondaryType'] == '用户行为告警/非法外联')  # 告警类型
            pytest.assume(data['factoryName'] == 'XX区域')  # 区域
            pytest.assume(data['alarmPrimaryMessage'] == '网络中出现了非法外联。')  # 告警描述
            pytest.assume(data['warmSuggest'] == '请确认主机所属区域是否允许外部连接；如果不允许请停止外部连接处理；如果允许可以对相关规则进行配置不产生此类告警信息')  # 告警类型
            self.logging.info('跨区通信')
            self.logging.info('查看区域列表')
            resp = AeraQuery().send()
            result = resp.json()
            print(result)
            data = result['data'][0]['children']  # xx集团子区域
            area_list = []
            for i in data:
                area_list.append(i['label'])
            if 'test' not in area_list:
                resp = AddAera(factoryIpScope='192.168.5.1-192.168.5.7').send()
                result = resp.json()
                print(result)
                pytest.assume(result['message'] == '操作成功')
            self.logging.info('查看资产列表')
            resp = GetList().send()
            result = resp.json()
            print(result)
            log_source_list = result['data']['list']  # 日志源数据
            list_ip = [i['ip'] for i in log_source_list]
            self.logging.info('查看区域列表')
            resp = AeraQuery().send()
            result = resp.json()
            print(result)
            vaule = result['data'][0]['children'][1]['value']
            if '192.168.5.5' not in list_ip:  # 如果没有创建资产
                # todo 改为添加资产
                # resp = AddLogSource(name='192.168.5.5', ip='192.168.5.5', factory=vaule).send()
                resp = AddAssetParam(name='192.168.5.5', ip='192.168.5.5', factoryId=vaule).send()
                result = resp.json()
                print(result)
            self.logging.info('查看资产包含192.168.5.5')
            asset = GetList()
            resp = asset.send()
            result = resp.json()
            data = result['data']['list']
            ip_list = [d['ip'] for d in data]
            print(ip_list)
            pytest.assume('192.168.5.5' in ip_list)
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.5.5|^网络会话|^2021-06-03 16:28:37|^17|^192.168.5.5|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip))
            time.sleep(30)
            self.logging.info('查看逻辑拓扑列表')
            resp = LogicTopo().send()
            result = resp.json()
            print(result)

            # pytest.assume(result['data']['list'][0]['status'] == 2)
            self.logging.info('查看告警检索-产生日志')
            resp = AlarmRetrieval().send()
            result = resp.json()
            print(result)
            data = result['data']['list'][0]
            pytest.assume(
                data['alarmStartTime'].split(' ')[0] == str(datetime.datetime.now().strftime("%Y-%m-%d")))  # 判断时间
            pytest.assume(data['alarmLevel'] == '一般')  # 告警级别
            pytest.assume(data['alarmSecondaryType'] == '用户行为告警/非法外联')  # 告警类型
            pytest.assume(data['factoryName'] == 'XX区域')  # 区域
            pytest.assume(data['alarmPrimaryMessage'] == '网络中出现了跨区通信的资产。')  # 告警描述
            pytest.assume(data['warmSuggest'] == '请确认主机所属区域是否允许外部连接；如果不允许请停止外部连接处理；如果允许可以对相关规则进行配置不产生此类告警信息')  # 告警类型
            self.logging.info('非法连接')
            self.logging.info('查看资产列表')
            resp = GetList().send()
            result = resp.json()
            print(result)
            asset_list = result['data']['list']  # 资产数据
            # list_ip = []
            # for i in log_source_list:
            #     list_ip.append(i['assetIp'])
            list_ip = [i['ip'] for i in asset_list]
            if '192.168.4.50' not in list_ip:  # 如果没有创建资产
                # todo 改为添加资产
                # resp = AddLogSource(name='192.168.4.50', ip='192.168.4.50').send()
                resp = AddAssetParam(name='192.168.4.50', ip='192.168.4.50').send()
                result = resp.json()
                print(result)
                pytest.assume(result['message'] == '操作成功')
            time.sleep(1)
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.50|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip, local_ip))
            time.sleep(30)
            self.logging.info('查看逻辑拓扑列表')
            resp = LogicTopo().send()
            result = resp.json()
            print(result)
            # pytest.assume(result['data']['list'][0]['status'] == 3)
            self.logging.info('查看告警检索-产生日志')
            resp = AlarmRetrieval().send()
            result = resp.json()
            print(result)
            data = result['data']['list'][0]
            pytest.assume(
                data['alarmStartTime'].split(' ')[0] == str(datetime.datetime.now().strftime("%Y-%m-%d")))  # 判断时间
            pytest.assume(data['alarmLevel'] == '一般')  # 告警级别
            pytest.assume(data['alarmSecondaryType'] == '用户行为告警/非法外联')  # 告警类型
            pytest.assume(data['factoryName'] == 'XX区域')  # 区域
            pytest.assume(data['alarmPrimaryMessage'] == '网络中出现了非法连接的资产。')  # 告警描述
            pytest.assume(
                data['warmSuggest'] == '请确认主机所属区域是否允许外部连接；如果不允许请停止外部连接处理；如果允许可以对相关规则进行配置不产生此类告警信息')  # 告警类型
            self.logging.info('未知设备接入')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.75|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip, local_ip))
            time.sleep(30)
            self.logging.info('查看逻辑拓扑列表')
            resp = LogicTopo().send()
            result = resp.json()
            print(result)

            # pytest.assume(result['data']['list'][0]['status'] == 4)
            status = [4, 3, 2, 1]  # 判断所有的拓朴类型
            status_list = []  # 拓朴状态
            for i in result['data']['list']:
                # for index, i in enumerate(result['data']['list']):
                status_list.append(i['status'])
            print(status_list)
            for i in status:
                pytest.assume(i in status_list)
            self.logging.info('查看告警检索-产生日志')
            resp = AlarmRetrieval().send()
            result = resp.json()
            print(result)
            data = result['data']['list'][0]
            pytest.assume(
                data['alarmStartTime'].split(' ')[0] == str(datetime.datetime.now().strftime("%Y-%m-%d")))  # 判断时间
            pytest.assume(data['alarmLevel'] == '重要')  # 告警级别
            pytest.assume(data['alarmSecondaryType'] == '用户行为告警/未知设备接入')  # 告警类型
            pytest.assume(data['factoryName'] == 'XX区域')  # 区域
            pytest.assume(data['alarmPrimaryMessage'] == '网络中出现了未知的设备接入。')  # 告警描述
            pytest.assume(
                data['warmSuggest'] == '请确认当前设备所在区域是否允许当前设备进行接入，如果不允许请将当前将设备断开连接，如果允许可以将当前设备加入已确认资产，不产生此类告警信息')  # 告警类型

            self.logging.info('网络基线明细列表查询，获取id-删除接口使用')
            resp = BaselineDetailsList().send()
            result = resp.json()

            if result['data']['list'] != []:
                # id = []
                # print(result['data']['list'][0])
                # for i in result['data']['list']:
                #     id.append(i['id'])
                id = [i['id'] for i in result['data']['list']]
                self.logging.info('删除网络基线明细')
                resp = DeleteBaselineDetails(ids=id).send()
                result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('禁用网络基线')
            resp = NetworkBaseline(status=2).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('恢复xx区域配置')
            mod = ModAera(value, factoryIpScope='')
            resp = mod.send()
            result = resp.json()
            print(result)
            pytest.assume(result['statusCode'] == 200)
            # self.logging.info('查看日志源列表，删除日志源')
            # 删除资产
            # resp = GetAsset().send()
            # result = resp.json()
            # asset_list = result['data']['list']  # 资产列表
            # ids = [i['id'] for i in asset_list if
            #        i['ip'] == '192.168.5.5' or i['ip'] == '192.168.4.50']
            # print(ids)
            # resp = DeleteAsset(id=ids).send()
            # result = resp.json()
            # pytest.assume(result['message'] == '操作成功')
        except Exception:
            raise Exception
        finally:
            self.logging.info('关闭非法外联流')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.10.65|^网络会话|^2021-06-03 16:28:37|^17|^192.168.10.65|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    IP))
            self.logging.info('关闭跨区通信流')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.5.5|^网络会话|^2021-06-03 16:28:37|^17|^192.168.5.5|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip))
            self.logging.info('关闭非法连接流')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.50|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip, local_ip))
            self.logging.info('关闭未知设备接入流')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.75|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip, local_ip))

    @allure.story('横向威胁态势')
    @allure.title('ISA-2432、ISA-3256')
    def test_horizontal_threat_posture(self):
        self.logging.info('查看区域管理列表')
        resp = AeraQuery().send()
        result = resp.json()
        print(result)
        mod_value = result['data'][0]['children'][0]['value']  # xx区域value值
        self.logging.info('修改xx区域')
        mod = ModAera(mod_value)
        resp = mod.send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)
        self.logging.info('开启默认网络基线')
        resp = NetworkBaseline().send()
        result = resp.json()
        print(result)
        pytest.assume(result['status'] == True)
        self.logging.info('非法外联')
        syslog(
            '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.10.65|^网络会话|^2021-06-03 16:28:37|^17|^192.168.10.65|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                IP))

        self.logging.info('未知设备接入')
        syslog(
            '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.75|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                local_ip, local_ip))
        time.sleep(20)

        self.logging.info('逻辑拓扑详情列表')
        resp = LogicTopo().send()
        result = resp.json()
        print(result['data']['list'][0])
        data = result['data']['list'][0]
        linkId = data['linkId']
        srcIp = data['srcIp']
        srcFactoryId = data['srcFactoryId']
        dstFactoryId = data['dstFactoryId']
        dstIp = data['dstIp']
        time.sleep(1)
        self.logging.info('加入基线')
        resp = BaselineDetailsList().send()  # 网络基线明细列表
        result = resp.json()
        print(result['data']['list'])
        if result['data']['list'] == []:
            resp = AddToBaseline(srcIp=srcIp, srcFactoryId=srcFactoryId, dstIp=dstIp, dstFactoryId=dstFactoryId,
                                 linkId=linkId).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
        time.sleep(5)
        self.logging.info('横向威胁态势页')
        resp = HorizontalThreatPosturePage().send()
        result = resp.json()
        print(result)
        assetCount = result['data']['assetCount']  # 已确认资产数
        normalConn = result['data']['normalConn']  # 正常横向访问连接数
        abnormalConn = result['data']['abnormalConn']  # 异常横向访问连接数
        unknownConn = result['data']['unknownConn']  # 非法外联告警
        normalConnTop5 = result['data']['normalConnTop5']  # 资产正常横向访问Top5
        threatConnTop5 = result['data']['threatConnTop5']  # 资产横向威胁访问Top5
        unknownConnTop5 = result['data']['unknownConnTop5']  # 非法外联告警Top5
        normalConnProtPie = result['data']['normalConnProtPie']  # 资产横向访问协议Top5
        threatConnProtPie = result['data']['threatConnProtPie']  # 资产横向威胁访问协议Top5
        connTypePie = result['data']['connTypePie']  # 逻辑拓扑连接类型占比
        self.logging.info('已确认资产数')
        resp = GetAssetList().send()
        result = resp.json()
        print(result)
        print('已确认资产数', result)
        print(result['data']['total'], assetCount)
        pytest.assume(result['data']['total'] == assetCount)  # 判断已确认资产数相同
        self.logging.info('正常横向访问连接数-正常逻辑拓扑')
        resp = LogicTopo(status=0).send()
        result = resp.json()
        print('正常横向访问连接数', result)
        print(result['data']['total'], normalConn)
        pytest.assume(result['data']['total'] == normalConn)
        self.logging.info('异常横向访问连接数-异常逻辑拓扑')
        resp = LogicTopoEcxept().send()
        result = resp.json()
        print('异常横向访问连接数', result)
        print(result['data']['total'], abnormalConn)
        pytest.assume(result['data']['total'] == abnormalConn)
        self.logging.info('非法外联告警')
        resp = AlarmRetrievalQuery().send()
        result = resp.json()
        print('非法外联告警', result)
        print(result['data']['total'], unknownConn)
        pytest.assume(result['data']['total'] == unknownConn)
        self.logging.info('资产正常横向访问Top5')
        if normalConnTop5 != []:  # 如果不为空，判断跳转后是否一致
            for i in normalConnTop5:
                name = i['name']
                value = i['value']
                resp = LogicTopo(ip=name, status=0).send()
                result = resp.json()
                print('资产正常横向访问Top5', result)
                print(result['data']['total'], value)
                pytest.assume(result['data']['total'] == value)
        self.logging.info('资产横向威胁访问Top5')
        if threatConnTop5 != []:  # 如果不为空，判断跳转后是否一致
            for i in threatConnTop5:
                name = i['name']
                value = i['value']
                resp = LogicTopoEcxept(ip=name).send()
                result = resp.json()
                print('资产横向威胁访问Top5', result)
                print(result['data']['total'], value)
                pytest.assume(result['data']['total'] == value)
        self.logging.info('非法外联告警Top5')
        if unknownConnTop5 != []:  # 如果不为空，判断跳转后是否一致
            for i in unknownConnTop5:
                name = i['name']
                value = i['value']
                alarm = AlarmRetrieval()
                alarm.json = {"keyword": "", "factory": 2, "safeDeviceIp": name, "alarmType": 30000100,
                              "alarmTypeArr": [30000000, 30000100], "alarm_filter": True, "actionStatus": '',
                              "startPage": 1, "pageSize": 10}
                resp = alarm.send()
                result = resp.json()
                print('非法外联告警Top5', result)
                print(result['data']['total'], value)
                pytest.assume(result['data']['total'] == value)
        self.logging.info('资产横向访问协议Top5')
        if normalConnProtPie != []:  # 如果不为空，判断跳转后是否一致
            for i in normalConnProtPie:
                port = i['port']
                value = i['value']
                transportProtocol = i['transportProtocol']
                topo = LogicTopoUsual()
                topo.json = {"pageSize": 10, "startPage": 1, "ip": "", "factoryId": 2, "status": 0,
                             "port": port, "transportProtocol": transportProtocol}
                resp = topo.send()
                result = resp.json()
                print('资产横向访问协议Top5', result)
                print(result['data']['total'], value)
                pytest.assume(result['data']['total'] == value)
        self.logging.info('资产横向威胁访问协议Top5')
        if threatConnProtPie != []:  # 如果不为空，判断跳转后是否一致
            for i in threatConnProtPie:
                port = i['port']
                value = i['value']
                transportProtocol = i['transportProtocol']
                topo = LogicTopoUsual()
                topo.json = {"pageSize": 10, "startPage": 1, "ip": "", "factoryId": 2, "exceptOk": True,
                             "port": port, "transportProtocol": transportProtocol}
                resp = topo.send()
                result = resp.json()
                print('资产横向威胁访问协议Top5', result)
                print(result['data']['total'], value)
                pytest.assume(result['data']['total'] == value)
        self.logging.info('逻辑拓扑连接类型占比')
        if connTypePie != []:  # 如果不为空，判断跳转后是否一致
            for i in connTypePie:
                name = i['name']
                value = i['value']
                status = ''
                if name == '正常':
                    status = 0
                if name == '非法外联':
                    status = 1
                if name == '跨区通信':
                    status = 2
                if name == '非法连接':
                    status = 3
                if name == '未知设备接入':
                    status = 4
                resp = LogicTopo(status=status).send()
                print(LogicTopo(status=status).json)
                result = resp.json()
                print('逻辑拓扑连接类型占比', result)
                print(result['data']['total'], value)
                pytest.assume(result['data']['total'] == value)
        self.logging.info('网络基线明细列表查询，获取id-删除接口使用')
        resp = BaselineDetailsList().send()
        result = resp.json()
        print(result['data']['list'])
        if result['data']['list'] != []:
            id = []
            for i in result['data']['list']:
                id.append(i['id'])
            self.logging.info('删除网络基线明细')
            resp = DeleteBaselineDetails(ids=id).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
        self.logging.info('恢复xx区域配置')
        mod = ModAera(mod_value, factoryIpScope='')
        resp = mod.send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)
        self.logging.info('禁用网络基线')
        resp = NetworkBaseline(status=2).send()
        result = resp.json()
        pytest.assume(result['message'] == '操作成功')

    @allure.story('拓扑管理-逻辑拓扑')
    @allure.title('ISA-2689')
    def test_add_baseline(self):
        """
        ISA-2689 : 非正常节点右键-添加基线，异常节点添加到网络基线中，节点和线变为绿色
        1 鼠标右键非法外联节点B，点击添加基线  添加基线成功
        2 在拓扑图中查看节点B的颜色  节点B变为绿色，即 变为正常节点
        3 鼠标右键跨区通信节点C，点击添加基线  添加基线成功
        4 在拓扑图中查看节点C的颜色  节点C变为绿色，即 变为正常节点
        5 鼠标右键非法连接节点D，点击添加基线  添加基线成功
        6 在拓扑图中查看节点D的颜色  节点D变为绿色，即 变为正常节点
        7 鼠标右键未知设备接入节点E，点击添加基线  添加基线成功
        8 在拓扑图中查看节点E的颜色  节点E变为绿色，即 变为正常节点
        """
        try:
            self.logging.info('查看区域管理列表')
            resp = AeraQuery().send()
            result = resp.json()
            print(result)
            value = result['data'][0]['children'][0]['value']  # xx区域value值
            self.logging.info('修改xx区域')
            mod = ModAera(value)
            resp = mod.send()
            result = resp.json()
            print(result)
            pytest.assume(result['statusCode'] == 200)
            self.logging.info('开启默认网络基线')
            resp = NetworkBaseline().send()
            result = resp.json()
            print(result)
            self.logging.info('非法外联')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.10.65|^网络会话|^2021-06-03 16:28:37|^17|^192.168.10.65|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    IP))

            self.logging.info('跨区通信')
            self.logging.info('查看区域列表')
            resp = AeraQuery().send()
            result = resp.json()
            print(result)
            data = result['data'][0]['children']  # xx集团子区域
            area_list = []
            for i in data:
                area_list.append(i['label'])
            if 'test' not in area_list:
                resp = AddAera(factoryIpScope='192.168.5.1-192.168.5.7').send()
                result = resp.json()
                print(result)
                pytest.assume(result['message'] == '操作成功')
            self.logging.info('查看日志源列表')
            resp = LogSourcePage().send()
            result = resp.json()
            print(result)
            log_source_list = result['data']['logSourceList']['list']  # 日志源数据
            list_ip = [i['assetIp'] for i in log_source_list]
            self.logging.info('查看区域列表')
            resp = AeraQuery().send()
            result = resp.json()
            print(result)
            vaule = result['data'][0]['children'][1]['value']
            if '192.168.5.5' not in list_ip:  # 如果没有创建资产
                # resp = AddLogSource(name='192.168.5.5', ip='192.168.5.5', factory=vaule).send()
                resp = AddAssetParam(name='192.168.5.5', ip='192.168.5.5', factoryId=vaule).send()
                result = resp.json()
                print(result)
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.5.5|^网络会话|^2021-06-03 16:28:37|^17|^192.168.5.5|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip))

            self.logging.info('非法连接')
            self.logging.info('查看资产列表')
            resp = GetList().send()
            result = resp.json()
            print(result)
            asset_list = result['data']['list']  # 资产数据
            list_ip = [i['ip'] for i in asset_list]
            if '192.168.4.50' not in list_ip:  # 如果没有创建资产
                # resp = AddLogSource(name='192.168.4.50', ip='192.168.4.50').send()
                resp = AddAssetParam(name='192.168.4.50', ip='192.168.4.50').send()
                result = resp.json()
                print(result)
                pytest.assume(result['message'] == '操作成功')
            time.sleep(1)
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.50|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip, local_ip))
            # todo 增加新的正常数据的逻辑拓扑；
            self.logging.info('未知设备接入')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.75|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip, local_ip))
            time.sleep(30)
            self.logging.info('查看逻辑拓扑列表')
            resp = LogicTopo().send()
            result = resp.json()
            print(result)

            status = [4, 3, 2, 1]  # 判断所有的拓朴类型
            # status_list = []  # 拓朴状态
            # for i in result['data']['list']:
            #     # for index, i in enumerate(result['data']['list']):
            #     status_list.append(i['status'])
            status_list = [i['status'] for i in result['data']['list']]
            print(status_list)
            for i in status:
                pytest.assume(i in status_list)
            self.logging.info('逻辑拓扑详情列表')
            resp = LogicTopo().send()
            result = resp.json()
            print(result['data']['list'])
            data_list = result['data']['list']
            if result['data']['list'] != []:
                for data in data_list:
                    linkId = data['linkId']
                    srcIp = data['srcIp']
                    srcFactoryId = data['srcFactoryId']
                    dstFactoryId = data['dstFactoryId']
                    dstIp = data['dstIp']
                    time.sleep(1)
                    self.logging.info('加入基线')
                    resp = BaselineDetailsList().send()  # 网络基线明细列表
                    result = resp.json()
                    print(result['data']['list'])
                    resp = AddToBaseline(srcIp=srcIp, srcFactoryId=srcFactoryId, dstIp=dstIp, dstFactoryId=dstFactoryId,
                                         linkId=linkId).send()
                    # print(AddToBaseline(srcIp=srcIp, srcFactoryId=srcFactoryId, dstIp=dstIp, dstFactoryId=dstFactoryId,
                    #                     linkId=linkId).json)
                    result = resp.json()
                    pytest.assume(result['message'] == '操作成功')
            self.logging.info('查看逻辑拓扑列表')
            resp = LogicTopo().send()
            result = resp.json()
            print(result)
            status_list = [i['status'] for i in result['data']['list']]
            print(status_list)
            for i in status_list:
                pytest.assume(i == 0)
            time.sleep(5)
            # todo 操作日志容易导致失败
            # self.logging.info('audit查看操作日志')
            # header = login_test(audit, password)
            # log = OperatorLog()
            # log.headers = header
            # resp = log.send()
            # result = resp.json()
            # print(result)
            # data_list = result['data']['list'][1:5]
            # value_list = ['模块[逻辑拓扑图]，基线[默认网络基线]，添加明细数据[192.168.5.5-192.168.4.173] 成功']
            # for index, data in enumerate(data_list):
            #     print(data['context'], value_list[index])
            #     pytest.assume(data['context'] == value_list[index])
        except Exception:
            raise Exception
        finally:
            self.logging.info('网络基线明细列表查询，获取id-删除接口使用')
            resp = BaselineDetailsList().send()
            result = resp.json()
            if result['data']['list'] != []:
                id = [i['id'] for i in result['data']['list']]
                self.logging.info('删除网络基线明细')
                resp = DeleteBaselineDetails(ids=id).send()
                result = resp.json()
                pytest.assume(result['message'] == '操作成功')
            self.logging.info('禁用网络基线')
            resp = NetworkBaseline(status=2).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('查看资产列表，删除资产')
            resp = GetList().send()
            result = resp.json()
            asset_list = result['data']['list']  # 资产列表
            ids = [i['id'] for i in asset_list if
                   i['ip'] == '192.168.5.5' or i['ip'] == '192.168.4.50']
            print(ids)
            resp = DeleteAsset(id=ids).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('恢复xx区域配置')
            mod = ModAera(value, factoryIpScope='')
            resp = mod.send()
            result = resp.json()
            print(result)
            pytest.assume(result['statusCode'] == 200)
            self.logging.info('关闭非法外联流')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.10.65|^网络会话|^2021-06-03 16:28:37|^17|^192.168.10.65|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    IP))
            self.logging.info('关闭跨区通信流')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.5.5|^网络会话|^2021-06-03 16:28:37|^17|^192.168.5.5|^|^64760|^{}|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip))
            self.logging.info('关闭非法连接流')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.50|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip, local_ip))
            self.logging.info('关闭未知设备接入流')
            syslog(
                '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.75|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                    local_ip, local_ip))

    @allure.story('拓扑管理-逻辑拓扑')
    @allure.title('逻辑拓扑流量状态 ISA-2562、ISA-2563、ISA-2564')
    def test_network_session_traffic_status(self):
        self.logging.info('查看区域管理列表')
        resp = AeraQuery().send()
        result = resp.json()
        print(result)
        value = result['data'][0]['children'][0]['value']  # xx区域value值
        self.logging.info('修改xx区域')
        mod = ModAera(value)
        resp = mod.send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)
        self.logging.info('开启默认网络基线')
        resp = NetworkBaseline().send()
        time.sleep(1)
        self.logging.info('未知设备接入-流量状态为1')
        resp = LogicTopo().send()  # 查看逻辑拓扑图明细列表
        result = resp.json()
        print(result)
        total = result['data']['total']
        syslog(
            '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.153|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^1|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                local_ip, local_ip))
        time.sleep(5)
        resp = LogicTopo().send()  # 查看逻辑拓扑图明细列表
        result = resp.json()
        print(result)
        total_one = result['data']['total']
        # pytest.assume(int(total_one) - 1 == int(total))
        resp = LogicTopo(ip=local_ip, status=4).send()  # 根据资产ip和状态搜索
        result = resp.json()
        data = result['data']['list'][0]  # 判断第一条数据
        print(data)
        pytest.assume(data['srcIp'] == local_ip and data['dstIp'] == '192.168.4.153' and data['status'] == 4)
        self.logging.info('未知设备接入-流量状态为2')
        syslog(
            '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.153|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^2|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                local_ip, local_ip))
        time.sleep(5)
        resp = LogicTopo().send()  # 查看逻辑拓扑图明细列表
        result = resp.json()
        print(result)
        total_two = result['data']['total']
        pytest.assume(int(total_one) == int(total_two))
        self.logging.info('未知设备接入-流量状态为3')
        syslog(
            '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.153|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
                local_ip, local_ip))
        time.sleep(30)

        resp = LogicTopo().send()  # 查看逻辑拓扑图明细列表
        result = resp.json()
        total_three = result['data']['total']
        pytest.assume(int(total_two) - 1 == int(total_three))
        self.logging.info('日志检索查看发送的日志信息')
        resp = LogRetrieve().send()
        result = resp.json()
        pytest.assume(result['dataList'][0][
                          'originlog'] == '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^{}|^网络会话|^2021-06-03 16:28:37|^17|^{}|^|^64760|^192.168.4.153|^|^5350|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'.format(
            local_ip, local_ip))
        print(result)
        self.logging.info('禁用网络基线')
        resp = NetworkBaseline(status=2).send()
        self.logging.info('恢复xx区域配置')
        mod = ModAera(value, factoryIpScope='')
        resp = mod.send()
        result = resp.json()
        print(result)
        pytest.assume(result['statusCode'] == 200)

    @allure.story('资产管理-已确认资产-新增修改资产')
    @allure.title('ISA-1907')
    def test_edit_field_add_asset(self):
        """
        ISA-1907 :编辑字段信息为添加资产时填写的信息
        1 选中一个资产，点击编辑资产   弹出编辑资产页面,页面回显资产信息
        2 手动编辑输入归属单位，归属专业，归属系统，主机名，物理端口编号，注册时间，资产业务价值，资产机密性，资产完整性，资产可用性，安全责任人,输入其他必填项并保存,查看新增资产信息
        列表中： 归属单位，归属专业，归属系统，主机名，物理端口编号，注册时间，资产业务价值，资产机密性，资产完整性，资产可用性、安全责任人  显示为编辑资产时手动填写的信息
        """
        try:
            with allure.step('1 选中一个资产，点击编辑资产   弹出编辑资产页面,页面回显资产信息'):
                add = AddAsset()  # 新增资产
                add.json = {
                    "alias": "",
                    "assetAvailability": '',
                    "assetBusinessValue": "3",
                    "assetConfidentiality": '',
                    "assetIntegrity": '',
                    "belongProfessiona": "",
                    "belongingSystem": "",
                    "belongingUnit": "",
                    "deviceVersion": "",
                    "factoryId": 3,
                    "hasGuard": "",
                    "hostName": "",
                    "ip": "192.168.56.3",
                    "ipMacs": [],
                    "loginTime": "2022-02-01 00:00:00",
                    "mac": "",
                    "modelId": "",
                    "name": "test1",
                    "operateSystem": "",
                    "physicalPortNumber": "",
                    "safetyResponsiblePerson": "",
                    "serialNumber": "",
                    "typeId": "",
                    "values": [],
                    "vendorId": ""
                }
                resp = add.send()
                result = resp.json()
                print(result)
                assert result['message'] == '操作成功'
            with allure.step(
                    '2 手动编辑输入归属单位，归属专业，归属系统，主机名，物理端口编号，注册时间，资产业务价值，资产机密性，资产完整性，资产可用性，安全责任人,输入其他必填项并保存,查看新增资产信息'):
                id_dict = self.db.select("select id from soc.soc_asset_info where ip='192.168.56.3'")
                id = id_dict[0]['id']
                mod = ModAsset()  # 修改资产
                mod.json = {"id": id, "ip": "192.168.56.3", "name": "test1", "modelId": '', "factoryId": 3, "mac": "",
                            "alias": "", "serialNumber": "", "deviceVersion": "", "hasGuard": 0, "operateSystem": "",
                            "ipMacs": [], "typeId": 409999, "vendorId": '', "belongingUnit": "test1",
                            "belongProfessiona": "test1", "belongingSystem": "test1", "hostName": "test1",
                            "physicalPortNumber": "123", "loginTime": "2022-02-01 00:00:00", "assetBusinessValue": 3,
                            "assetConfidentiality": 1, "assetIntegrity": 1, "assetAvailability": 1,
                            "safetyResponsiblePerson": "test1", "values": []}
                resp = mod.send()
                result = resp.json()
                assert result['message'] == '操作成功'
                resp = RecognizedAssetsList(keyword='192.168.56.3').send()
                result = resp.json()
                with allure.step('列表中： 归属单位，归属专业，归属系统，主机名，物理端口编号，注册时间，资产业务价值，资产机密性，资产完整性，资产可用性、安全责任人  显示为编辑资产时手动填写的信息'):
                    print(result)
                    value = result['data']['list'][0]
                    assert value['belongingUnit'] == 'test1' and value['belongProfessiona'] == 'test1' and value[
                        'belongingSystem'] == 'test1' and value['hostName'] == 'test1' and value[
                               'physicalPortNumber'] == '123' and \
                           value['assetBusinessValue'] == 3 and value['assetConfidentiality'] == 1 and value[
                               'assetIntegrity'] == 1 and value['assetAvailability'] == 1 and value[
                               'safetyResponsiblePerson'] == 'test1'
        except Exception:
            raise Exception
        finally:
            resp = DeleteAsset(id=[id]).send()

    @allure.story('资产管理-已确认资产-查询条件')
    @allure.title('ISA-1909')
    def test_filter_assets_business_value_assets(self):
        """
        ISA-1909 : 【建议自动化-低】可根据资产业务价值筛选资产
        1 点击“筛选”，选择资产业务价值为1进行查询  列表筛选出资产业务价值为1的资产
        2 点击“筛选”，选择资产业务价值为2进行查询  列表筛选出资产业务价值为2的资产
        3 点击“筛选”，选择资产业务价值为3进行查询  列表筛选出资产业务价值为3的资产
        4 点击“筛选”，选择资产业务价值为4进行查询  列表筛选出资产业务价值为4的资产
        5 点击“筛选”，选择资产业务价值为5进行查询  列表筛选出资产业务价值为5的资产
        """
        try:
            add = AddAsset()  # 新增资产
            for i in range(1, 6):
                add.json = {
                    "alias": "",
                    "assetAvailability": '',
                    "assetBusinessValue": f"{i}",
                    "assetConfidentiality": '',
                    "assetIntegrity": '',
                    "belongProfessiona": "",
                    "belongingSystem": "",
                    "belongingUnit": "",
                    "deviceVersion": "",
                    "factoryId": 3,
                    "hasGuard": "",
                    "hostName": "",
                    "ip": f"192.168.55.{i}",
                    "ipMacs": [],
                    "loginTime": "2022-02-01 00:00:00",
                    "mac": "",
                    "modelId": "",
                    "name": f"test{i}",
                    "operateSystem": "",
                    "physicalPortNumber": "",
                    "safetyResponsiblePerson": "",
                    "serialNumber": "",
                    "typeId": "",
                    "values": [],
                    "vendorId": ""
                }
                resp = add.send()
                result = resp.json()
                print(result)
                assert result['message'] == '操作成功'
            time.sleep(1)
            filter = AssetFilter()  # 筛选
            for i in range(1, 6):
                filter.json = {"typeId": "", "belongingUnit": "", "belongProfessiona": "", "belongingSystem": "",
                               "hostName": "", "physicalPortNumber": "", "loginTime": "", "assetBusinessValue": f"{i}",
                               "assetConfidentiality": "", "assetIntegrity": "", "assetAvailability": "",
                               "safetyResponsiblePerson": "", "values": [], "startPage": 1, "pageSize": 10,
                               "keyword": ""}
                resp = filter.send()
                result = resp.json()
                print(result)
                values = result['data']['list']
                for value in values:
                    assert value['assetBusinessValue'] == i
        except Exception:
            raise Exception
        finally:
            id_dict = self.db.select(
                "select id from soc.soc_asset_info where ip in('192.168.55.1','192.168.55.2','192.168.55.3','192.168.55.4','192.168.55.5')")
            id_list = [id['id'] for id in id_dict]
            resp = DeleteAsset(id=id_list).send()

    @allure.story('资产管理-已确认资产-导出与导入资产')
    @allure.title('ISA-3495')
    def test_import_asset_field_correct(self):
        """
        ISA-3495 : 导入资产时，新增字段内容为导入文件中填写的内容
        1 资产模板中输入主机名，物理端口编号，资产机密性，资产完整性，资产可用性，安全责任人、
        归属单位，归属专业，归属系统，主机名，物理端口编号，注册时间，资产机密性，资产完整性，资产可用性，安全责任人 其他必填项均正确输入 通过“导入资产”导入文件
        资产导入成功
        2 查看导入资产信息 字段为资产导入文件中填写的内容
        """
        try:
            with allure.step('步骤1'):
                resp = ImportAssetExcel(file='资产模版.xlsx').send()
                result = resp.json()
                print(result)
                with allure.step('资产导入成功'):
                    assert result['message'] == '操作成功'
            with allure.step('查看导入资产信息'):
                resp = GetList(keyword='192.168.3.12').send()
                result = resp.json()
                print(result)
                data = result['data']['list'][0]
                with allure.step('字段为资产导入文件中填写的内容'):
                    assert data['name'] == '导入' and data['alias'] == '导入1' and data['factoryName'] == 'XX区域' and data[
                        'belongingUnit'] == '导入' and data['belongProfessiona'] == '导入' and data[
                               'belongingSystem'] == '导入' and data['hostName'] == '192.168.3.12' and data[
                               'assetBusinessValue'] == 3 and data['safetyResponsiblePerson'] == '导入'

        except Exception:
            raise Exception
        finally:
            with allure.step('查看导入资产信息'):
                # 删除导入的资产
                id_dict = self.db.select("select id FROM `soc`.`soc_asset_info` where ip='192.168.3.12'")
                id = [id['id'] for id in id_dict]
                resp = DeleteAsset(id=id).send()
                result = resp.json()
                print(result)
                assert result['message'] == '操作成功'

    @allure.story('资产管理-属性管理-新增属性')
    @allure.title('ISA-2455')
    def test_add_field(self):
        """
        ISA-2455 : 新增属性
        1 点击新增 弹出新增属性弹窗
        2 输入“属性名称”、“属性类型” 点击保存  属性保存成功
        """
        try:
            with allure.step('新增,输入“属性名称”、“属性类型” 点击保存'):
                resp = AddAttributes().send()
                result = resp.json()
                print(result)
                with allure.step('属性保存成功'):
                    assert result['message'] == '新增属性成功'
        except Exception:
            raise Exception
        finally:
            with allure.step('删除新增属性'):
                id_dict = self.db.select("select id FROM `soc`.`soc_asset_attribute` where name='test字符串'")
                id = [id['id'] for id in id_dict]
                print(id)
                resp = BatchDeleteAttributes(id=id).send()

                result = resp.json()
                print(result)
                assert result['message'] == '删除属性成功'

    @allure.story('资产管理-属性管理-新增属性')
    @allure.title('ISA-2456')
    def test_mod_field(self):
        """
        ISA-2456 : 编辑属性
        1 选择一个属性，点击编辑  弹出编辑属性弹窗
        2 修改“属性名称”,点击保存  属性名称修改成功
        """
        try:
            with allure.step('1 新增一个属性，选择一个属性，点击编辑'):
                resp = AddAttributes().send()
                result = resp.json()
                print(result)
                with allure.step('属性保存成功'):
                    assert result['message'] == '新增属性成功'
            with allure.step('2 修改“属性名称”,点击保存'):
                id_dict = self.db.select("select id from soc.soc_asset_attribute where name='test字符串'")
                id = id_dict[0]['id']
                resp = ModAttributes(id=id).send()  # 修改属性
                result = resp.json()
                print(result)
                assert result['message'] == '编辑属性成功'
                with allure.step('属性名称修改成功'):
                    resp = AttributesList().send()  # 属性列表页
                    result = resp.json()
                    print(result)
                    assert result['data']['list'][0]['name'] == 'test1'

        except Exception:
            raise Exception
        finally:
            BatchDeleteAttributes(id=[id]).send()  # 删除属性

    @allure.story('资产管理-漏洞管理-漏洞记录-资产匹配漏洞逻辑优化')
    @allure.title('ISA-2725')
    def test_switch_open_match_vulnerability_library(self):
        """
        ISA-2725 : 【建议自动化-中】打开“是否匹配漏洞”开关，资产会匹配漏洞库的数据
        1
        1.进入 资产中心--资产管理--已确认资产 页面，点击<新增资产>按钮，
        2.输入添加的资产 ip：192.168.4.193，操作系统：microsoft windows server 2008 sp2
        3.其他参数合规，点击<确定>按钮
        1.新增资产成功
        2.【漏洞记录】页面，该资产和漏洞库中的信息匹配成功，展示该系统下对应的所有漏洞
        2 通过“资产导入”、“雷达扫描”、“资产同步”等方式导入操作系统为“microsoft windows server 2008 sp2”的资产
        【漏洞记录】页面，该资产和漏洞库中的信息匹配成功，展示该系统下对应的所有漏洞
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
                        "operateSystem": "microsoft windows server 2008 sp2", "ipMacs": [], "typeId": "",
                        "vendorId": "",
                        "belongingUnit": "", "belongProfessiona": "", "belongingSystem": "", "hostName": "",
                        "physicalPortNumber": "", "loginTime": "", "assetBusinessValue": "3",
                        "assetConfidentiality": "",
                        "assetIntegrity": "", "assetAvailability": "", "safetyResponsiblePerson": "", "values": []}
            resp = add.send()
            result = resp.json()
            print(result)
            id = result['data']['id']
            pytest.assume(result['message'] == '操作成功')
            # 查看漏洞分布
            time.sleep(2)
            resp = VulnerabilityDistributionPage().send()
            result = resp.json()
            print(result)
            vul_total_one = result['data']['totalSize']  # 分布记录总数

            # pytest.assume(
            #     'vulName' in value and 'vulLevelName' in value and 'cve' in value and 'cnvd' in value and 'cnnvd' in value and 'vulTypeName' in value and 'vulReleaseTime' in value and 'icsName' in value and 'amount' in value and 'proportion' in value)
            # 删除资产
            delete = DeleteAsset()
            delete.json = {"ids": [id]}
            resp = delete.send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            # 资产导入
            resp = ImportAssetExcel(file='资产原始数据.xlsx').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            # 查看漏洞分布
            time.sleep(2)
            resp = VulnerabilityDistributionPage().send()
            result = resp.json()
            print(result)
            vul_total_two = result['data']['totalSize']  # 分布记录总数
            pytest.assume(vul_total_one == vul_total_two)
            # 删除资产
            id_idct = self.db.select("select id from soc.soc_asset_info where ip='192.168.0.202'")
            id = id_idct[0]['id']
            delete = DeleteAsset()
            delete.json = {"ids": [id]}
            resp = delete.send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
        except Exception:
            raise Exception
        finally:
            # 关闭漏洞开关
            config.json = {"match": 0}
            resp = config.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '操作成功')

    @allure.story('资产管理-漏洞管理-漏洞记录-资产匹配漏洞逻辑优化')
    @allure.title('ISA-2745')
    def test_switch_close_match_vulnerability_library(self):
        """
        ISA-2745 : 关闭“是否匹配漏洞”开关，资产不会匹配漏洞库的数据
        1
        1.进入 资产中心--资产管理--已确认资产 页面，点击<新增资产>按钮，
        2.输入添加的资产 ip：192.168.4.193，操作系统：microsoft windows server 2008 sp2
        3.其他参数合规，点击<确定>按钮
        1.新增资产成功
        2.【漏洞记录】页面，该资产下没有漏洞信息
        2 点击“导入数据”按钮，导入资产
        1.新增资产成功
        2.【漏洞记录】页面，该导入的资产没有漏洞信息
        3 通过USM上报资产
        备注：audit登录USM，在【Syslog配置】页面，点击<z资产信息发送>按钮，向ISA中上报资产信息
        1.新增资产成功
        2.【漏洞记录】页面，USM上报的资产没有漏洞信息
        """
        try:
            # 新增资产
            add = AddAsset()
            add.json = {"ip": "192.168.0.202", "name": "192.168.0.202", "modelId": "", "factoryId": 3, "mac": "",
                        "alias": "", "serialNumber": "", "deviceVersion": "", "hasGuard": "",
                        "operateSystem": "microsoft windows server 2008 sp2", "ipMacs": [], "typeId": "",
                        "vendorId": "",
                        "belongingUnit": "", "belongProfessiona": "", "belongingSystem": "", "hostName": "",
                        "physicalPortNumber": "", "loginTime": "", "assetBusinessValue": "3",
                        "assetConfidentiality": "",
                        "assetIntegrity": "", "assetAvailability": "", "safetyResponsiblePerson": "", "values": []}
            resp = add.send()
            result = resp.json()
            print(result)
            id = result['data']['id']
            pytest.assume(result['message'] == '操作成功')
            # 查看漏洞分布
            time.sleep(2)
            resp = VulnerabilityDistributionPage().send()
            result = resp.json()
            print(result)
            vul_total_one = result['data']['totalSize']  # 分布记录总数
            pytest.assume(vul_total_one == 0)
            # pytest.assume(
            #     'vulName' in value and 'vulLevelName' in value and 'cve' in value and 'cnvd' in value and 'cnnvd' in value and 'vulTypeName' in value and 'vulReleaseTime' in value and 'icsName' in value and 'amount' in value and 'proportion' in value)
            # 删除资产
            delete = DeleteAsset()
            delete.json = {"ids": [id]}
            resp = delete.send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            # 资产导入
            resp = ImportAssetExcel(file='资产原始数据.xlsx').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            # 查看漏洞分布
            time.sleep(2)
            resp = VulnerabilityDistributionPage().send()
            result = resp.json()
            print(result)
            vul_total_two = result['data']['totalSize']  # 分布记录总数
            pytest.assume(vul_total_two == 0)
            # 删除资产
            id_idct = self.db.select("select id from soc.soc_asset_info where ip='192.168.0.202'")
            id = id_idct[0]['id']
            delete = DeleteAsset()
            delete.json = {"ids": [id]}
            resp = delete.send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
        except Exception:
            raise Exception
        finally:
            pass

    @allure.story('资产管理-漏洞管理-漏洞扫描-调用OEM漏扫设备配置')
    @allure.title('ISA-2889')
    def test_vulnerability_ip_config(self):
        """
        ISA-2889 : 配置扫描器时IP地址的填写
        1 不填写IP地址，其他项符合校验规则
        提示“请输入扫描器地址”；
        2 输入192.168.1.1
        扫描器地址填写成功；
        3 输入中文、英文、特殊字符，其他项符合校验规则
        提示“请输入正确的扫描器地址，如：127.0.0.1”；
        4 输入格式不正确的IP地址，如127.0000.1，其他项符合校验规则
        提示“请输入正确的扫描器地址，如：127.0.0.1”；
        5 输入225.0.0.1
        提示“请输入正确的扫描器地址，如：127.0.0.1”；只能输入1~233开头的IP地址；
        """
        with allure.step("1 不填写IP地址，其他项符合校验规则"):
            resp = ScanTestConnection(ip='').send()
            result = resp.json()
            with allure.step('提示“请输入扫描器地址”'):
                print(result)
                assert result['message'] == 'ip不能为空'
        with allure.step("2 输入192.168.1.1"):
            resp = ScanTestConnection().send()
            result = resp.json()
            with allure.step('扫描器地址填写成功；'):
                print(result)
                assert result['message'] == '连接成功！'
        with allure.step("3 输入中文、英文、特殊字符，其他项符合校验规则"):
            resp = ScanTestConnection(ip='as测试！@#').send()
            result = resp.json()
            with allure.step('提示“请输入正确的扫描器地址，如：127.0.0.1”；'):
                print(result)
                assert result['message'] == '[as测试！@#]请输入正确的ip，如127.0.0.1'
        with allure.step("4 输入格式不正确的IP地址，如127.0000.1，其他项符合校验规则"):
            resp = ScanTestConnection(ip='127.0000.1').send()
            result = resp.json()
            with allure.step('提示“请输入正确的扫描器地址，如：127.0.0.1”；'):
                print(result)
                assert result['message'] == '[127.0000.1]请输入正确的ip，如127.0.0.1'
        with allure.step("5 输入225.0.0.1"):
            resp = ScanTestConnection(ip='225.0.0.1').send()
            result = resp.json()
            with allure.step('提示“请输入正确的扫描器地址，如：127.0.0.1”；只能输入1~233开头的IP地址；'):
                print(result)
                assert result['message'] == '连接服务器失败，请确认漏洞扫描器状态'

    @allure.story('资产管理-漏洞管理-漏洞扫描-调用OEM漏扫设备配置')
    @allure.title('ISA-2890')
    def test_vulnerability_test_connect(self):
        """
        ISA-2890 : 点击“测试链接”按钮的响应效果
        1 所有项填写符合校验规则，点击测试连接，连接失败  提醒“链接服务器失败,请确认漏洞扫描器状态”；
        2 所有项填写符合校验规则，点击测试链接，连接成功  提醒“连接成功”；

        """
        with allure.step("1 所有项填写符合校验规则，点击测试连接，连接失败"):
            resp = ScanTestConnection(ip='225.0.0.1').send()
            result = resp.json()
            with allure.step('提醒“链接服务器失败,请确认漏洞扫描器状态”'):
                print(result)
                assert result['message'] == '连接服务器失败，请确认漏洞扫描器状态'
        with allure.step("2 所有项填写符合校验规则，点击测试链接，连接成功"):
            resp = ScanTestConnection().send()
            result = resp.json()
            with allure.step('提醒“连接成功”'):
                print(result)
                assert result['message'] == '连接成功！'

    @allure.story('资产管理-风险评分配置-新增资产风险评分配置菜单')
    @allure.title('ISA-2734')
    def test_restoring_weight_configuration(self):
        """
        ISA-2734 : 恢复默认可将权重配置恢复成默认比例
        进入“资产中心-资产管理-风险评分配置”  修改权重比例为442
        1 点击“恢复默认”按钮  查看评分配置
        评分配置状态恢复成3：4：3
        """
        with allure.step('进入“资产中心-资产管理-风险评分配置”  修改权重比例为442'):
            resp = RiskScore(vul=4, threat=4, compliant=2).send()
            result = resp.json()
            print(result)
            assert result['message'] == '操作成功'
        with allure.step('点击“恢复默认”按钮  查看评分配置'):
            resp = RiskScoreReset().send()
            result = resp.json()
            print(result)
            with allure.step('评分配置状态恢复成3：4：3'):
                assert result['message'] == '操作成功' and result['param'] == ["3", "4", "3"]


@allure.feature('系统案例-合规分析')
class TestComplianceAnalys:
    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    @allure.story('通过USM上报数据进行合格评估')
    @allure.title('ISA-3376')
    def test_after_mod_score_calculate_score(self):
        """
        ISA-3376 : 手动修改评估结果之后重新计算合规评分
        1 查看合规评估详情 手动将评估结果修改为不合规
        页面立即保存
        2 查看资产合规评分  根据修改后的结果重新计算合规评分
        """
        try:
            with allure.step('1 查看合规评估详情 手动将评估结果修改为不合规'):
                resp = ComplianceTaskAdd().send()  # 新增合规评估
                result = resp.json()
                print(result)
                assert result['message'] == '操作成功'
                time.sleep(1)
                id_dict = self.db.select("select id FROM `soc`.`soc_compliance_task`")
                task_id = id_dict[0]['id']
                value_dict = self.db.select(
                    "select id,first_code,second_code,third_code,third_result FROM `soc`.`soc_factory_compliance_item_third` where first_name='安全通信网络' and second_name='通信传输'")
                print(value_dict)
                id = value_dict[0]['id']
                first_code = value_dict[0]['first_code']
                second_code = value_dict[0]['second_code']
                third_code = value_dict[0]['third_code']
                third_result = value_dict[0]['third_result']
                print(id, first_code, second_code, third_code, third_result)
                # resp = ComplianceTaskUpdate(id=id, itemCode=first_code, thirdCode=third_code ).send()
                time.sleep(3)
                resp = ComplianceTaskList().send()  # 查看资产评估的评分
                result = resp.json()
                print(result)
                assert result['data']['list'][0]['complianceIndex'] == 100.0
                resp = ComplianceTaskUpdate(id=id, taskId=task_id).send()  # 修改合规评估
                result = resp.json()
                print(result)
                assert result['message'] == '操作成功'
            with allure.step('查看资产合规评分  根据修改后的结果重新计算合规评分'):
                resp = ComplianceTaskList().send()  # 查看资产评估的评分
                result = resp.json()
                print(result)
                assert result['data']['list'][0]['complianceIndex'] == 94.0
        except Exception:
            raise Exception
        finally:
            resp = ComplianceTaskDelete(id=[task_id]).send()  # 删除合规评分
            result = resp.json()
            print(result)


@allure.feature('系统案例-告警管理')
class TestAlarmHandling:
    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    @allure.story('告警检索-告警信息增加字段')
    @allure.title('ISA-2924')
    def test_affected_ip_is_asset(self):
        """
        ISA-2924 : 当受影响IP为资产IP则在告警列表中显示该资产名称和资产类型，如果没有受影响IP或者受影响IP不是资产IP，告警列表字段中“资产名称”与“资产类型”显示为空
        1 选择一条告警信息，该告警信息受影响IP后的“资产名称”，“资产类型”两列属性有内容，通过"所属区域"与“受影响IP”到“资产中心-资产管理-已确认资产”页面进行查找
        查找到该资产（资产IP与受影响IP相同，资产所属区域与告警列表中所属区域相同）
        2 查看该资产的“资产名称”，“资产类型”
        该资产的“资产名称”，“资产类型”与告警列表中该条告警“资产名称”，“资产类型”字段显示的一致
        3 若告警没有受影响IP
        告警列表的“资产名称”，“资产类型”两列显示为空
        4 通过告警列表中的受影响IP与所属区域两种属性，无法在资产列表中寻找到对应资产
        告警列表的“资产名称”，“资产类型”两列显示为空
        """
        with allure.step('产生两种类型的告警，受影响ip为资产、受影响ip不为资产'):
            syslog(
                '20|^F039F7F1654C4B38A05A36C290BC0B3C|^null|^null|^Probe201229008|^52425|^S7|^102|^null|^201229008|^null|^null|^192.168.100.124|^违反S7协议关键事件告警,功能码:写|^{}|^TCP|^0|^null|^192.168.1.2|^2021-06-03 17:29:49|^null|^null|^|^|^null|^null|^0|^'.format(
                    IP))  # 受影响ip为资产
            time.sleep(5)
            syslog(
                '5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.100.124|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配|^1|^null|^201229008|^')  # 受影响ip不为资产
            time.sleep(30)
        with allure.step('步骤1 查看受影响ip的告警信息，受影响ip为资产、受影响ip不为资产两种'):
            resp = AlarmRetrieval().send()  # 查看告警检索
            result = resp.json()
            print(result)
            log_five = result['data']['list'][0]
            log_twenty = result['data']['list'][1]
            asset_name = log_twenty['assetName']
            asset_type = log_twenty['assetType']
            assert log_twenty['safeDeviceIp'] == IP and log_twenty['factoryName'] == 'XX区域' and log_twenty[
                'assetName'] == '安全态势感知设备' and log_five[
                       'safeDeviceIp'] == '192.168.100.123' and log_five['factoryName'] == 'XX区域' and log_five[
                       'assetName'] == None and log_five['assetType'] == None
        with allure.step('查找资产，受影响ip为资产、受影响ip不为资产'):
            resp = GetList(keyword=IP).send()  # 获取资产详情
            result = resp.json()
            print(result)
            value = result['data']['list'][0]
            assert value['ip'] == IP and value['name'] == asset_name and value['typeName'] == asset_type
            resp = GetList(keyword='192.168.100.123').send()  # 获取资产详情
            result = resp.json()
            print(result)
            total = result['data']['total']
            assert total == 0


@allure.feature('系统案例-大屏管理')
class TestBigScreenManagement:
    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    @allure.story('安全通告')
    def test_safety_notice(self):
        self.logging.info('新增未启用安全通告')
        resp = AddSafetyNotice(title="test", description='test', cveCode='1234').send()
        result = resp.json()
        pytest.assume(result['message'] == '新增安全通告成功')
        self.logging.info('查看综合安全态势安全通告')
        resp = SecurityPostureSecurityNotice().send()
        result = resp.json()
        pytest.assume(result['data']['data'] == [])
        self.logging.info('查看用安全通告,修改启用安全通告')
        resp = SafetyNotice().send()
        result = resp.json()
        id = result['data']['data'][0]['id']
        resp = ModSafetyNotice(id=id, title="test", description='test', cveCode='1234', enable=1).send()
        result = resp.json()
        pytest.assume(result['message'] == '修改安全通告成功')
        self.logging.info('查看综合安全态势安全通告')
        resp = SecurityPostureSecurityNotice().send()
        result = resp.json()
        data = result['data']['data'][0]
        pytest.assume(data['title'] == 'test' and data['description'] == 'test' and data['cveCode'] == '1234' and data[
            'operatingSystem'] == 'Windows' and data['enable'] == 1)
        self.logging.info('禁用安全通告')
        resp = ModSafetyNotice(id=id, title="test", description='test', cveCode='1234', enable=0).send()
        result = resp.json()
        pytest.assume(result['message'] == '修改安全通告成功')
        self.logging.info('删除安全通告')
        resp = DeleteSafetyNotice(ids=[id]).send()
        result = resp.json()
        pytest.assume(result['message'] == '删除安全通告成功')
        time.sleep(5)
        self.logging.info('audit查看操作日志')
        header = login_test(audit, password)
        log = OperatorLog()
        log.headers = header
        resp = log.send()
        result = resp.json()
        print(result)
        data_list = result['data']['list'][1:5]
        # todo 和乐敏确认启用和禁用记录操作日志
        value_list = ['删除安全通告[test]成功', '修改安全通告[test]成功', '修改安全通告[test]成功', '新增安全通告[test]成功']
        for index, data in enumerate(data_list):
            print(data['context'], value_list[index])
            pytest.assume(data['context'] == value_list[index])


@allure.feature('系统案例-安全知识库')
class TestSecurityKnowledgeBase:
    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    @allure.story('安全知识库-常见端口库-常见端口知识库')
    @allure.title('ISA-2469')
    def test_common_ports_add_check(self):
        """
        ISA-2469 :常见端口的添加校验
        1 新增一条与内置端口重复的数据，点击确定按钮,端口号、传输层协议均相同
        添加成功；以新添加的为准；
        2 继续添加一条与内置端口重复的数据,端口号及传输层协议均相同
        提示“添加失败”；
        3 继续添加一条与内置端口重复的数据,端口号相同、传输层协议不同
        添加成功；
        4 继续添加一条与内置端口重复的数据,端口号不同、传输层协议相同
        添加成功；
        5 重复步骤4，填写内容相同
        提示“添加失败”；
        """
        try:
            with allure.step('1 新增一条与内置端口重复的数据，点击确定按钮,端口号、传输层协议均相同'):
                resp = AddCommonPort().send()
                result = resp.json()
                with allure.step('添加成功；以新添加的为准；'):
                    print(result)
                    assert result['message'] == '端口新增成功'
            with allure.step('2 继续添加一条与内置端口重复的数据,端口号及传输层协议均相同'):
                resp = AddCommonPort(serviceType='tcpmux2').send()
                result = resp.json()
                with allure.step('提示“添加失败”；'):
                    print(result)
                    assert result['message'] == '端口重复，存在UDP传输层协议的端口'
            with allure.step('3 继续添加一条与内置端口重复的数据,端口号相同、传输层协议不同'):
                resp = AddCommonPort(transportLayer='tcp', serviceType='tcpmux3').send()
                result = resp.json()
                with allure.step('添加成功；'):
                    print(result)
                    assert result['message'] == '端口新增成功'
            with allure.step('4 继续添加一条与内置端口重复的数据,端口号不同、传输层协议相同'):
                resp = AddCommonPort(port='2', transportLayer='tcp', serviceType='tcpmux4').send()
                result = resp.json()
                with allure.step('添加成功；'):
                    print(result)
                    assert result['message'] == '端口新增成功'
            with allure.step('5 重复步骤4，填写内容相同'):
                resp = AddCommonPort(port='2', transportLayer='tcp', serviceType='tcpmux4').send()
                result = resp.json()
                with allure.step('提示“添加失败”；'):
                    print(result)
                    assert result['message'] == '端口重复，存在TCP传输层协议的端口'
        except Exception:
            raise Exception
        finally:
            id_dict = self.db.select(
                "select id from soc.soc_ports_library where service_type in ('tcpmux1','tcpmux3','tcpmux4')")
            id = [id['id'] for id in id_dict]
            DeleteCommonPort(ids=id).send()

    @allure.story('安全知识库-情报更新-情报更新')
    @allure.title('ISA-2773')
    def test_no_security_station_updates(self):
        """
        ISA-2773 : 安监站配置有问题的情况下，点击”点击更新“按钮，会出现提示”无法连接网络，重试或者使用离线库更新
        1 查看安监站配置  安监站没有配置
        2 点击”点击更新“按钮  "点击更新"按钮右侧显示"更新中"的状态变为"网络异常"状态  提示："无法连接网络，重试或者使用离线库更新"
        """
        self.logging.info('配置错误的安监站ip')
        KnowledgeUpdateConfig(ip='180.76.136.24').send()
        self.logging.info('无安监站配置，更新失败')
        resp = IntelligenceAutoUpdate().send()
        result = resp.json()
        pytest.assume(result['message'] == 'FTP网络连接失败')

    @allure.story('安全知识库-威胁情报库-安全分析-威胁情报-安全分析页面')
    @allure.title('ISA-2790')
    def test_ip_analys(self):
        """
        ISA-2790 : ”安全分析“页面，进行IP分析功能
        进入"安全知识库-威胁情报库-安全分析"页面
        1 输入IP"27.128.201.88",点击"放大镜"按钮，查看安全分析列表。  显示该IP的相关信息
        2 多次输入该IP进行分析  每次分析的数据结果显示相同
        3 点击操作列的"详情"按钮  弹出该条数据的详情弹窗
        4 查看详情弹窗 显示:威胁值、威胁来源、威胁分类、地理位置、威胁标签
        5 若威胁情报库有该条件的多条数据，则显示
        威胁值:resetprofile.com           威胁来源:maltrail
        威胁分类:恶意软件                    地理位置:
        威胁标签:apt_37、apt_kimsuky
        -----------------------------------------------------------------------------
        威胁值:resetprofile.com          威胁来源:VirusTotal
        威胁分类:恶意网站                    地理位置:
        威胁标签:
        -----------------------------------------------------------------------------
        威胁值:resetprofile.com          威胁来源:TianJi Partners
        威胁分类:APT情报                    地理位置:
        威胁标签:
        """
        with allure.step('1 输入IP"27.128.201.88",点击"放大镜"按钮，查看安全分析列表。'):
            resp = SecurityAnalysisQuery().send()
            result = resp.json()
            print(result)
            with allure.step('显示该IP的相关信息'):
                assert result['data']['total'] == 1 and result['data']['list'][0]['value'] == '27.128.201.88'
        with allure.step('2 多次输入该IP进行分析'):
            resp = SecurityAnalysisQuery().send()
            result = resp.json()
            print(result)
            with allure.step('每次分析的数据结果显示相同'):
                assert result['data']['total'] == 1 and result['data']['list'][0]['value'] == '27.128.201.88'
        with allure.step('3 点击操作列的"详情"按钮 4 查看详情弹窗析 5 若威胁情报库有该条件的多条数据'):
            resp = IntelligenceUpdateDetail().send()
            result = resp.json()
            print(result)
            assert result['data'][0]['value'] == '27.128.201.88' and result['data'][0]['category'] == '扫描器节点' and \
                   result['data'][0]['geo'] == '中国-河北-保定' and result['data'][0]['sourceRef'] == 'Emergingthreats' and \
                   result['data'][0]['threatTagVO']['service'] == ['ssh'] and result['data'][1][
                       'value'] == '27.128.201.88' and \
                   result['data'][1]['category'] == '僵尸网络' and result['data'][1]['geo'] == '中国-河北-保定' and \
                   result['data'][1]['sourceRef'] == 'ThreatWeb'

    @allure.story('安全知识库-处置建议库-处置建议库')
    @allure.title('ISA-2763')
    def test_add_disposal_advice(self):
        """
        ISA-2763 :新增一条处置建议
        1 新增一条告警类型为“业务异常告警/设备无流量/设备无流量告警中”的处置建议
        提示“新增处置建议成功”；
        2 新增一条告警类型为“业务异常告警/设备无流量/设备无流量已结束”的处置建议
        提示“新增处置建议成功”；
        3 新增一条告警类型为“业务异常告警/设备无流量”的处置建议
        提示“新增处置建议成功”；
        4 新增一条告警类型为“业务异常告警”的处置建议
        提示“新增处置建议成功”；
        5 新增一条告警类型为“业务异常告警”的处置建议
        提示“新增失败，已存在该告警类型的处置建议”；
        """
        try:
            with allure.step('1 新增一条告警类型为“业务异常告警/设备无流量/设备无流量告警中”的处置建议'):
                resp = AddDisposalAdvice(alarmType=10000101, content='test1').send()
                result = resp.json()
                with allure.step('提示“新增处置建议成功”；'):
                    print(result)
                    assert result['message'] == '新增处置建议成功'
            with allure.step('2 新增一条告警类型为“业务异常告警/设备无流量/设备无流量已结束”的处置建议'):
                resp = AddDisposalAdvice(alarmType=10000102, content='test2').send()
                result = resp.json()
                with allure.step('提示“新增处置建议成功”；'):
                    print(result)
                    assert result['message'] == '新增处置建议成功'
            with allure.step('3 新增一条告警类型为“业务异常告警/设备无流量”的处置建议'):
                resp = AddDisposalAdvice(alarmType=10000500, content='test3').send()
                result = resp.json()
                with allure.step('提示“新增处置建议成功”；'):
                    print(result)
                    assert result['message'] == '新增处置建议成功'
            with allure.step('4 新增一条告警类型为“业务异常告警”的处置建议'):
                resp = AddDisposalAdvice(alarmType=10000000, content='test4').send()
                result = resp.json()
                with allure.step('提示“新增处置建议成功”；'):
                    print(result)
                    assert result['message'] == '新增处置建议成功'
            with allure.step('5 新增一条告警类型为“业务异常告警”的处置建议'):
                resp = AddDisposalAdvice(alarmType=10000000, content='test4').send()
                result = resp.json()
                with allure.step('提示“新增失败，已存在该告警类型的处置建议”；'):
                    print(result)
                    assert result['message'] == '新增失败，已存在该告警类型的处置建议'
        except Exception:
            raise Exception
        finally:
            id_dict = self.db.select(
                "select id from soc.soc_disposal_suggestions where content in ('test1','test2','test3','test4')")
            ids = [id['id'] for id in id_dict]
            DeleteDisposalAdvice(ids=ids).send()


@allure.feature('系统案例-数据接口')
class TestDataInterface:
    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    @allure.story('接口安全性')
    @allure.title('ISA-1460')
    def test_encrypted_logs_not_decrypted(self):
        """
        ISA-1460 :加密日志未解密不进行范化
        1 在态势感知系统创建一个接收syslog的日志源并不启用加密
        日志源创建成功
        2 向日志审计系统发送日志
        在态势感知系统查看收到的日志信息,系统接受到加密的日志没有进行范化
        """
        with allure.step('2 向日志审计系统发送日志'):
            # 日志检索，查看第一条数据
            resp = LogRetrieve().send()
            result = resp.json()
            before_total = result['total']
            #  发送加密的数据
            syslog(
                '181CFE736298F1DECB9B6976A5CF08C00B427A4BFC44E75695FF1CEE6630799DDF2F84D8CCDA9D1DFAEB88288C021F4663C1E7796B896D48C7C933C21389E1E17B2A0672AE6313AE9A2422CDA45D752C1BCA36250BBC011BCB3F1B2CD089B4262C7C0BA8D3310AA1F74498035A3F88EE9558845BAB704E4DC3F77A3E5C068BE167FB343D70723F3127B91C77BDB9BF561BA34B74A83F37B3310862CB16ADAB257096F253244C59601A660771A5C590C4FE1EE5E6FCFAEE80CDF243F37C77050AB5601A7AF22EFBD5AD8F080DCE61845FCA1495CA69FD58AF8576A32E23D7B6F2817C47DE09F7563701FA7ABC26B0D12D7F91BBC51B527A6D584F24EDA7EB8FBD4E7931CC7F81C3781598301E4A18C529F574F8E5B4F2D5022F1416530BA3FF51531DD6D59331D578C00EB1F0DF9C3BDCD9F7E3D03DDB018DB3BB3EFBE7AB37B5715112641D3A907F46197930D67B624A')
            time.sleep(30)
        with allure.step('在态势感知系统查看收到的日志信息,系统接受到加密的日志没有进行范化'):
            # 日志检索，查看第一条数据
            resp = LogRetrieve().send()
            result = resp.json()
            data = result['dataList'][0]['originlog']
            after_total = result['total']
            # 判断第一条日志
            assert data == '181CFE736298F1DECB9B6976A5CF08C00B427A4BFC44E75695FF1CEE6630799DDF2F84D8CCDA9D1DFAEB88288C021F4663C1E7796B896D48C7C933C21389E1E17B2A0672AE6313AE9A2422CDA45D752C1BCA36250BBC011BCB3F1B2CD089B4262C7C0BA8D3310AA1F74498035A3F88EE9558845BAB704E4DC3F77A3E5C068BE167FB343D70723F3127B91C77BDB9BF561BA34B74A83F37B3310862CB16ADAB257096F253244C59601A660771A5C590C4FE1EE5E6FCFAEE80CDF243F37C77050AB5601A7AF22EFBD5AD8F080DCE61845FCA1495CA69FD58AF8576A32E23D7B6F2817C47DE09F7563701FA7ABC26B0D12D7F91BBC51B527A6D584F24EDA7EB8FBD4E7931CC7F81C3781598301E4A18C529F574F8E5B4F2D5022F1416530BA3FF51531DD6D59331D578C00EB1F0DF9C3BDCD9F7E3D03DDB018DB3BB3EFBE7AB37B5715112641D3A907F46197930D67B624A'
            assert int(after_total) - int(before_total) == 1  # 判断新增一条数据


@allure.feature('系统案例-策略配置')
class TestBaselineConfig:
    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    @allure.story('日志源配置-自动发现日志源')
    @allure.title('ISA-2240')
    def test_self_search_logsource_add_asset(self):
        """
        ISA-2240 : 自发现日志源，会自动新增一条已确认资产
        1 客户端A向ISA上报syslog日志
        日志已发送
        2 从ISA 日志源配置界面查看
        自动生成客户端A对应的日志源，且信息正确
        3 查看已确认资产，搜索步骤2日志源对应的资产
        自动生成已确认资产，资产信息和日志源保持一致
        """
        try:
            with allure.step('前置操作'):
                id_dict = self.db.select(f"select id from soc.soc_log_source_info where asset_ip='{local_ip}'")
                id = [id['id'] for id in id_dict]
                resp = DeleteLogSource(ids=id).send()  # 删除本地ip日志源
                result = resp.json()
                time.sleep(1)
                assert result['message'] == '操作成功'
                resp = AutoFindLogSource(flag='true').send()  # 开启自发现日志源
                result = resp.json()
                assert result['message'] == '开启自发现日志源'
                resp = RecognizedAssetsList().send()
                result = resp.json()
                value_list = result['data']['list']
                ip_list = [value['ip'] for value in value_list]
                assert local_ip not in ip_list  # 判断本地ip不在已确认资产中
            with allure.step('1 客户端A向ISA上报syslog日志'):
                syslog(
                    '<6>Nov 29 14:09:52 HOST;110103300117111310721344;ipv4;3; device_health: CPU使用=96；内存使用=57；磁盘使用=1；温度=0；会话数=79')
                time.sleep(30)
                with allure.step('日志已发送'):
                    resp = LogRetrieve().send()  # 日志检索查看日志
                    result = resp.json()
                    assert result['dataList'][0][
                               'originlog'] == '<6>Nov 29 14:09:52 HOST;110103300117111310721344;ipv4;3; device_health: CPU使用=96；内存使用=57；磁盘使用=1；温度=0；会话数=79'
            with allure.step('2 从ISA 日志源配置界面查看'):
                resp = LogSourcePage().send()
                result = resp.json()
                assetIp = result['data']['logSourceList']['list'][0]['assetIp']
                id = result['data']['logSourceList']['list'][0]['id']
                with allure.step('自动生成客户端A对应的日志源，且信息正确'):
                    print(result)
                    assert result['data']['logSourceList']['list'][0]['logSourceName'][
                           :-1] == '自发现日志源' and assetIp == local_ip
            with allure.step('3 查看已确认资产，搜索步骤2日志源对应的资产'):
                resp = RecognizedAssetsList().send()
                result = resp.json()
                with allure.step('自动生成已确认资产，资产信息和日志源保持一致'):
                    value_list = result['data']['list']
                    ip_list = [value['ip'] for value in value_list]
                    assert local_ip in ip_list
        except Exception:
            raise Exception
        finally:
            with allure.step('后置操作'):
                resp = ModLogSource(name=assetIp, ip=assetIp, normalizeGroup=["1393", "1386", "1400", "11404"],
                                    id=id).send()
                result = resp.json()
                print(result)
                resp = AutoFindLogSource(flag='flase').send()  # 开启自发现日志源
                result = resp.json()
                assert result['message'] == '关闭自发现日志源'

    @allure.story('日志源配置-添加日志源时自动生成一个已确认资产')
    @allure.title('ISA-3347')
    def test_add_logsource_add_asset(self):
        """
        ISA-3347 : 新增一条日志源时没有对应资产会自动将其新增为一个已确认资产
        1 日志源配置页面，点击新增按钮，填写日志源名称为“test”、协议类型为“syslog协议”、设备IP为（A网）“192.16.10.1”、所属区域为“XX区域”，点击确定按钮（填写的信息与系统中已存在日源的IP及协议类型均不同，且不存在一个已确认资产与新增日志源的IP及区域相同）
        可以成功新增一条日志源；
        2 查看已确认资产列表
        生成了一个与步骤1对应的已确认资产；
        3 在日志源配置页面，点击新增按钮，所有项填写同步骤1，点击确定按钮
        新增日志源失败；
        4 查看已确认资产的列表
        没有新增的已确认资产，也没有更新了信息的已确认资产；
        """
        try:
            with allure.step('前置操作'):
                resp = RecognizedAssetsList().send()
                result = resp.json()
                value_list = result['data']['list']
                ip_list = [value['ip'] for value in value_list]
                assert '192.16.10.1' not in ip_list  # 判断本地ip不在已确认资产中
            with allure.step(
                    '1 日志源配置页面，点击新增按钮，填写日志源名称为“test”、协议类型为“syslog协议”、设备IP为（A网）“192.16.10.1”、所属区域为“XX区域”，点击确定按钮（填写的信息与系统中已存在日源的IP及协议类型均不同，且不存在一个已确认资产与新增日志源的IP及区域相同）'):
                resp = AddLogSource(name='test', ip='192.16.10.1').send()
                result = resp.json()
                print(result)
                with allure.step('可以成功新增一条日志源；'):
                    resp = LogSourcePage().send()
                    result = resp.json()
                    value_list = result['data']['logSourceList']['list']

                    ip_list = [value['assetIp'] for value in value_list]
                    assert '192.16.10.1' in ip_list
            with allure.step('2 查看已确认资产列表'):
                resp = RecognizedAssetsList().send()
                result = resp.json()
                value_list = result['data']['list']
                newAsset = value_list[-1]
                data_total_before = result['data']['total']
                ip_list = [value['ip'] for value in value_list]
                with allure.step('生成了一个与步骤1对应的已确认资产；'):
                    assert '192.16.10.1' in ip_list  # 判断本地ip不在已确认资产中
            with allure.step('3 在日志源配置页面，点击新增按钮，所有项填写同步骤1，点击确定按钮'):
                resp = AddLogSource(name='test', ip='192.16.10.1').send()
                result = resp.json()
                with allure.step('新增日志源失败；'):
                    print(result)
                    assert result['message'] == '日志源名称重复' and result['status'] == False
            with allure.step('4 查看已确认资产的列表'):
                resp = RecognizedAssetsList().send()
                result = resp.json()
                data_total_after = result['data']['total']
                new_asset = value_list[-1]
                with allure.step('没有新增的已确认资产，也没有更新了信息的已确认资产；'):
                    assert data_total_before == data_total_after and newAsset == new_asset
        except Exception:
            raise Exception
        finally:
            with allure.step('后置操作'):
                id_dict = self.db.select("select id from soc.soc_log_source_info where asset_ip='192.16.10.1'")
                id = [id['id'] for id in id_dict]
                resp = DeleteLogSource(ids=id).send()
                result = resp.json()
                print(result)

    @allure.story('日志源配置-添加日志源时自动生成一个已确认资产')
    @allure.title('ISA-3348')
    def test_add_logsource_related_asset(self):
        """
        ISA-3348 : 新增一条日志源时已存在资产会将日志源跟已确认资产关联
        1 已确认资产页面，新增一个IP为192.168.4.175，区域为XX区域的资产，填写完成点击确定
        新增已确认资产成功；
        2 日志源配置页面，新增一个IP为192.168.4.175，协议类型为syslog协议，区域为XX区域的日志源
        新增日志源成功，且自动与步骤1的已确认资产关联；
        """
        try:
            with allure.step('1 已确认资产页面，新增一个IP为192.168.4.175，区域为XX区域的资产，填写完成点击确定'):
                resp = AddAssetParam(name='192.16.4.15', ip='192.16.4.15').send()
                result = resp.json()
                with allure.step('新增已确认资产成功；'):
                    print(result)
                    assert '资产添加成功' in result['message']
                    resp = RecognizedAssetsList(keyword='192.16.4.15').send()
                    result = resp.json()
                    print(result)
                    value_list = result['data']['list']
                    ip_list = [value['ip'] for value in value_list]
                    value_before = value_list[0]  # 新增日志源之前的资产
                    assert '192.16.4.15' in ip_list  # 判断本地ip在已确认资产中
            with allure.step('2 日志源配置页面，新增一个IP为192.168.4.175，协议类型为syslog协议，区域为XX区域的日志源'):
                resp = AddLogSource(name='192.16.4.15', ip='192.16.4.15').send()
                result = resp.json()
                with allure.step('新增日志源成功，且自动与步骤1的已确认资产关联；'):
                    print(result)
                    resp = RecognizedAssetsList(keyword='192.16.4.15').send()
                    result = resp.json()
                    print(result)
                    value_after = result['data']['list'][0]  # 新增日志源之前的资产
                    assert value_before['ip'] == value_after['ip'] and value_before != value_after
        except Exception:
            raise Exception
        finally:
            with allure.step('后置操作'):
                id_dict = self.db.select("select id from soc.soc_log_source_info where asset_ip='192.16.4.15'")
                id = [id['id'] for id in id_dict]
                resp = DeleteLogSource(ids=id).send()
                result = resp.json()
                print(result)

    @allure.story('日志源配置-添加日志源时自动生成一个已确认资产')
    @allure.title('ISA-3485')
    def test_import_logsource_add_asset(self):
        """
        ISA-3485 : 【建议自动化-低】导入日志源时没有对应资产会将其添加为一个已确认资产
        1 日志源配置页面，点击导入数据按钮，导入日志源
        成功导入一条日志源；
        2 查看已确认资产列表
        生成了一个与步骤1对应的已确认资产；
        """
        try:
            with allure.step('前置操作'):
                resp = RecognizedAssetsList().send()
                result = resp.json()
                value_list = result['data']['list']
                data_total_before = result['data']['total']
                ip_list = [value['ip'] for value in value_list]
                assert '192.168.4.179' not in ip_list  # 判断ip不在已确认资产中
            with allure.step('1 日志源配置页面，点击导入数据按钮，导入日志源'):
                resp = LogSourceImport(file='日志源信息_小于5M.xlsx').send()
                result = resp.json()
                with allure.step('成功导入一条日志源；'):
                    print(result)
            with allure.step('2 查看已确认资产列表'):
                time.sleep(3)
                resp = RecognizedAssetsList().send()
                result = resp.json()
                data_total_after = result['data']['total']
                ip_list = [value['ip'] for value in result['data']['list']]
                assert '192.168.4.179' in ip_list and int(data_total_after) - int(data_total_before) == 1 # 判断ip不在已确认资产中
        except Exception:
            raise Exception
        finally:
            with allure.step('后置操作'):
                id_dict = self.db.select("select id from soc.soc_log_source_info where asset_ip='192.168.4.179'")
                id = [id['id'] for id in id_dict]
                resp = DeleteLogSource(ids=id).send()
                result = resp.json()
                print(result)
                assert result['message'] == '操作成功'

    @allure.story('日志源配置-添加日志源时自动生成一个已确认资产')
    @allure.title('ISA-3486')
    def test_import_logsource_related_asset(self):
        """
        ISA-3486 :导入日志源时已存在资产会将日志源跟已确认资产关联
        1 已确认资产页面，新增一个IP为192.168.4.175，区域为XX区域的资产，填写完成点击确定
        新增已确认资产成功；
        2 日志源配置页面，点击导入数据按钮，导入IP为192.168.4.175，区域为XX区域的日志源
        成功导入一条日志源，且自动与步骤1的已确认资产关联；
        """
        try:
            with allure.step('1 已确认资产页面，新增一个IP为192.168.4.175，区域为XX区域的资产，填写完成点击确定'):
                resp = AddAssetParam(name='192.168.4.179', ip='192.168.4.179').send()
                result = resp.json()
                with allure.step('新增已确认资产成功；'):
                    print(result)
                    assert '操作成功' in result['message']
                    resp = RecognizedAssetsList(keyword='192.168.4.179').send()
                    result = resp.json()
                    print(result)
                    value_list = result['data']['list']
                    ip_list = [value['ip'] for value in value_list]
                    value_before = value_list[0]  # 新增日志源之前的资产
                    assert '192.168.4.179' in ip_list  # 判断本地ip在已确认资产中
                with allure.step('2 日志源配置页面，点击导入数据按钮，导入IP为192.168.4.175，区域为XX区域的日志源'):
                    resp = LogSourceImport(file='日志源信息_小于5M.xlsx').send()
                    result = resp.json()
                with allure.step('新增日志源成功，且自动与步骤1的已确认资产关联；'):
                    print(result)
                    time.sleep(3)
                    resp = RecognizedAssetsList(keyword='192.168.4.179').send()
                    result = resp.json()
                    print(result)
                    value_after = result['data']['list'][0]  # 新增日志源之前的资产
                    assert value_before['ip'] == value_after['ip'] and value_before != value_after
        except Exception:
            raise Exception
        finally:
            with allure.step('后置操作'):
                id_dict = self.db.select("select id from soc.soc_log_source_info where asset_ip='192.168.4.179'")
                id = [id['id'] for id in id_dict]
                resp = DeleteLogSource(ids=id).send()
                result = resp.json()
                print(result)


    @allure.story('关联分析')
    @allure.title('ISA-2146')
    def test_import_wrong_correlation_analysis(self):
        """
        ISA-2146 : 导入关联规则字段不符合长度要求的合法关联规则文件
        1 先导出一个关联规则文件  导出成功
        2 打开该关联规则文件，不修改格式，只修改一些字段的值。  例如规则组名称为64个字符，在导出的excel关联规则文件中，修改一个规则，把该规则中的规则组名称修改为大于64个字符的名称，其余字段不做修改。保存，导入该关联分析规则文件
        导入失败
        3 按照步骤2的方法，规则组名称合格，修改一条规则的“范化策略名称”大于64个字符，其余字段全部符合要求。保存，导入该文件  导入失败
        4 修改一条规则的“告警描述”大于128个字符，其余字段全部符合要求，保存，导入该文件  导入失败
        """
        self.logging.info('规则组名称大于64字符')
        resp = ImportCorrelationAnalysis(file='correlation_analysis\\关联分析-规则组超长.xlsx').send()
        result = resp.json()
        print(result)
        pytest.assume(result['reason'] == '第2行导入失败！关联分析组不存在或者为空！')
        self.logging.info('范化策略名称大于64字符')
        resp = ImportCorrelationAnalysis(file='correlation_analysis\\关联分析-范化策略不符合规则.xlsx').send()
        result = resp.json()
        print(result)
        pytest.assume(result['reason'] == '第2行导入失败！关联分析名称不合法！')
        self.logging.info('告警描述大于256字符')
        resp = ImportCorrelationAnalysis(file='correlation_analysis\\关联分析-告警描述超限.xlsx').send()
        result = resp.json()
        print(result)
        pytest.assume(result['reason'] == '第2行导入失败！关联分析描述不合法！')

    @allure.story('关联分析')
    @allure.title('ISA-2154')
    def test_import_wrong_correlation_two(self):
        """
        ISA-2154 : 导入关联规则字段不符合字符类型要求的合法关联规则文件
        1先导出一个关联规则文件  导出成功
        3打开该关联规则文件，不修改格式，只修改一些字段的值。
        在导出的excel关联规则文件中，修改一个规则，把该规则中的规则组名称修改为包含不合要求的特殊字符（例如#￥%%），其余字段不做修改。
        保存，导入该关联分析规则文件
        导入失败
        4按照步骤2的方法，规则组名称合格，修改一条规则的“范化策略名称”包含不合要求的特殊字符（例如#￥%%），其余字段全部符合要求。保存，导入该文件
        """
        self.logging.info('规则组名称大于64字符')
        resp = ImportCorrelationAnalysis(file='correlation_analysis\\关联分析-规则组包含特殊字符.xlsx').send()
        result = resp.json()
        print(result)
        pytest.assume(result['reason'] == '第2行导入失败！关联分析组不存在或者为空！')
        self.logging.info('范化策略名称大于64字符')
        resp = ImportCorrelationAnalysis(file='correlation_analysis\\关联分析-范化策略包含特殊字符.xlsx').send()
        result = resp.json()
        print(result)
        pytest.assume(result['reason'] == '第2行导入失败！关联分析名称不合法！')

    # @allure.story('ISA-2693')
    # def test_asset_baseline(self):
    #     """
    #     ISA-2693 : 用“生成基线”生成所有已确认资产的端口基线
    #     1 点击端口基线列表上方的“生成基线”  开始生成端口基线，在“生成基线”按钮后出现提示信息“生成基线中，请勿操作……”
    #     2 在生成基线过程中，点击页面上的新增或者删除按钮  提示正在生成基线中，稍候操作
    #     3 等待基线生成完成，查看端口基线列表
    #     所有已确认资产生成端口基线，每一个设备排列在端口基线页面的列表中。
    #     所有已确认资产的设备名称都显示在端口基线列表中。
    #     在每个设备的“端口基线”列中，显示有端口（为该设备开放的端口）。多个端口之间用,进行分隔显示。
    #     如果有设备没有开放的端口，则“端口基线”列中显示空
    #     """
    #     self.logging.info('生成基线')
    #     resp = GenerateBaseline().send()
    #     result = resp.json()
    #     print(result)
    #     pytest.assume(result['message'] == '开始生成端口基线')
    #     self.logging.info('查看资产获取设备信息')
    #     resp = RecognizedAssetsList().send()
    #     result = resp.json()
    #     print(result)
    #     name_list = [list['name'] for list in result['data']['list']]  # 获取所有设备名称
    #     typeName = [list['typeName'] for list in result['data']['list']]  # 获取所有设备类型
    #     self.logging.info('查看基线端口')
    #     resp = BaselinePage().send()
    #     result = resp.json()
    #     print(result)
    #     values = result['data']['values']
    #     value_name_list = [value['name'] for value in values]  # 获取所有设备名称
    #     aseetTypeCn_list = [value['aseetTypeCn'] for value in values]  # 获取所有设备类型
    #     ids = [value['id'] for value in values]  # 参数供删除接口使用
    #     ports_list = [value['ports'] for value in result['data']['values']]  # 获取所有设备名称
    #     self.logging.info('判断设备名称、设备类型和端口号的显示格式')
    #     for name in value_name_list:  # 名称
    #         pytest.assume(name in name_list)
    #     pytest.assume(len(value_name_list) == len(name_list))   # 名称数量相等
    #     for name in aseetTypeCn_list:   # 类型
    #         pytest.assume(name in typeName)
    #     pytest.assume(len(typeName) == len(aseetTypeCn_list))  # 类型数量相等
    #     print(ports_list)
    #     for port in ports_list:  # 如果为空，判断为空。如果有一个端口判断端口存在，如果为多个端口按','分割后的列表和端口数量一致
    #         if port == None:
    #             pytest.assume(port == None)
    #         elif len(port) == 1:
    #             pytest.assume(port == port)
    #         else:
    #             port_list = port.strip(',')
    #             pytest.assume(len(port) == len(port_list))
    #     resp = DeleteGenerateBaseline(ids=ids).send()
    #     result = resp.json()
    #     pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('基线配置')
    @allure.title('ISA-2778')
    def test_add_different_ways_port(self):
        """
        ISA-2778 : 验证“端口基线-新增端口”中输入端口的几种方式
        1 在端口基线页面中新建端口基线  新建端口基线成功
        2 点击端口基线列表中“操作”列中的“查看明细”  进入“端口明细列表”页面
        3 点击“新增”  进入新增端口页面
        4 输入端口号，可以单个输入，例如80,8080,7777，中间用英文逗号间隔  输入成功
        5 也可以输入端口范围，例如888-999  输入成功
        6 混合输入，例如80,81,345-367  输入成功
        7 点击确定，返回端口详情页面，再点击确定
        返回端口基线列表页面，输入的端口显示在“端口基线”列中。显示形式和输入形式一致，显示端口也和输入端口一致
        """
        try:
            query = AssetListQuery()
            resp = query.send()
            result = resp.json()
            first_id = result['data']['list'][0]['id']
            print(first_id)
            print(result)
            self.logging.info('新增端口基线')
            add = AddGenerateBaseline()
            add.json = {"assetId": first_id}
            resp = add.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '新增端口基线成功')
            self.logging.info('基线列表页')
            resp = BaselinePage().send()
            result = resp.json()
            id = result['data']['values'][0]['id']  # 基线id
            self.logging.info('端口基线明细')
            resp = PortBaselineDetails(portId=id).send()
            result = resp.json()
            print(result)
            self.logging.info('添加基线端口')
            AddBaselinePort(portId=id, ports="80,8080,7777").send()
            AddBaselinePort(portId=id, ports="888-899").send()
            AddBaselinePort(portId=id, ports="80,81,345-367").send()
            self.logging.info('端口基线明细')
            resp = PortBaselineDetails(portId=id).send()
            result = resp.json()
            print(result)
            port_list = [value['ports'] for value in result['data']['values']]
            print(port_list)
            pytest.assume(port_list[-3:] == ['80,8080,7777', '888,889,890,891,892,893,894,895,896,897,898,899',
                                             '80,81,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367'] or port_list[
                                                                                                                                                     :3] == [
                              '80,8080,7777', '888,889,890,891,892,893,894,895,896,897,898,899',
                              '80,81,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367'])
        except Exception as e:
            raise e
        finally:
            pass
            self.logging.info('删除端口基线')
            delete = DeleteGenerateBaseline()
            delete.json = {"ids": [id]}
            print(delete.json)
            resp = delete.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('基线配置')
    @allure.title('ISA-2780')
    def test_add_error_ways_port(self):
        """
        ISA-2780 : 验证“端口基线-新增端口”中输入非法端口
        1 在端口基线页面中新建端口基线  新建端口基线成功
        2 点击端口基线列表中某一基线后的“查看明细”  进入“端口明细列表”页面
        3 点击“新增”  进入新增端口页面
        4 输入错误端口号，例如字母aaa，点击确定  提示输入正确的端口，查看提示
        5 输入字母数字组合，例如a333，77a3  提示输入正确的端口，查看提示
        6 输入汉字例如：测试  提示输入正确的端口，查看提示
        7 输入特殊字符@#  提示输入正确的端口，查看提示
        """
        try:
            query = AssetListQuery()
            resp = query.send()
            result = resp.json()
            first_id = result['data']['list'][0]['id']
            print(first_id)
            print(result)
            self.logging.info('新增端口基线')
            add = AddGenerateBaseline()
            add.json = {"assetId": first_id}
            resp = add.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '新增端口基线成功')
            self.logging.info('基线列表页')
            resp = BaselinePage().send()
            result = resp.json()
            id = result['data']['values'][0]['id']  # 基线id
            self.logging.info('端口基线明细')
            resp = PortBaselineDetails(portId=id).send()
            result = resp.json()
            print(result)
            self.logging.info('添加基线端口')
            # todo bug修改后增加断言
            resp = AddBaselinePort(portId=id, ports="aaa").send()
            result = resp.json()
            print(result)
            resp = AddBaselinePort(portId=id, ports="a333,77a3").send()
            result = resp.json()
            print(result)
            resp = AddBaselinePort(portId=id, ports="测试").send()
            result = resp.json()
            print(result)
            resp = AddBaselinePort(portId=id, ports="@#").send()
            result = resp.json()
            print(result)
        except Exception as e:
            raise e
        finally:
            self.logging.info('删除端口基线')
            delete = DeleteGenerateBaseline()
            delete.json = {"ids": [id]}
            print(delete.json)
            resp = delete.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('基线配置')
    @allure.title('ISA-2699')
    def test_mod_baseline_port(self):
        """
        ISA-2699 : “编辑”端口来修改基线端口
        1 在“端口基线”页面，点击端口基线列表的某一列后的“查看明细” 进入“端口明细列表”
        2 选择某一个需要修改的基线端口，点击其后操作列中的“编辑”  进入“编辑端口”页面。编辑端口页面中展示的端口号，协议和服务，和端口明细列表中显示的信息一致
        3 在编辑端口页面中，可以修改端口信息，修改完成，点击确定  可以修改成功
        4 修改成功后返回端口明细列表 新修改的信息显示在端口列表中
        """
        try:
            query = AssetListQuery()
            resp = query.send()
            result = resp.json()
            first_id = result['data']['list'][0]['id']
            print(first_id)
            print(result)
            self.logging.info('新增端口基线')
            add = AddGenerateBaseline()
            add.json = {"assetId": first_id}
            resp = add.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '新增端口基线成功')
            self.logging.info('基线列表页')
            resp = BaselinePage().send()
            result = resp.json()
            id = result['data']['values'][0]['id']  # 基线id
            self.logging.info('添加基线端口')
            resp = AddBaselinePort(portId=id, ports=11).send()
            self.logging.info('端口基线明细')
            resp = PortBaselineDetails(portId=id).send()
            result = resp.json()
            print(result)
            mod_id = result['data']['values'][0]['id']
            self.logging.info('修改基线端口')
            EditBaselinePort(id=mod_id, portId=id, ports=1).send()
            self.logging.info('端口基线明细')
            resp = PortBaselineDetails(portId=id).send()
            result = resp.json()
            print(result)
            pytest.assume(result['data']['values'][0]['ports'] == '1')
        except Exception as e:
            raise e
        finally:
            self.logging.info('删除端口基线')
            delete = DeleteGenerateBaseline()
            delete.json = {"ids": [id]}
            print(delete.json)
            resp = delete.send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('基线配置')
    @allure.title('ISA-2705')
    def test_query_baseline_port(self):
        """
        ISA-2705 : 查询端口基线
        1 在“端口基线”页面右上角，查询输入框中输入设备名称或者设备ip，点击搜索  可以搜索出对应的设备端口基线，端口基线列表中只显示查询出来的基线列表
        2 查询框支持对“设备名称”的模糊搜索，例如输入：多  凡是设备名称中包含“多”字符的端口基线，显示在基线列表中，例如设备：多-5555
        3 输入设备名称支持的特殊字符.  可以搜索成功 ，包含这些特殊字符的设备显示在下方的基线列表中，例如设备：测试._，设备_.
        4 搜索结果为空  端口基线列表显示为空
        """
        try:
            self.logging.info('新增资产')  # 新增三个资产
            AddAssetParam(name='多-5555', ip='192.168.56.77').send()
            AddAssetParam(name='测试.-', ip='192.168.56.78').send()
            AddAssetParam(name='设备_.', ip='192.168.56.79').send()
            self.logging.info('生成基线')
            resp = GenerateBaseline().send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '开始生成端口基线')

            self.logging.info('查看基线端口')
            resp = BaselinePage().send()
            result = resp.json()
            print(result)
            values = result['data']['values']
            # value_name_list = [value['name'] for value in values]  # 获取所有设备名称
            # aseetTypeCn_list = [value['aseetTypeCn'] for value in values]  # 获取所有设备类型
            port_ids = [value['id'] for value in values]  # 参数供删除接口使用
            # ports_list = [value['ports'] for value in result['data']['values']]  # 获取所有设备名称
            self.logging.info('设备名称')
            resp = PortBaselineQuery(keyword='多-5555').send()
            result = resp.json()
            print(result)
            pytest.assume(result['data']['totalSize'] == 1)
            pytest.assume(result['data']['values'][0]['name'] == '多-5555')
            self.logging.info('设备ip')
            resp = PortBaselineQuery(keyword='192.168.56.77').send()
            pytest.assume(result['data']['totalSize'] == 1)
            pytest.assume(result['data']['values'][0]['ip'] == '192.168.56.77')
            result = resp.json()
            print(result)
            self.logging.info('设备名称模糊搜索')
            resp = PortBaselineQuery(keyword='多').send()
            result = resp.json()
            print(result)
            pytest.assume(result['data']['totalSize'] == 1)
            pytest.assume(result['data']['values'][0]['name'] == '多-5555')
            self.logging.info('设备名称支持的特殊字符.')
            resp = PortBaselineQuery(keyword='.-').send()
            result = resp.json()
            print(result)
            pytest.assume(result['data']['totalSize'] == 1)
            pytest.assume(result['data']['values'][0]['name'] == '测试.-')
            self.logging.info('搜索结果为空')
            resp = PortBaselineQuery(keyword='少').send()
            result = resp.json()
            print(result)
            pytest.assume(result['data']['totalSize'] == 0)
        except Exception as e:
            raise e
        finally:
            self.logging.info('删除新增资产')
            ids = self.db.select(
                "select id from soc.soc_asset_info where ip in ('192.168.56.77','192.168.56.78','192.168.56.79')")
            ids_list = [id['id'] for id in ids]
            DeleteAsset(id=ids_list).send()
            self.logging.info('删除端口基线')
            resp = DeleteGenerateBaseline(ids=port_ids).send()
            result = resp.json()
            pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('基线配置')
    @allure.title('ISA-3223')
    def test_repeat_operator_generate_baseline(self):
        """
        ISA-3223 : 多次生成同一设备的端口基线，基线去重检查
        1 在“策略配置—基线配置—端口基线”主页面，点击“生成基线”，等待基线生成完毕  所有“已确认资产”自动生成基线，所有基线显示在“端口基线”主页面的端口基线列表中
        2 再次点击“生成基线”命令。等待基线生成完毕
        生成完毕之后，查看基线列表，不能存在“设备ip+区域”相同的两条基线
        用搜索功能，在搜索框输入设备IP地址（该IP为已生成基线的设备ip），并匹配该设备所属的区域，查找结果显示只有一条基线
        """
        try:
            self.logging.info('生成基线')
            resp = GenerateBaseline().send()
            result = resp.json()
            print(result)
            self.logging.info('查看基线端口')
            time.sleep(2)
            resp = BaselinePage().send()
            result = resp.json()
            print(result)
            total_before = result['data']['totalSize']  # 端口基线总数
            self.logging.info('重复生成基线')
            resp = GenerateBaseline().send()
            result = resp.json()
            print(result)
            self.logging.info('查看基线端口')
            time.sleep(2)
            resp = BaselinePage().send()
            result = resp.json()
            print(result)
            total_after = result['data']['totalSize']  # 端口基线总数
            pytest.assume(total_before == total_after)
            values = result['data']['values']
            ids = [value['id'] for value in values]  # 参数供删除接口使用
            self.logging.info('搜索设备ip，显示只有一条')
            resp = PortBaselineQuery(keyword=local_ip).send()
            result = resp.json()
            print(result)
            pytest.assume(result['data']['totalSize'] == 1)
        except Exception as e:
            raise e
        finally:
            self.logging.info('删除端口基线')
            resp = DeleteGenerateBaseline(ids=ids).send()
            result = resp.json()
            pytest.assume(result['message'] == '删除端口基线成功')

    @allure.story('基线配置')
    @allure.title('ISA-3344')
    def test_delete_asset_delete_baseline_port(self):
        """
        ISA-3344 : 资产删除，对应资产的端口基线被自动删除
        1 在“端口基线”页面中，点击自动生成基线（假设有个已确认资产的设备ip是1.1.1.1）  生成所有已确认资产的端口基线（其中必有一条设备ip为1.1.1.1的端口基线）
        2 在资产中心-已确认资产页面中，选中一个资产（例如1.1.1.1），点击删除  资产删除成功，在已确认资产页面中找不到该资产
        3 点击端口基线页面，查看端口基线  设备ip为1.1.1.1的端口基线已经找不到了
        """
        try:
            self.logging.info('新增资产')  # 新增三个资产
            AddAssetParam(name='192.168.56.77', ip='192.168.56.77').send()
            self.logging.info('生成基线')
            resp = GenerateBaseline().send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '开始生成端口基线')
            self.logging.info('查看基线端口')
            resp = BaselinePage().send()
            result = resp.json()
            print(result)
            values = result['data']['values']
            name_list = [value['name'] for value in values]
            print(name_list)
            pytest.assume('192.168.56.77' in name_list)  # 资产删除前存在端口基线存在
            self.logging.info('删除新增资产')
            ids = self.db.select(
                "select id from soc.soc_asset_info where ip='192.168.56.77'")
            ids_list = [id['id'] for id in ids]
            DeleteAsset(id=ids_list).send()
            self.logging.info('查看基线端口')
            resp = BaselinePage().send()
            result = resp.json()
            print(result)
            values = result['data']['values']
            port_ids = [value['id'] for value in values]  # 参数供删除接口使用
            name_list = [value['name'] for value in values]
            print(name_list)
            pytest.assume('192.168.56.77' not in name_list)  # 资产删除前存在端口基线存在
        except Exception as e:
            raise e
        finally:
            self.logging.info('删除端口基线')
            resp = DeleteGenerateBaseline(ids=port_ids).send()
            result = resp.json()
            pytest.assume(result['message'] == '删除端口基线成功')

    # @allure.story('网络基线')
    # @allure.title('ISA-2916')
    # def test_add_baseline_name_check(self):
    #     """
    #     ISA-2916 : 【建议自动化-低】新增网络基线的基线名称校验
    #     1 点击“基线名称”输入框
    #     可以输入；
    #     2 输入为空
    #     提示“基线名称不能为空”；
    #     3 输入不符合校验规则,如:“<、>”
    #     提示“基线名称可输入英文、数字、中文、空格和特殊字符(-_.)”；
    #     4 输入超过64个字符，输入的字符符合校验规则
    #     第65个及以后的无法输入；
    #     """
    #     try:
    #         with allure.step('1 点击“基线名称”输入框'):
    #
    #             resp = AddNetworkBaseline(name='test', fromTime=last_week, toTime=today).send()
    #             result = resp.json()
    #             with allure.step('可以输入；'):
    #                 print(result)
    #         with allure.step('2 输入为空'):
    #             time.sleep(2)
    #             resp = AddNetworkBaseline(name='', fromTime=last_week, toTime=today).send()
    #             result = resp.json()
    #             with allure.step('提示“基线名称不能为空”；'):
    #                 print(result)
    #         with allure.step('3 输入不符合校验规则,如:“<、>”'):
    #             resp = AddNetworkBaseline(name='<、>', fromTime=last_week, toTime=today).send()
    #             result = resp.json()
    #             with allure.step('提示“基线名称可输入英文、数字、中文、空格和特殊字符(-_.)”；'):
    #                 print(result)
    #         with allure.step('4 输入超过64个字符，输入的字符符合校验规则'):
    #             resp = AddNetworkBaseline(name=small_field+'user', fromTime=last_week, toTime=today).send()
    #             result = resp.json()
    #             with allure.step('第65个及以后的无法输入；'):
    #                 print(result)
    #     except Exception:
    #         raise Exception
    #     finally:
    #         pass


    @allure.story('工单管理-新增工单')
    @allure.title('ISA-2868')
    def test_add_work_order(self):
        """
        ISA-2868 :新增工单
        1 点击“新增”按钮  弹出新增工单弹窗
        2 输入工单名称、开始时间、完成时间、执行人、工单描述、执行描述,点击保存  保存成功
        """
        try:
            with allure.step('2 输入工单名称、开始时间、完成时间、执行人、工单描述、执行描述,点击保存'):
                start_time = str(
                    (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")) + ' 23:57:00'  # 开始时间
                end_time = str(
                    (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")) + ' 23:59:59'  # 开始时间
                resp = WorkOrderAdd(startTime=start_time, endTime=end_time).send()
                result = resp.json()
                print(result)
                resp = WorkOrderShow().send()
                show_result = resp.json()
                print(show_result)
                value = show_result['data']['list'][0]
                with allure.step('保存成功'):
                    assert result['message'] == '操作成功'
                    assert show_result['data']['total'] == 1 and value['workName'] == 'test' and value['workName'] == \
                           'test' and value['workExecutor'] == 'tym'
        except Exception:
            raise Exception
        finally:
            with allure.step('删除工单'):
                id_dict = self.db.select("select id from soc.soc_work_order_info where work_name='test'")
                id = id_dict[0]['id']
                delete = DeleteWorkOrder()
                delete.json = {"ids": [id]}
                resp = delete.send()
                result = json.loads(resp.text)
                assert result['statusCode'] == 200

    @allure.story('工单管理-工单处理')
    @allure.title('ISA-2870')
    def test_work_order_edit(self):
        """
        ISA-2870 : 【建议自动化-高】编辑工单
        1 选择自己创建的工单，点击“修改”按钮  弹出编辑工单弹窗
        2 修改工单名称、开始时间、完成时间、执行人、工单描述、工单执行描述,点击保存
        工单信息修改成功
        """
        try:
            with allure.step('1 新增一个工单信息'):
                start_time = str(
                    (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")) + ' 23:57:00'  # 开始时间
                end_time = str(
                    (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")) + ' 23:59:59'  # 开始时间
                resp = WorkOrderAdd(startTime=start_time, endTime=end_time).send()
                result = resp.json()
                print(result)
                resp = WorkOrderShow().send()
                show_result = resp.json()
                print(show_result)
                value = show_result['data']['list'][0]
                with allure.step('工单新增成功'):
                    assert result['message'] == '操作成功'
                    assert show_result['data']['total'] == 1 and value['workName'] == 'test' and value[
                        'workExecutor'] == 'tym'
            with allure.step('2 选择自己创建的工单，点击“修改”按钮;修改工单名称、开始时间、完成时间、执行人、工单描述、工单执行描述,点击保存'):
                id_dict = self.db.select("select id from soc.soc_work_order_info where work_name='test'")
                id = id_dict[0]['id']
                start_time = str(
                    (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d")) + ' 23:57:00'  # 开始时间
                end_time = str(
                    (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d")) + ' 23:59:59'  # 开始时间
                resp = WorkOrderMod(id=id, workName='test1', workCreator='operator', workExecutor='operator',
                                    workDescription='开始1', workExecuteDescription='结束1', startTime=start_time,
                                    endTime=end_time).send()
                result = resp.json()
                print(result)
                resp = WorkOrderShow().send()
                show_result = resp.json()
                print(show_result)
                value = show_result['data']['list'][0]
                with allure.step('工单信息修改成功'):
                    assert result['message'] == '操作成功'
                    assert show_result['data']['total'] == 1 and value['workName'] == 'test1' and value[
                        'workDescription'] == '开始1' and value[
                               'workExecuteDescription'] == '结束1' and value['startTime'] == start_time and value[
                               'endTime'] == end_time and value['workExecutor'] == 'operator'
        except Exception:
            raise Exception
        finally:
            with allure.step('删除工单'):
                id_dict = self.db.select("select id from soc.soc_work_order_info where work_name='test1'")
                id = id_dict[0]['id']
                delete = DeleteWorkOrder()
                delete.json = {"ids": [id]}
                resp = delete.send()
                result = json.loads(resp.text)
                assert result['statusCode'] == 200

    @allure.story('工单管理-工单处理')
    @allure.title('ISA-3213')
    def test_overtime_work_order(self):
        """
        ISA-3213 : 超过工单结束时间完成的工单状态变为已超时
        1 超过工单结束时间之后终止工单,查看工单状态  工单状态为已终止
        2 超过工单结束时间之后编辑工单状态为已完成,查看工单状态  工单状态为已超时
        """
        try:
            with allure.step('1 新增两个工单信息,超过工单结束时间之后终止工单,查看工单状态'):
                start_time = str(
                    (datetime.datetime.now() + datetime.timedelta(minutes=0.5)).strftime("%Y-%m-%d %H:%M:%S"))  # 开始时间
                end_time = str(
                    (datetime.datetime.now() + datetime.timedelta(minutes=0.6)).strftime("%Y-%m-%d %H:%M:%S"))  # 开始时间
                resp1 = WorkOrderAdd(workName='test1', workExecutor='operator', startTime=start_time,
                                     endTime=end_time).send()
                result1 = resp1.json()
                time.sleep(1)
                resp2 = WorkOrderAdd(workName='test2', workExecutor='operator', startTime=start_time,
                                     endTime=end_time).send()
                result2 = resp2.json()
                print(result1)
                print(result2)
                id_dict1 = self.db.select("select id from soc.soc_work_order_info where work_name='test1'")  # 创建test1工单
                id_dict2 = self.db.select("select id from soc.soc_work_order_info where work_name='test2'")  # 创建test2工单
                time.sleep(45)
                id1 = id_dict1[0]['id']
                id2 = id_dict2[0]['id']
                resp = StopWorkOrder(id=id2, workName='test2', workExecutor='operator', createTime=start_time,
                                     updateTime=end_time).send()  # 终止工单test2
                result1 = resp.json()
                print(result1)
                with allure.step('工单状态为已终止'):
                    resp = WorkOrderShow().send()
                    show_result = resp.json()
                    print(show_result)
                    # value1 = show_result['data']['list'][0]
                    value2 = show_result['data']['list'][1]
                    assert value2['workStatus'] == 4
            with allure.step('2 超过工单结束时间之后编辑工单状态为已完成,查看工单状态'):
                resp = WorkOrderMod(id=id1, workCreator='operator', workName='test1', workExecutor='operator',
                                    startTime=start_time, endTime=end_time, workStatus=3).send()  # 编辑工单test1
                result2 = resp.json()
                print(result2)
                with allure.step('工单状态为已超时'):
                    resp = WorkOrderShow().send()
                    show_result = resp.json()
                    print(show_result)
                    value1 = show_result['data']['list'][0]
                    assert value1['workStatus'] == 5
        except Exception:
            raise Exception
        finally:
            with allure.step('删除工单'):
                delete = DeleteWorkOrder()
                delete.json = {"ids": [id1, id2]}
                resp = delete.send()
                result = json.loads(resp.text)
                assert result['statusCode'] == 200

    @allure.story('工单管理-工单删除与终止')
    @allure.title('ISA-2881')
    def test_delete_work_order(self):
        """
        ISA-2881 : 删除工单
        1 选择一个工单数据，点击删除  弹出二次确认弹窗
        2 点击确定 工单信息从列表中删除
        """
        with allure.step('1 新建工单'):
            start_time = str(
                (datetime.datetime.now() + datetime.timedelta(minutes=0.5)).strftime("%Y-%m-%d %H:%M:%S"))  # 开始时间
            end_time = str(
                (datetime.datetime.now() + datetime.timedelta(minutes=0.6)).strftime("%Y-%m-%d %H:%M:%S"))  # 开始时间
            resp = WorkOrderAdd(workName='test1', workExecutor='operator', startTime=start_time,
                                endTime=end_time).send()
            result = resp.json()
            print(result)
            assert result['message'] == '操作成功'
        with allure.step('2 删除工单'):
            id_dict = self.db.select("select id from soc.soc_work_order_info where work_name='test1'")
            id = id_dict[0]['id']
            delete = DeleteWorkOrder()
            delete.json = {"ids": [id]}
            resp = delete.send()
            result = json.loads(resp.text)
            print(result)
            assert result['statusCode'] == 200
            assert result['message'] == '操作成功'
            resp = WorkOrderShow().send()
            show_result = resp.json()
            print(show_result)
            assert show_result['data']['total'] == 0

    # todo 增加 新增值班表案例;

    @allure.story('值班管理-新增值班表')
    @allure.title('ISA-2638')
    def test_check_legacy_work(self):
        """
        ISA-2638 :"新增值班表"页面点击“查看遗留工作”按钮，出现遗留工作弹窗
        1 点击”查看遗留工作“按钮  出现"遗留工作"弹窗
        """
        try:
            resp = AddAttendanceMangagement(remnant='遗留工作已完成', completed='已完成', noCompleted='test',
                                            workSummary='perfect').send()  # 新增值班表 交接未完成工作
            result = resp.json()
            print(result)
            with allure.step('1 点击”查看遗留工作“按钮'):
                resp = CheckNoCompleteWork().send()
                result = resp.json()
                print(result)
                with allure.step('出现"遗留工作"弹窗'):
                    assert result['data']['noCompletedWork'] == 'test'
        except Exception:
            raise Exception
        finally:
            #  删除值班表
            id_dict = self.db.select("select id from soc.soc_work_duty_info")
            id = [id['id'] for id in id_dict]
            DeleteWorkMangagement(id=id).send()

    @allure.story('值班管理-新增值班表')
    @allure.title('ISA-3491')
    def test_no_work_check_legacy_work(self):
        """
        ISA-3491 :若无遗留工作，点击“查看遗留工作”按钮，显示提示"暂无遗留工作"
        1 新增值班表，在交接未完成工作内不填入信息，其他信息填入合规内容，点击"确认"按钮  新增值班表成功
        2 再次点击"新增"值班表操作，点击“查看遗留工作”按钮  提示“暂无遗留工作”
        """
        try:
            with allure.step('1 新增值班表，在交接未完成工作内不填入信息，其他信息填入合规内容，点击"确认"按钮'):
                resp = AddAttendanceMangagement().send()  # 新增值班表 交接未完成工作
                result = resp.json()
                with allure.step('新增值班表成功'):
                    assert result['message'] == '操作成功'
            with allure.step('2 再次点击"新增"值班表操作，点击“查看遗留工作”按钮'):
                resp = CheckNoCompleteWork().send()
                result = resp.json()
                print(result)
                with allure.step('提示“暂无遗留工作”'):
                    assert result['data']['noCompletedWork'] == ''
        except Exception:
            raise Exception
        finally:
            # 删除值班表
            id_dict = self.db.select("select id from soc.soc_work_duty_info")
            id = [id['id'] for id in id_dict]
            DeleteWorkMangagement(id=id).send()

    @allure.story('值班管理-新增值班表')
    @allure.title('ISA-2647')
    def test_add_legacy_work_operator_log(self, get_header):
        """
        ISA-2647 : 点击“新增值班表”页面“确定”按钮，通过内容校验，新增值班表数据
        1 页面填入不合规内容，点击“确定”按钮  不合规内容在输入框下有提示信息
        2 页面填入合规内容，点击“确定”按钮，查看值班列表  1.提示“操作成功”  2.新增一条值班表数据
        3 使用audit用户登录系统，查看系统操作日志  该操作记录系统操作日志
        """
        try:
            with allure.step('2 页面填入合规内容，点击“确定”按钮，查看值班列表 '):
                resp = AddAttendanceMangagement().send()  # 新增值班表 交接未完成工作
                result = resp.json()
                with allure.step('1.提示“操作成功”  2.新增一条值班表数据'):
                    assert result['message'] == '操作成功'
            with allure.step('3 使用audit用户登录系统，查看系统操作日志'):
                time.sleep(2)
                audit = OperatorLog()
                audit.headers = get_header[2]
                resp = audit.send()
                result = resp.json()
                print(result)
                with allure.step('该操作记录系统操作日志'):
                    assert result['data']['list'][0]['context'] == '增加值班表[test]成功'
        finally:
            # 删除值班表
            id_dict = self.db.select("select id from soc.soc_work_duty_info")
            id = [id['id'] for id in id_dict]
            DeleteWorkMangagement(id=id).send()

    @allure.story('值班管理-修改值班表和删除值班表')
    @allure.title('ISA-2662')
    def test_mod_legacy_work(self, get_header):
        """
        ISA-2662 :任选一条“值班表”进行修改操作
        1 任选一条值班表，点击"编辑"按钮  进入“编辑值班表”页面
        2 修改该“值班表”内容，修改后的内容不合规，点击页面下方“确定”按钮  修改不合规内容的下方出现红字提示
        3 修改该“值班表”内容，修改后的内容合规，点击页面下方“确定”按钮  提示“操作成功”
        4 查看刚刚修改的值班表内容  内容被修改
        5 使用audit用户登陆系统，查看系统操作日志  修改值班表操作被记录
        """
        try:
            with allure.step('1 任选一条值班表，点击"编辑"按钮  进入“编辑值班表”页面'):
                resp = AddAttendanceMangagement().send()  # 新增值班表 交接未完成工作
                result = resp.json()
                assert result['message'] == '操作成功'
            with allure.step('3 修改该“值班表”内容，修改后的内容合规，点击页面下方“确定”按钮  提示“操作成功”'):
                id_dict = self.db.select("select id from soc.soc_work_duty_info")
                id = [id['id'] for id in id_dict]
                print(id)
                resp = ModAttendanceMangagement(id=id[0], name='test1').send()  # 新增值班表 交接未完成工作
                result = resp.json()
                assert result['message'] == '操作成功'
            with allure.step('4 查看刚刚修改的值班表内容  内容被修改'):
                resp = AttendanceMangagement().send()  # 查看值班管理
                result = resp.json()
                print(result)
                assert result['data']['list'][0]['workDutyName'] == 'test1'
            with allure.step('5 使用audit用户登陆系统，查看系统操作日志  修改值班表操作被记录'):
                time.sleep(2)
                log = OperatorLog()
                log.headers = get_header[2]
                resp = log.send()
                result = resp.json()
                print(result)
                assert result['data']['list'][0]['context'] == '修改值班表[test1]成功'
        finally:
            DeleteWorkMangagement(id=id).send()  # 删除值班表

    @allure.story('值班管理-修改值班表和删除值班表')
    @allure.title('ISA-2664')
    def test_delete_legacy_work_add_operator_log(self, get_header):
        """
        ISA-2664 : 【建议自动化-高】点击“修改值班表”的“删除”按钮，删除数据，记录该删除操作
        1 在值班表列表任选一条值班表数据，点击"删除"操作  有弹窗提示：”是否确认删除“
        2 在弹窗内点击”确认“按钮  提示”操作成功“
        3 在值班列表中查看该值班表  该值班表在值班列表中被删除
        4 使用audit用户登陆系统，查看系统操作日志  删除值班表操作被记录
        """
        with allure.step('1 在值班表列表任选一条值班表数据，点击"删除"操作'):
            resp = AddAttendanceMangagement().send()  # 新增值班表 交接未完成工作
            result = resp.json()
            assert result['message'] == '操作成功'

            with allure.step('删除成功'):
                id_dict = self.db.select("select id from soc.soc_work_duty_info")
                id = [id['id'] for id in id_dict]
                resp = DeleteWorkMangagement(id=id).send()  # 删除值班表
                result = resp.json()
                print(result)
                assert result['message'] == '操作成功'
        with allure.step('3 在值班列表中查看该值班表'):
            resp = AttendanceMangagement(keyword='test').send()
            result = resp.json()
            print(result)
        with allure.step('该值班表在值班列表中被删除'):
            assert result['data']['total'] == 0
        with allure.step('4 使用audit用户登陆系统，查看系统操作日志'):
            time.sleep(2)
            log = OperatorLog()
            log.headers = get_header[2]
            resp = log.send()
            result = resp.json()
            print(result)
        with allure.step('删除值班表操作被记录'):
            assert result['data']['list'][0]['context'] == '删除值班表[test]成功'
