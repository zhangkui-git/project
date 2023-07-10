'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/4/9 10:05
software: PyCharm
'''
import datetime
import time

import allure
import pytest

from api.isa.admin import SnmpTrapAdd, SnmpTrapQuery, DisableEnableUser, Iec104Edit, SnmpTrapDelete, DataBackupSave, \
    FullBackup, BackupQuery
from api.isa.alarm_handling import AlarmRetrieval
from api.isa.audit import OperatorLog
from api.isa.data_analysis import *
from api.isa.policy_config import *
from api.login_api import login_test
from common.dbutil import DB, Linux
from common.logger import GetLogger
from common.syslog import syslog
from config.config import local_ip, IP, linux_port, linux_pass, linux_user
from data.common_data import small_field, username, password, admin


@allure.feature('共有案例-数据分析')
class TestDataAnlays:
    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    # ISA-1478 二次范化为界面校验
    # @allure.story('日志检索')
    # @allure.title('ISA-1478 ')
    # def test_second_normalize_no_select_log(self):
    #     """
    #     ISA-1478 : 未选择日志点击二次范化时提示先选择日志
    #     不勾选任何日志,点击二次范化
    #     提示请选择要二次范化的日志
    #     """
    #     self.logging.info('')
    #     resp = SecondaryNormalize(rawLogStr='', sourceIp=local_ip, normalizeGroup='').send()
    #     result = resp.json()
    #     print(result)

    @allure.story('日志检索-日志检索左侧菜单树增加日志源分组、设备类型分组')
    @allure.title('ISA-1670 ')
    def test_add_log_source_influence_group(self):
        """
        ISA-1670 : 【已实现自动化】新增日志源对<日志源>分组和<设备类型>分组下的子级树的数据改变
        1 在“策略配置-日志源配置”页面，点击<新增>按钮  出现[新增日志源]窗口
        2
        1.填入符合要求的信息
        2.点击<确认>按钮
        弹出提示“操作成功”
        3
        1. 进入“日志分析-日志检索”页面，
        2. 查看<日志源>分组下的子级树
        3.查看<设备类型>分组下的子级树
        1. <日志源>分组新增子级树，子级树名称为新增日志源的日志源名称
        2. <设备类型>分组中增加新增日志源的设备类型子级树，如果此设备类型已存在，则不再添加
        """
        try:
            self.logging.info('获取所有分组')
            resp = GetGroup().send()
            result = resp.json()
            print(result)
            print(result['data'][1])
            source_list = [i['name'] for i in result['data'][1]['filters']]  # 日志源
            print(result['data'][2])
            asset_list = [i['name'] for i in result['data'][1]['filters']]  # 设备类型
            self.logging.info('新增日志源192.168.56.7')
            resp = AddLogSource(name='192.168.56.7', ip='192.168.56.7').send()
            result = resp.json()
            print(result)
            pytest.assume(resp.status_code == 200)
            self.logging.info('获取所有分组')
            resp = GetGroup().send()
            result = resp.json()
            print(result)
            self.logging.info('判断日志源IP地址')
            # print(result['data'][1])
            name_list = [i['name'] for i in result['data'][1]['filters']]
            print(name_list)
            if '192.168.56.7' not in source_list:  # 如果ip不在日志源分组内新增
                pytest.assume(name_list[-1] == '192.168.56.7')
            else:
                pytest.assume('192.168.56.7' in name_list)
            self.logging.info('判断设备类型')
            # print(result['data'][2])
            name_list = [i['name'] for i in result['data'][2]['filters']]
            print(name_list)
            if '可编程逻辑控制器' in asset_list:  # 如果可编程逻辑控制器在设备类型，前后无变化
                pytest.assume(asset_list == name_list)
            else:
                pytest.assume(name_list[-1] == '可编程逻辑控制器')
        except Exception:
            raise Exception
        finally:
            self.logging.info('删除日志源192.168.56.7')
            id = self.db.select("select id from soc.soc_log_source_info where asset_ip='192.168.56.7'")
            ids = [i['id'] for i in id]
            resp = DeleteLogSource(ids).send()
            pytest.assume(resp.status_code == 200)

    @allure.story('日志检索-日志检索左侧菜单树增加日志源分组、设备类型分组')
    @allure.title('ISA-1673')
    def test_delete_log_source_influence_group(self):
        """
        ISA-1673 : 删除日志源对<日志源>分组和<设备类型>分组下子级树的数据改变
        1 在“策略配置-日志源配置”页面，勾选1条日志源信息，点击<删除>按钮  被勾选的日志源被删除，提示“操作成功 ”
        2
        1.进入“日志分析-日志检索”页面，
        2.查看<日志源>分组下的子级树
        3.查看<设备类型>分组下的子级树
        1.<日志源>分组下子级树中，与被删除日志源相同日志源名称的子级树也会被删除
        2.<设备类型>分组下子级树中，若还有其他相同类型的设备的日志源则此条子级树保留，若没有被删除日志源相同日志源设备类型的设备则子级树将被删除
        """
        self.logging.info('新增日志源192.168.56.7')
        resp = AddLogSource(name='192.168.56.7', ip='192.168.56.7').send()
        result = resp.json()
        print(result)
        pytest.assume(resp.status_code == 200)
        self.logging.info('删除日志源192.168.56.7')
        id = self.db.select("select id from soc.soc_log_source_info where asset_ip='192.168.56.7'")
        ids = [i['id'] for i in id]
        resp = DeleteLogSource(ids).send()
        pytest.assume(resp.status_code == 200)
        self.logging.info('获取所有分组')
        resp = GetGroup().send()
        result = resp.json()
        print(result)
        self.logging.info('判断日志源IP地址')
        # print(result['data'][1])
        name_list = [i['name'] for i in result['data'][1]['filters']]
        print(name_list)
        pytest.assume('192.168.56.7' not in name_list)  # 192.168.56.7 不在日志源分组
        self.logging.info('判断设备类型')
        name_list = [i['name'] for i in result['data'][2]['filters']]
        print(name_list)
        asset_type = self.db.select("select fk_asset_type_path from soc.soc_log_source_info")  # 数据库查询设备类型
        print(asset_type)
        type = [i['fk_asset_type_path'] for i in asset_type]
        if '101001' in type:  # 如果可编程逻辑控制器在设备类型，前后无变化
            pytest.assume('可编程逻辑控制器' in name_list)
        else:
            pytest.assume('可编程逻辑控制器' not in name_list)

    @allure.story('日志检索-日志检索左侧菜单树增加日志源分组、设备类型分组')
    @allure.title('ISA-1674')
    def test_mod_log_source_influence_group(self):
        """
        ISA-1674 : 修改日志源信息对<日志源>分组和<设备类型>分组下的子级树数据的改变
        1 在“策略配置-日志源配置”页面，选择1条日志源信息，进行“编辑”操作，修改日志源名称(原名称:123，现名称:321)
        1.若该名称已存在，则弹出“日志源名称重复”的提示信息
        2.若该名称不存在，则弹出提示信息“操作成功”
        2
        1.进入“日志分析-日志检索”页面
        2.查看<日志源>分组下的子级树
        3.查看<设备类型>分组下的子级树
        1.<日志源>分组子级树下的名称将修改为新的日志源名称（由123改为321）
        2.<设备类型>分组子级树下的子级树无变化
        3 在“策略配置-日志源配置”页面，选择1条日志源信息，进行“编辑”操作，修改日志源的设备类型  弹出提示信息“操作成功”
        4
        1.进入“日志分析-日志检索”页面，
        2.查看<日志源>分组下的子级树
        3.查看<设备类型>分组下的子级树
        1.<日志源>分组子级树无变化
        2.若<设备类型>分组子级树含有该类型的设备则无变化，若<设备类型>分组子级树不含有该类型的设备则新添加子级树，名称为此设备类型
        5 在“策略配置-日志源配置”页面，选择1条日志源信息，进行“编辑”操作，修改日志源名称与日志源的设备类型
        1.若该名称已存在，则弹出“日志源名称重复”的提示信息
        2.若该名称不存在，则弹出提示信息“操作成功”
        6
        1.进入“日志分析-日志检索”页面，
        2.查看<日志源>分组下的子级树
        3.查看<设备类型>分组下的子级树
        1.<日志源>分组子级树下的名称将修改为新的日志源名称
        2.若<设备类型>分组子级树含有该类型的设备则无变化，若<设备类型>分组子级树不含有该类型的设备则新添加子级树，名称为此设备类型
        """
        try:
            self.logging.info('获取所有分组')
            resp = GetGroup().send()
            result = resp.json()
            print(result)
            print(result['data'][1])
            source_list = [i['name'] for i in result['data'][1]['filters']]  # 日志源
            print(result['data'][2])
            asset_list = [i['name'] for i in result['data'][2]['filters']]  # 设备类型
            self.logging.info('新增日志源192.168.56.7')
            resp = AddLogSource(name='192.168.56.7', ip='192.168.56.7').send()
            result = resp.json()
            print(result)
            pytest.assume(resp.status_code == 200)
            self.logging.info('修改日志源为192.168.56.77')
            id = self.db.select("select id from soc.soc_log_source_info where asset_ip='192.168.56.7'")
            source_id = [i['id'] for i in id]
            resp = ModLogSource(name='192.168.56.77', ip='192.168.56.77', id=source_id[0]).send()
            print(ModLogSource(name='192.168.56.77', ip='192.168.56.77').json)
            result = resp.json()
            print(result)
            self.logging.info('获取所有分组')
            resp = GetGroup().send()
            result = resp.json()
            print(result)
            self.logging.info('判断日志源IP地址')
            # print(result['data'][1])
            name_list = [i['name'] for i in result['data'][1]['filters']]
            print(name_list)
            pytest.assume('192.168.56.7' not in name_list)  # 192.168.56.7 不在日志源分组
            pytest.assume('192.168.56.77' in name_list)  # 192.168.56.77 在日志源分组
            self.logging.info('判断设备类型')
            # print(result['data'][2])
            name_list = [i['name'] for i in result['data'][2]['filters']]
            pytest.assume(asset_list == name_list)  # 设备类型不变
            # 修改设备类型
            self.logging.info('获取所有分组')
            resp = GetGroup().send()
            result = resp.json()
            print(result)
            print(result['data'][1])
            source_list = [i['name'] for i in result['data'][1]['filters']]  # 日志源
            print(result['data'][2])
            asset_list = [i['name'] for i in result['data'][1]['filters']]  # 设备类型
            self.logging.info('修改设备类型为192.168.56.77')
            resp = ModLogSource(name='192.168.56.77', ip='192.168.56.77', assetType=101002, id=source_id[0]).send()
            result = resp.json()
            print(result)
            self.logging.info('获取所有分组')
            resp = GetGroup().send()
            result = resp.json()
            print(result)
            self.logging.info('判断日志源IP地址')
            # print(result['data'][1])
            name_list = [i['name'] for i in result['data'][1]['filters']]
            print(name_list)
            pytest.assume('192.168.56.77' in name_list)  # 192.168.56.77 在日志源分组
            self.logging.info('判断设备类型')
            # print(result['data'][2])
            name_list = [i['name'] for i in result['data'][2]['filters']]
            print(name_list)
            pytest.assume('远程终端控制系统' in name_list)  # 设备类型改变
            # 同时修改日志源名称和设备类型
            self.logging.info('修改设备类型为192.168.56.77')
            resp = ModLogSource(name='192.168.56.78', ip='192.168.56.78', assetType=101003, id=source_id[0]).send()
            result = resp.json()
            print(result)
            self.logging.info('获取所有分组')
            resp = GetGroup().send()
            result = resp.json()
            print(result)
            self.logging.info('判断日志源IP地址')
            # print(result['data'][1])
            name_list = [i['name'] for i in result['data'][1]['filters']]
            print(name_list)
            pytest.assume('192.168.56.78' in name_list)  # 192.168.56.77 在日志源分组
            self.logging.info('判断设备类型')
            # print(result['data'][2])
            name_list = [i['name'] for i in result['data'][2]['filters']]
            print(name_list)
            pytest.assume('集散控制系统' in name_list)  # 设备类型改变
        except Exception:
            raise Exception
        finally:
            self.logging.info('删除日志源')
            ids = [i['id'] for i in id]
            resp = DeleteLogSource(ids).send()
            pytest.assume(resp.status_code == 200)


@allure.feature('共有案例-策略配置')
class TestPolicyConfig:
    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    @allure.story('日志范化-SNMP OID')
    @allure.title('ISA-1386')
    def test_oid_must_input(self):
        """
        ISA-1386 : 新增SNMP OID时oid为必填项
        1 点击新增，弹出“创建snmp oid”页面  “oid”有必填项标识
        2 “OID”输入为空，其他项均正确输入 点击保存  提示oid不能为空
        """
        resp = SnmpOidAdd(oid='').send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == 'oid长度需要在1和64之间')

    @allure.story('日志范化-SNMP OID')
    @allure.title('ISA-1387')
    def test_oid_Overrun(self):
        """
        ISA-1387 : 【已实现自动化】新增SNMP OID时oid最大长度不超过64个字符
        1 点击新增  弹出创建snmp oid页面
        2 “OID”输入框输入65个字符  前端页面限制截取64个字符

        3 其他项正确输入，点击保存  长度为64字符的oid保存成功
        """
        resp = SnmpOidAdd(oid=small_field + '123').send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == 'oid长度需要在1和64之间')

    @allure.story('日志范化-SNMP OID')
    @allure.title('ISA-1426')
    def test_batch_delete_snmp(self):
        """
        ISA-1426 : 批量删除SNMP OID
        1 选择两条自定义数据，点击列表的删除  弹出二次确认弹窗
        2 点击确定  选择的两条数据从列表中删除
        """
        self.logging.info('新增两条snmp oid数据')
        resp = SnmpOidAdd(oid='.1.2.3.4', name='test1').send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '操作成功')
        resp = SnmpOidAdd(oid='.1.2.3.4.5', name='test2', fkNormalizeFieldId='5e4b9aa1aedaa116acddda25',
                          fkNormalizeFieldAlias='http访问uri').send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '操作成功')
        self.logging.info('删除两条数据')
        id = self.db.select("select id from soc.soc_normalize_snmp_oid_info where is_custom='1'")  # 数据库查询自定义可删除的id
        id_list = [i['id'] for i in id]
        resp = SnmpOidDelete(ids=id_list).send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '2条数据删除成功！')

    @allure.story('日志范化-SNMP OID')
    @allure.title('ISA-1432')
    def test_search_snmp(self):
        """
        ISA-1432 : 检索SNMP OID
        1 在列表检索输入框中输入oid关键字，如.1.1 点击搜索  列表搜索出oid包含.1.1的所有数据
        2 在列表检索输入框中输入名称关键字，如te 点击搜索  列表搜索出名称包含te的所有数据
        """
        try:
            # todo 增加特殊字符的校验
            self.logging.info('新增1条snmp oid数据')
            resp = SnmpOidAdd(oid='.1.2.3.4', name='test1').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('检索snmp .1.2.3')
            resp = SnmpOidQuery(keywordContent='.1.2.3').send()
            result = resp.json()
            print(result)
            pytest.assume(result['data']['total'] == 1)  # 判断只有一条数据
            pytest.assume(result['data']['list'][0]['oid'] == '.1.2.3.4')
            self.logging.info('检索snmp te')
            resp = SnmpOidQuery(keywordContent='test').send()
            result = resp.json()
            pytest.assume(result['data']['total'] == 1)  # 判断只有一条数据
            pytest.assume(result['data']['list'][0]['oid'] == '.1.2.3.4')
            pytest.assume(result['data']['list'][0]['name'] == 'test1')
        except Exception:
            raise Exception
        finally:
            self.logging.info('删除1条数据')
            id = self.db.select("select id from soc.soc_normalize_snmp_oid_info where is_custom='1'")  # 数据库查询自定义可删除的id
            id_list = [i['id'] for i in id]
            resp = SnmpOidDelete(ids=id_list).send()
            result = resp.json()
            pytest.assume(result['message'] == '1条数据删除成功！')

    # todo 增加查看1427
    @allure.story('日志范化-SNMP OID')
    @allure.title('ISA-1427')
    def test_check_snmp_oid(self):
        """
        ISA-1427 : 查看SNMP OID
        1 选择一条snmp oid数据，点击操作列的查看
        弹出snmp oid查看弹窗,页面显示snmp oid数据
        """
        with allure.step('1 选择一条snmp oid数据，点击操作列的查看'):
            id_idct = self.db.select("select id from soc.soc_normalize_snmp_oid_info where description='磁盘索引节点使用率'")
            id = id_idct[0]['id']
            resp = SnmpOidCheck(id=id).send()
            result = resp.json()
            print(result)
            with allure.step('1 选择一条snmp oid数据，点击操作列的查看'):
                assert result['data']['list'][0]['oid'] == '.1.3.6.1.4.1.2021.9.1.10' and result['data']['list'][0]['name'] == 'dskPercentNode' and result['data']['list'][0]['fkNormalizeFieldAlias'] == '磁盘索引节点使用率' and result['data']['list'][0]['description'] == '磁盘索引节点使用率'


    @allure.story('日志范化-SNMP OID')
    @allure.title('ISA-1655')
    def test_inner_data_undelete(self):
        """
        ISA-1655 : 系统内置内置数据不可删除
        1 通过勾选框选中系统内置数据，点击列表的删除  提示系统内置数据不可删除
        """
        self.logging.info('删除内置数据')
        id_dict = self.db.select(
            "select id from soc.soc_normalize_snmp_oid_info where is_custom='2' order by create_time limit 1")  # 查询一条内置数据
        id = [i['id'] for i in id_dict]
        print(id)
        resp = SnmpOidDelete(id).send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '存在1个内置数据，无法删除！')

    @allure.story('日志范化-SNMP OID')
    @allure.title('ISA-1429')
    def test_associated_fields_snmp_delete(self):
        """
        ISA-1429 : SNMP OID关联字段后，该字段不可删除
        1 创建一个snmp oid数据，字段选择自定义创建的字段  snmp oid数据创建成功
        2 进入范化策略-字段，删除snmp oid中选择的字段  提示snmp oid关联字段不可删除
        """
        try:
            self.logging.info('新增字段')
            resp = FieldAdd().send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('新增关联新增字段的snmp')
            field_id = self.db.select("select field_id from soc.soc_normalize_field_info where field_alias='testtest'")
            id = [field['field_id'] for field in field_id]
            print(id)
            resp = SnmpOidAdd(fkNormalizeFieldId=id[0], fkNormalizeFieldAlias='testtest').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('删除字段')
            resp = FieldDelete(id).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '存在1个被SNMP OID关联字段，无法删除！')
        except Exception:
            raise Exception
        finally:
            self.logging.info('删除snmp数据')
            snmp_id = self.db.select(
                "select id from soc.soc_normalize_snmp_oid_info where is_custom='1'")  # 数据库查询自定义可删除的id
            id_list = [i['id'] for i in snmp_id]
            resp = SnmpOidDelete(ids=id_list).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '1条数据删除成功！')
            self.logging.info('删除字段')
            resp = FieldDelete(id).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '1条数据删除成功！')

    # todo 1440\1441
    @allure.story('日志范化-SNMP OID')
    @allure.title('ISA-1440')
    def test_field_only_one_snmp_oid(self):
        """
        ISA-1440 : 同一个字段只能对应一个自定义oid
        1 创建一个snmp oid，关联创建的自定义字段，测试字段,其他项正确输入,点击保存
        snmp oid创建成功
        2 再次新增snmp oid，字段选择创建的自定字段，如测试字段,其他项正确输入,点击保存
        关联字段已被关联，不允许重复配置
        """
        try:
            self.logging.info('新增字段')
            resp = FieldAdd().send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('1 创建一个snmp oid，关联创建的自定义字段，测试字段,其他项正确输入,点击保存')
            field_id = self.db.select("select field_id from soc.soc_normalize_field_info where field_alias='testtest'")
            id = [field['field_id'] for field in field_id]
            print(id)
            resp = SnmpOidAdd(fkNormalizeFieldId=id[0], fkNormalizeFieldAlias='testtest').send()
            result = resp.json()
            print(result)
            self.logging.info('snmp oid创建成功')
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('2 再次新增snmp oid，字段选择创建的自定字段，如测试字段,其他项正确输入')
            resp = SnmpOidAdd(oid=".12.2.3", name='test1', fkNormalizeFieldId=id[0], fkNormalizeFieldAlias='testtest').send()
            result = resp.json()
            print(result)
            self.logging.info('关联字段已被关联，不允许重复配置')
            pytest.assume(result['message'] == '关联字段已被关联，不允许重复配置')
        except Exception:
            raise Exception
        finally:
            self.logging.info('删除snmp数据')
            snmp_id = self.db.select(
                "select id from soc.soc_normalize_snmp_oid_info where is_custom='1'")  # 数据库查询自定义可删除的id
            id_list = [i['id'] for i in snmp_id]
            resp = SnmpOidDelete(ids=id_list).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '1条数据删除成功！')
            self.logging.info('删除字段')
            resp = FieldDelete(id).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '1条数据删除成功！')


    # @allure.story('日志范化-字段组配置')
    # @allure.title('ISA-1441')
    # @pytest.mark.skip('失败')
    # def test_inner_field_only_one_snmp_oid(self):
    #     """
    #     ISA-1441 : 内置oid可以与自定义oid对应同一个字段
    #     1 新增snmp oid，字段选择内置oid已经关联的字段,其他项正确输入,点击保存
    #     oid创建成功
    #     2 接收同时含有关联同一个字段的自定义oid和内置oid的snmp trap日志,查看日志检索字段范化
    #     只解析自定义oid中的字段,内置的snmp oid字段没有解析
    #     """
    #     try:
    #
    #         self.logging.info('新增字段')
    #         resp = FieldAdd().send()
    #         result = resp.json()
    #         print(result)
    #         pytest.assume(result['message'] == '操作成功')
    #         field_dict = self.db.select("select field_id from soc.soc_normalize_field_info where field_name='test'")
    #         field = field_dict[0]['field_id']
    #         print(field)
    #         # 数据库插入内置oid
    #         # self.db.update(f"INSERT INTO `soc`.`soc_normalize_snmp_oid_info` (`id`, `oid`, `name`, `description`, `is_custom`, `fk_normalize_field_id`, `create_time`, `update_time`) VALUES ('76', '.1.3.6.1.4.1.51011.3.100102', 'test', 'test', '2', '{field}', '2021-11-26 12:08:32', '2021-11-26 12:08:32')")
    #         # time.sleep(2)
    #         self.logging.info('新增snmp oid，字段选择内置oid已经关联的字段,其他项正确输入,点击保存')
    #         field_id = self.db.select("select field_id from soc.soc_normalize_field_info where field_alias='qqq'")
    #         id = [field['field_id'] for field in field_id]
    #         print(id)
    #         resp = SnmpOidAdd(oid=".1.3.6.1.4.1.51011.3.100102", name='test12', fkNormalizeFieldId=id[0], fkNormalizeFieldAlias='qqq').send()
    #         result = resp.json()
    #         print(result)
    #         self.logging.info('oid创建成功')
    #         pytest.assume(result['message'] == '操作成功')
    #
    #         self.logging.info('1输入服务器IP，如：“192.168.4.196”，服务器端口“162”，SNMP版本选择“V1”, 团体字符串输入“test123”,打开状态开关，点击“确定”按钮')
    #         add = SnmpTrapAdd(ip=IP, status=1)
    #         header = login_test(admin, password)
    #         add.headers = header
    #         resp = add.send()
    #         result = resp.json()
    #         print(result)
    #         if pytest.assume(result['message'] == '操作成功'):
    #             self.logging.info('提示“操作成功”，页面新增该条服务器信息')
    #         else:
    #             self.logging.info('步骤1结果失败')
    #         self.logging.info('2在192.168.4.196上，配置日志源信息，协议类型选择“SNMP Trap协议”，设备IP（A网）输入步骤一中的机器IP，团体字符串输入"test123",其他参数合规即可')
    #         id_dict = self.db.select("select id FROM `soc`.`soc_log_source_info` WHERE  `asset_ip`='{}'".format(local_ip))  # 获取本机日志源id
    #         id= id_dict[0]['id']
    #         header = login_test(name=username, pwd=password)
    #         add = AddLogSource(name=IP, ip=IP, protocolType=5, community='test', normalizeGroup=["1393", "1386", "1400", "11404"], ftpMode=1)
    #         resp = add.send()  # 修改日志源信息
    #         result = resp.json()
    #         print(result)
    #         if pytest.assume('操作成功' in result['message']):
    #             self.logging.info('保存该日志源成功')
    #         else:
    #             self.logging.info('步骤2结果失败')
    #         self.logging.info('3 当测试机器产生新的告警信息时，立刻校验192.168.4.196中的日志检索页面信息')
    #         syslog('5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.100.124|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配|^1|^null|^201229008|^')  #  发送日志
    #         time.sleep(60)
    #         #   查看日志检索产生日志
    #         log = LogRetrieve()
    #         resp = log.send()
    #         result = resp.json()
    #         print(result)
    #         log1 = result['dataList'][0]['originlog']
    #         log1_header, log1_tail = log1.split('|')[0], log1.split('|')[2:]
    #         # print(log1_header, log1_tail)
    #         log2 = result['dataList'][1]['originlog']
    #         log2_header, log2_tail = log2.split('|')[0], log2.split('|')[2:]
    #         # print(log2_header, log2_tail)
    #         # test2 = pytest.assume(result['dataList'][0]['originlog'] == '1.3.6.1.4.1.51011.3.100102 = 100102|^2022-04-15 16:56:48|^重要|^地址欺诈|^XX区域|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配'or result['dataList'][1]['originlog'] == '1.3.6.1.4.1.51011.3.100102 = 100102|^2022-04-15 16:56:48|^重要|^地址欺诈|^XX区域|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配')
    #         test2 = pytest.assume(log1_header == '1.3.6.1.4.1.51011.3.100102 = 100102' and log1_tail == ['^重要', '^地址欺诈', '^XX区域', '^192.168.100.123', '^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配'] or log2_header == '1.3.6.1.4.1.51011.3.100102 = 100102' and log2_tail == ['^重要', '^地址欺诈', '^XX区域', '^192.168.100.123', '^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配'])
    #         if test2:
    #             self.logging.info('1.日志检索页面产生对应的日志信息 2.日志信息，格式如“ 1.3.6.1.2.1.11.30 =100102|^2021-11-02 10:21:29|^一般|^尝试系统调用|^XX区域|^192.168.40.135|^违反规则访问关键文件或注册表的行为”')
    #         else:
    #             self.logging.info('步骤3结果失败')
    #     except Exception:
    #         raise Exception
    #     finally:
    #         # self.logging.info('删除snmp数据')
    #         # snmp_id = self.db.select(
    #         #     "select id from soc.soc_normalize_snmp_oid_info where is_custom='1'")  # 数据库查询自定义可删除的id
    #         # id_list = [i['id'] for i in snmp_id]
    #         # print(id_list)
    #         # resp = SnmpOidDelete(ids=id_list).send()
    #         # result = resp.json()
    #         # print(result)
    #         # pytest.assume(result['message'] == '1条数据删除成功！')
    #         # self.db.update("DELETE FROM `soc`.`soc_normalize_snmp_oid_info` WHERE  `name`='test'")
    #         # time.sleep(2)
    #         # self.logging.info('删除字段')
    #         # resp = FieldDelete(id).send()
    #         # result = resp.json()
    #         # print(result)
    #         # pytest.assume(result['message'] == '1条数据删除成功！')
    #         # self.logging.info('删除服务器配置')
    #
    #         id_dict = self.db.select("select id FROM `soc`.`soc_snmp_trap_config` WHERE ip='{}'".format(IP))
    #         id = [id['id'] for id in id_dict]
    #         delete = SnmpTrapDelete(id=id)
    #         header = login_test(admin, password)
    #         delete.headers = header
    #         resp = delete.send()
    #         result = resp.json()
    #         print(result)
    #         # self.db.update("DELETE FROM `soc`.`soc_snmp_trap_config` WHERE ip='{}'".format(IP))   # 删除snmp配置
    #         self.db.update("DELETE FROM `soc`.`soc_log_source_info` WHERE asset_ip='{}'".format(IP))  # 删除日志源

    @allure.story('日志范化-字段组配置')
    @allure.title('ISA-1490')
    def test_field_group_show(self):
        """
        ISA-1490 : 字段组页面左侧新增字段分组
        1 查看页面左侧新增字段组  新增系统内置的字段组
        2 点击字段组名称，如“日志公共字段” ,查看字段筛选  筛选出“日志公共字段”下所有字段
        """
        self.logging.info('查看字段组')
        resp = FieldGroupShow().send()
        result = resp.json()
        print(result)
        data = result['data']
        field_list = [file_group['label'] for file_group in data]
        print(field_list)
        name_list = self.db.select("select name from soc.soc_normalize_field_group")  # 数据库查询字段组
        name = [name['name'] for name in name_list]
        print(name)
        pytest.assume(len(field_list) > 0)
        pytest.assume(field_list == name)
        self.logging.info('查看日志公共字段')
        resp = GroupFieldShow().send()
        result = resp.json()
        print(result)
        name_list = self.db.select(
            "select field_alias from soc.soc_normalize_field_info where field_group=1")  # 数据库查询日志公共下的字段
        name = [name['field_alias'] for name in name_list]
        pytest.assume(result['message'] == '操作成功')
        print(result['data']['total'])
        pytest.assume(result['data']['total'] == len(name))

    @allure.story('日志范化-字段组配置')
    @allure.title('ISA-1724')
    def test_field_delete_faild(self):
        """
        ISA-1724 : 字段组下有字段无法删除(包含字段组的增删改)
        1 选择一个有字段的字段组，点击删除  弹出二次确认删除的弹窗
        2 点击确定  提示字段组下有字段，不可删除
        """
        try:
            self.logging.info('新增字段组')
            resp = FieldGroupAdd().send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('修改字段组')
            group_id = self.db.select("select id from soc.soc_normalize_field_group where name='test_group'")
            print(group_id)
            id = group_id[0]['id']
            resp = FieldGroupMod(id=id, name='test_group1').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('字段组下添加字段')
            resp = FieldAdd(fieldGroup=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('字段组下有字段删除字段组')
            resp = FieldGroupDelete(id=id, name='test_group1').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '字段组下有字段，不可删除')
        except Exception:
            raise Exception
        finally:
            field_id = self.db.select("select field_id from soc.soc_normalize_field_info where field_name='test'")
            # field_id = group_id[0]['group_id']
            field_id = [field['field_id'] for field in field_id]
            print(field_id)
            self.logging.info('字段删除字段')
            resp = FieldDelete(id=field_id).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '1条数据删除成功！')
            self.logging.info('字段组下有字段删除字段组')
            resp = FieldGroupDelete(id=id, name='test_group1').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')

    @allure.story('日志范化-字段组配置')
    @allure.title('ISA-1514')
    def test_field_delete_sucess(self):
        """
        ISA-1514 : 字段组下无字段可删除字段组
        1 选择创建的字段组，点击删除  弹出二次确认删除的弹窗
        2 点击确定  字段组删除成功
        """

        self.logging.info('新增字段组')
        resp = FieldGroupAdd().send()
        result = resp.json()
        pytest.assume(result['message'] == '操作成功')
        group_id = self.db.select("select id from soc.soc_normalize_field_group where name='test_group'")
        print(group_id)
        id = group_id[0]['id']
        self.logging.info('删除字段组')
        resp = FieldGroupDelete(id=id, name='test_group').send()
        result = resp.json()
        pytest.assume(result['message'] == '操作成功')

    @allure.story('日志范化-agent_后台进程')
    @allure.title('ISA-3415')
    def test_cyber_threats_log(self):
        """
        ISA-3415 : 测试网络威胁相关日志范化处理
        1 在"策略配置-日志范化"检索"网络威胁感知"，点击查看，复制日志样本，使用udpsend发送该日志，日志源的范化策略选择"安全设备 / 安全审计 / 网络威胁感知系统"
        该日志范化成功，范化策略名称为"网络威胁感知系统"，日志分类：/攻击入侵/apt恶意软件活动，类别与大类别显示：/攻击入侵/apt恶意软件活动
        """
        try:
            id = self.db.select("select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))
            id = id[0]['id']
            self.logging.info('修改日志源-安全设备/安全审计/网络威胁感知系统')
            resp = ModLogSource(name=local_ip, ip=local_ip, normalizeGroup=[1392], id=id).send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)
            time.sleep(1)
            self.logging.info('发送网络威胁日志')
            syslog(
                '<8>Apr 15 19:00:25 yice-PC <14>1 2022-03-17T06:41:14.012Z 10.0.0.5 notice - - - 1550763919473^ATD^10.1.0.32^NDE^b14d0543-3bcc-472e-8d05-433bcc572eab^p4p2^11000003^apt^apt-malware^APT-Anunak^1.1.1.4^44782^^1.1.1.1^21868^^tcp^ftp^malware-download^^^4^7^MALWARE::Variant.Cabby.3^874058e8d8582bf85c115ce319c5b0af^method:;status_code:;host:;uri:unknown;^APT attack malware found in file inspection engine^Australia^^-33.494,143.2104^AU^Australia^^-33.494,143.2104^AU^^^^^^^^^^^unknown^^^unknown^application/x-dosexec^^^^^^^^^^Ws9zCdP3qHz8eHPZcKApf3SRlMU=^ais^^^^^^^^^^^{"file":{"av":"1/4","gene":"False","fuid":"File-ATD-node-3-47055c1a-35ef-11e9-b46d-a4bf0154d09d","platform":"windows"}}^^exe^47cf1ce07da791fe9252d102d79149aab51a9d96b9aa2f3b7afb50a51277be5a^3072:su2q9BIau/qCVjvoXCwWg2n/pujQiJweZ7SZ1LOlODa4+J3881TZVn3lpgA:OqbQVT5wWgsGJw2WlOeaA81Ln7^874058e8d8582bf85c115ce319c5b0af^anti-sandbox, hide, recon, abnormal, anti-emu, packer, APT_Anunak, suspfile, fake, injection, shellcode, persistence, unpacking^874058e8d8582bf85c115ce319c5b0af')
            time.sleep(40)
            resp = LogRetrieve().send()
            result = resp.json()
            print(result)
            print(result['dataList'][0]['eventcategory'])
            pytest.assume(result['dataList'][0]['eventcategory'] == '攻击入侵/apt恶意软件活动' and result['dataList'][0]['classtype'] == '/攻击入侵/apt恶意软件活动')
        except Exception:
            raise Exception
        finally:
            self.logging.info('恢复日志源')
            resp = ModLogSource(name=local_ip, ip=local_ip, normalizeGroup=[1393, 1386, 1400, 11404], id=id).send()
            result = resp.json()
            pytest.assume(result['statusCode'] == 200)

    @allure.story('日志源配置-导入日志源')
    @allure.title('ISA-1648')
    def test_upload_overtake_five_million(self):
        """
        ISA-1648 : 上传的文件大小上限为100K
        1 在已确认日志源-导入数据-文件上传，选择文件A  导入成功
        2 在已确认日志源-导入数据-文件上传，选择文件B  导入成功
        3 在已确认日志源-导入数据-文件上传，选择文件C  导入失败，提示文件大小不能大于100K
        """
        try:
            self.logging.info('导入文件小于100K')
            resp = LogSourceImport(file='日志源信息_小于5M.xlsx').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('导入文件大于100K')
            resp = LogSourceImport(file='日志源信息_等于5M.xlsx').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '导入失败：文件最大为100k！')
        except Exception:
            raise Exception
        finally:
            self.logging.info('删除日志源')
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='192.168.4.179'")  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            resp = DeleteLogSource(ids=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')

    @allure.story('日志源配置-导入日志源')
    @allure.title('ISA-1814')
    def test_upload_log_source_correct(self):
        """
        ISA-1814 : 表格中日志源的所属范化组有多个，导入后界面显示正确，没有遗漏
        1 在日志源excel表格中手动输入日志源信息，所属范化组按书写规范，写入过个系统存在的范化组；导入该日志源  导入成功
        2 在已确认日志源界面查看步骤1导入日志源的所属范化组  范化组个数正确；每个范化组名称都正确
        """
        try:
            self.logging.info('导入文件')
            resp = LogSourceImport(file='日志源信息_小于5M.xlsx').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('查看日志源')
            resp = LogSourcePage().send()
            result = resp.json()
            print(result)
            pytest.assume(
                result['data']['logSourceList']['list'][0]['normalizeGroup'] == '统一安全管理平台，安全隔离与信息交换系统，安全配置核查，工业互联防火墙')
        except Exception:
            raise Exception
        finally:
            self.logging.info('删除日志源')
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='192.168.4.179'")  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            resp = DeleteLogSource(ids=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')

    @allure.story('日志源配置-日志过滤')
    @allure.title('ISA-1636')
    def test_filter_keyword(self):
        """
        ISA-1636 : 【内容校验】过滤配置页面中，关键字输入框中可支持的输入内容为中文、字母、数字、特殊字符
        1 关键字输入框中输入“违反MODBUS白名单规则告警，功能码:03 Read Holding Registers；起始地址:100；结束地%^&*()（）:'"-_.~”，其他参数合规，点击“确定”按钮  提示“操作成功”
        2 关键字输入框中输入“违反MODBUS”，其他参数合规，点击“确定”按钮  提示“操作成功”
        3 关键字输入框中输入“；起始地址:100；结束地%^&*()（）:'"-_.~”，其他参数合规，点击“确定”按钮  提示“操作成功”
        """
        try:
            self.logging.info('关键字输入:违反MODBUS白名单规则告警，功能码:03 Read Holding Registers；起始地址:100；结束地%^&*()（）:\'"-_.~')
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
            id = id_dict[0]['id']
            resp = LogSourceFilter(id=id,
                                   keyWord='违反MODBUS白名单规则告警，功能码:03 Read Holding Registers；起始地址:100；结束地%^&*()（）:\'"-_.~').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('关键字输入:违反MODBUS')
            resp = LogSourceFilter(id=id, keyWord='违反MODBUS').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('关键字输入:；起始地址:100；结束地%^&*()（）:\'"-_.~')
            resp = LogSourceFilter(id=id, keyWord='；起始地址:100；结束地%^&*()（）:\'"-_.~').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')
        except Exception:
            raise Exception
        finally:
            self.logging.info('不过滤')
            resp = LogSourceFilter(id=id).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功')

    @allure.story('日志源配置-日志源配置增加连接故障判断')
    @allure.title('ISA-1827')
    def test_add_log_source_status(self):
        """
        ISA-1827 : 新增日志源，初始状态为未知
        1 创建一个日志源，日志源协议类型不是FTP/SFTP/WMI/SMB这四种类型，如syslog等  日志源创建成功
        2 查看该日志源的在线状态  日志源在线状态为未知
        """
        id_dict = self.db.select(
            "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
        id = [id['id'] for id in id_dict]
        self.logging.info('删除本机日志源')
        resp = DeleteLogSource(ids=id).send()
        result = resp.json()
        pytest.assume(result['message'] == '操作成功')
        self.logging.info('添加本机日志源')
        resp = AddLogSource(name=local_ip, ip=local_ip, normalizeGroup=["1393", "1386", "1400", "11404"]).send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '操作成功，自动生成资产[{}]'.format(local_ip))
        self.logging.info('查看日志源')
        resp = LogSourcePage().send()
        result = resp.json()
        print(result)
        pytest.assume(result['data']['logSourceList']['list'][0]['status'] == 2)  # 日志源在线状态为未知

    @allure.story('日志源配置-日志源配置增加连接故障判断')
    @allure.title('ISA-1828')
    def test_add_log_source_status(self):
        """
        ISA-1828 : 日志源上报日志后，日志源变为在线状态
        1 日志源上报日志  LAA/ISA接收到日志，最近日志时间更新
        2 查看日志源的在线状态  日志源的在线状态从未知变为在线
        """
        id_dict = self.db.select(
            "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
        id = [id['id'] for id in id_dict]
        self.logging.info('删除本机日志源')
        resp = DeleteLogSource(ids=id).send()
        result = resp.json()
        pytest.assume(result['message'] == '操作成功')
        self.logging.info('添加本机日志源')
        resp = AddLogSource(name=local_ip, ip=local_ip, normalizeGroup=["1393", "1386", "1400", "11404"]).send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '操作成功，自动生成资产[{}]'.format(local_ip))
        self.logging.info('查看日志源')
        resp = LogSourcePage().send()
        result = resp.json()
        print(result)
        pytest.assume(result['data']['logSourceList']['list'][0]['status'] == 2)  # 日志源在线状态为未知
        self.logging.info('发送一条日志')
        syslog(
            '5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.100.124|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配|^1|^null|^201229008|^')
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        time.sleep(5)
        self.logging.info('查看日志源')
        resp = LogSourcePage().send()
        result = resp.json()
        print(result)
        data = result['data']['logSourceList']['list'][0]  # 第一条日志源
        pytest.assume(data['status'] == 1)  # 日志源在线状态为在线
        print(now_time, data['latestReceiveTime'][:-3])
        pytest.assume(str(now_time) == data['latestReceiveTime'][:-3])  # LAA/ISA接收到日志，最近日志时间更新

    @allure.story('日志源配置-自发现日志源')
    @allure.title('ISA-2232')
    def test_close_auto_find_log_source_send_log(self):
        """
        ISA-2232 : 自发现日志源关闭，未在日志源列表的日志源上报日志
        1 客户端A向LAA/ISA上报syslog日志  syslog日志已发送
        2 从日志源配置界面中查找客户端A对应的日志源信息  没有客户端A对应的日志源信息
        """
        self.logging.info('关闭自发现日志源')
        resp = AutoFindLogSource(flag='flase').send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '关闭自发现日志源')
        id_dict = self.db.select(
            "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
        id = [id['id'] for id in id_dict]
        self.logging.info('删除本机日志源')
        resp = DeleteLogSource(ids=id).send()
        result = resp.json()
        pytest.assume(result['message'] == '操作成功')
        syslog(
            '5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.100.124|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配|^1|^null|^201229008|^')
        time.sleep(5)
        self.logging.info('查看日志源')
        resp = LogSourcePage().send()
        result = resp.json()
        print(result)
        data = result['data']['logSourceList']['list']  # 第一条日志源
        print(data)
        pytest.assume(data == [])  # 日志源为空
        self.logging.info('添加本机日志源')
        resp = AddLogSource(name=local_ip, ip=local_ip, normalizeGroup=["1393", "1386", "1400", "11404"]).send()
        result = resp.json()
        print(result)
        pytest.assume(result['message'] == '操作成功，自动生成资产[{}]'.format(local_ip))

    @allure.story('日志源配置-自发现日志源')
    @allure.title('ISA-2233')
    def test_open_auto_find_log_source_send_log(self):
        """
        ISA-2233 : 自发现日志源开启，未在日志源列表的日志源上报日志
        1 客户端A向LAA/ISA上报syslog日志  syslog日志已发送
        2 在日志源配置界面查找客户端A对应的日志源  能找到客户端A对应的日志源，且日志源的各字段信息正确
        """
        try:
            self.logging.info('打开自发现日志源')
            resp = AutoFindLogSource(flag='true').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '开启自发现日志源')
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            self.logging.info('删除本机日志源')
            resp = DeleteLogSource(ids=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            syslog(
                '5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.100.124|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配|^1|^null|^201229008|^')
            time.sleep(5)
            self.logging.info('查看日志源')
            resp = LogSourcePage().send()
            result = resp.json()
            print(result)
            data = result['data']['logSourceList']['list'][0]  # 第一条日志源
            print(data)
            print(type(eval(data['logSourceName'][6:])))
            pytest.assume(
                data['logSourceName'][:6] == '自发现日志源' and type(eval(data['logSourceName'][6:])) == int)  # 自发现日志源 + 数字
            pytest.assume(data['assetIp'] == local_ip)  # IP地址
            pytest.assume(data['normalizeGroup'] == '统一安全管理平台')  # 范化组
            pytest.assume(data['assetTypeName'] == '统一安全管理平台')  # 设备类型
        except Exception:
            raise Exception
        finally:
            self.logging.info('关闭自发现日志源')
            resp = AutoFindLogSource(flag='flase').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '关闭自发现日志源')
            self.logging.info('删除自发现日志源')
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            resp = DeleteLogSource(ids=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('添加本机日志源')
            resp = AddLogSource(name=local_ip, ip=local_ip, normalizeGroup=["1393", "1386", "1400", "11404"]).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功，自动生成资产[{}]'.format(local_ip))

    @allure.story('日志源配置-自发现日志源')
    @allure.title('ISA-2235')
    def test_mod_auto_find_log_source(self):
        """
        ISA-2235 : 修改自发现的日志源信息
        1 选择自发现的日志源，编辑，修改日志源名称、协议类型、设备IP、所属区域、所属范化组、设备类型，点击保存
        保存成功，自发现的日志源可以再次编辑
        """
        try:
            self.logging.info('打开自发现日志源')
            resp = AutoFindLogSource(flag='true').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '开启自发现日志源')
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            self.logging.info('删除本机日志源')
            resp = DeleteLogSource(ids=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            syslog(
                '5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.100.124|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配|^1|^null|^201229008|^')
            time.sleep(5)
            self.logging.info('查看日志源')
            resp = LogSourcePage().send()
            result = resp.json()
            print(result)
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            self.logging.info('修改日志源')
            resp = ModLogSource(name='test', ip=local_ip, assetType=101002, normalizeGroup=["1393"], id=id[0]).send()
            result = resp.json()
            print(result)
            self.logging.info('查看日志源')
            resp = LogSourcePage().send()
            result = resp.json()
            print(result)
            data = result['data']['logSourceList']['list'][0]  # 第一条日志源
            print(data)
            pytest.assume(
                data['logSourceName'] == 'test')  # 日志源名称
            pytest.assume(data['assetIp'] == local_ip)  # IP地址
            pytest.assume(data['normalizeGroup'] == '安全隔离与信息交换系统')  # 范化组
            pytest.assume(data['assetTypeName'] == '远程终端控制系统')  # 设备类型
        except Exception:
            raise Exception
        finally:
            self.logging.info('关闭自发现日志源')
            resp = AutoFindLogSource(flag='flase').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '关闭自发现日志源')
            self.logging.info('删除日志源')
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            resp = DeleteLogSource(ids=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('添加本机日志源')
            resp = AddLogSource(name=local_ip, ip=local_ip, normalizeGroup=["1393", "1386", "1400", "11404"]).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功，自动生成资产[{}]'.format(local_ip))

    @allure.story('日志源配置-自发现日志源')
    @allure.title('ISA-2236')
    def test_delete_auto_find_log_source_escalate_again(self):
        """
        ISA-2236 : 删除自发现的日志源后，再次上报日志
        1 将自发现的日志源A删除  删除成功
        2 日志源A对应的客户端再次上报syslog日志  日志已上报
        3 从LAA/ISA中查看日志源  产生日志源A对应的日志源，信息正确
        """
        try:
            self.logging.info('打开自发现日志源')
            resp = AutoFindLogSource(flag='true').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '开启自发现日志源')
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            self.logging.info('删除本机日志源')
            resp = DeleteLogSource(ids=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            syslog(
                '5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.100.124|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配|^1|^null|^201229008|^')
            time.sleep(5)
            self.logging.info('查看日志源')
            resp = LogSourcePage().send()
            result = resp.json()
            print(result)
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            self.logging.info('删除自发现日志源')
            resp = DeleteLogSource(ids=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            syslog(
                '5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.100.124|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配|^1|^null|^201229008|^')
            time.sleep(5)
            self.logging.info('查看日志源')
            resp = LogSourcePage().send()
            result = resp.json()
            print(result)
            data = result['data']['logSourceList']['list'][0]  # 第一条日志源
            print(data)
            pytest.assume(
                data['logSourceName'][:6] == '自发现日志源' and type(eval(data['logSourceName'][6:])) == int)  # 自发现日志源 + 数字
            pytest.assume(data['assetIp'] == local_ip)  # IP地址
            pytest.assume(data['normalizeGroup'] == '统一安全管理平台')  # 范化组
            pytest.assume(data['assetTypeName'] == '统一安全管理平台')  # 设备类型
        except Exception:
            raise Exception
        finally:
            self.logging.info('关闭自发现日志源')
            resp = AutoFindLogSource(flag='flase').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '关闭自发现日志源')
            self.logging.info('删除自发现日志源')
            id_dict = self.db.select(
                "select id from soc.soc_log_source_info where asset_ip='{}'".format(local_ip))  # 数据库查询id信息
            id = [id['id'] for id in id_dict]
            resp = DeleteLogSource(ids=id).send()
            result = resp.json()
            pytest.assume(result['message'] == '操作成功')
            self.logging.info('添加本机日志源')
            resp = AddLogSource(name=local_ip, ip=local_ip, normalizeGroup=["1393", "1386", "1400", "11404"]).send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '操作成功，自动生成资产[{}]'.format(local_ip))

    @allure.story('关联分析-单点高危事件报警')
    @allure.title('ISA-2898')
    def test_performance_metric_below_threshold(self):
        """
        ISA-2898 :当CPU、内存、磁盘没有达到阈值时，不会触发告警信息
        1 使用UdpSend.exe工具，发送日志，该日志中对应的cpu使用率信息设置为94  不会产生单点高危告警
        2 使用UdpSend.exe工具，发送日志，该日志中对应的内存使用率信息设置为94  不会产生单点高危告警
        3 使用UdpSend.exe工具，发送日志，该日志中对应的磁盘使用率信息设置为79  不会产生单点高危告警
        """
        self.logging.info('发送CPU、内存、磁盘没有达到阈值日志')
        syslog('<6>Nov 29 14:09:52 HOST;110103300117111310721344;ipv4;3; device_health: CPU使用=94；内存使用=94；磁盘使用=79；温度=0；会话数=79')
        time.sleep(40)
        self.logging.info('日志检索查看日志')
        resp = LogRetrieve().send()
        result = resp.json()
        print(result)
        pytest.assume(result['dataList'][0]['originlog'] == '<6>Nov 29 14:09:52 HOST;110103300117111310721344;ipv4;3; device_health: CPU使用=94；内存使用=94；磁盘使用=79；温度=0；会话数=79')
        self.logging.info('告警检索查看告警')
        resp = AlarmRetrieval().send()
        result = resp.json()
        print(result)
        pytest.assume(result['data']['list'][0]['alarmPrimaryMessage'] != '健康日志')

    @allure.story('关联分析-单点高危事件报警')
    @allure.title('ISA-1948')
    def test_performance_metric_over_threshold(self):
        """
        ISA-1948 :当多个事件同时触发阈值后，产生单点高危事件告警
        1 使用UdpSend.exe工具，发送日志，该日志中对应的cpu信息设置为95，内存使用率信息设置为95
        告警处理”和“告警检索”页面，该日志产生单点高危告警，告警内容和描述符合实际
        2 使用UdpSend.exe工具，发送日志，该日志中对应的内存使用率信息设置为95，磁盘使用率信息设置为80
        告警处理”和“告警检索”页面，该日志产生单点高危告警，告警内容和描述符合实际
        3 使用UdpSend.exe工具，发送日志，该日志中对应的磁盘使用率信息设置为80，cpu信息设置为95
        告警处理”和“告警检索”页面，该日志产生单点高危告警，告警内容和描述符合实际
        """
        self.logging.info('发送CPU、内存、磁盘没有达到阈值日志')
        syslog('<6>Nov 29 14:09:52 HOST;110103300117111310721344;ipv4;3; device_health: CPU使用=95；内存使用=95；磁盘使用=80；温度=0；会话数=79')
        time.sleep(40)
        self.logging.info('日志检索查看日志')
        resp = LogRetrieve().send()
        result = resp.json()
        print(result)
        pytest.assume(result['dataList'][0]['originlog'] == '<6>Nov 29 14:09:52 HOST;110103300117111310721344;ipv4;3; device_health: CPU使用=95；内存使用=95；磁盘使用=80；温度=0；会话数=79')
        self.logging.info('告警检索查看告警')
        resp = AlarmRetrieval().send()
        result = resp.json()
        print(result)
        pytest.assume(result['data']['list'][0]['alarmPrimaryMessage'] == '健康日志')
        pytest.assume(result['data']['list'][0]['alarmLevel'] == '紧急')
        pytest.assume(result['data']['list'][0]['alarmSecondaryType'] == '业务异常告警/设备故障')

@allure.feature('共有案例-系统设置')
class TestSystemSite:
    # 设置headers为admin登录信息


    logging = GetLogger.get_logger()

    # 前置处理创建数据库对象
    def setup_class(self):
        self.db = DB('database')
        header = login_test(admin, password)
        BaseApi.Authorization = header['Authorization']

    # 后置处理，断开数据库连接
    def teardown_class(self):
        self.db.close()

    @allure.story('系统设置-SNMP Trap配置')
    @allure.title('ISA-1526')
    def test_snmp_trap_must_input_isnull(self):
        """
        ISA-1526 : 【新增】新增SNMP Trap配置页面中，对服务器IP的格式及内容进行校验
        1 服务器IP输入“192.168.4.257”  输入框下方弹出提示“请输入正确的服务器ip，如127.0.0.1”
        2 服务器IP输入“0.1.1.1”  输入框下方弹出提示“请输入正确的服务器ip，如127.0.0.1”
        3 服务器IP输入“192.168.9”  输入框下方弹出提示“请输入正确的服务器ip，如127.0.0.1”
        """
        try:
            self.logging.info('新增snmp trap服务器ip为192.168.4.257')
            resp = SnmpTrapAdd(ip='192.168.4.257').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '[192.168.4.257]请输入正确的ip，如127.0.0.1')
            # self.logging.info('新增snmp trap ip为0.1.1.1')
            # resp = SnmpTrapAdd(ip='0.1.1.1').send()
            # result = resp.json()
            # print(result)
            # pytest.assume(result['message'] == '[0.1.1.1]请输入正确的ip，如127.0.0.1')
            self.logging.info('新增snmp trap ip为192.168.9')
            resp = SnmpTrapAdd(ip='192.168.9').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '[192.168.9]请输入正确的ip，如127.0.0.1')
        except Exception:
            raise Exception


    @allure.story('系统设置-SNMP Trap配置')
    @allure.title('ISA-1561')
    def test_snmp_trap_biggest_100(self):
        """
        ISA-1561 :【新增】SNMP Trap最多可配置100个服务器信息
        1 模拟构造100条不同IP的服务器信息，查看页面显示
        1.页面显示正常
        2.通过点击页面底部的分页按钮，可以查看不同页面展示的IP信息
        2 步骤一执行完后，点击“新增”
        1.提示“最多可展示100个服务器IP信息”
        备注：测试时，页面提示意思相近即可
        """
        try:
            self.logging.info('新增100条数据')
            for num in range(100):
                SnmpTrapAdd(ip=f'1.1.1.{num}').send()
                # self.db.update("INSERT INTO `soc`.`soc_snmp_trap_config` (`ip`, `port`, `community`, `version`, `status`, `type`, `protocol`, `create_time`) VALUES ('1.1.1.{}', '162', 'q', '1', '0', '1', '1', '2022-04-13 16:31:22')".format(num))
            self.logging.info('新增101条数据')
            resp = SnmpTrapAdd(ip='1.1.1.100').send()
            result = resp.json()
            print(result)
            pytest.assume(result['message'] == '最多添加100个SNMP Trap配置')
        except Exception:
            raise Exception
        finally:
            self.logging.info('删除100条数据')
            # for num in range(100):
            #     self.db.update("DELETE FROM `soc`.`soc_snmp_trap_config` WHERE  `ip`='1.1.1.{}'".format(num))
            id_dict = self.db.select("select id FROM `soc`.`soc_snmp_trap_config`")
            id = [id['id'] for id in id_dict]
            # print(id)
            resp = SnmpTrapDelete(id=id).send()
            result = resp.json()
            print(result)

    @allure.story('系统设置-SNMP Trap配置')
    @allure.title('ISA-1588')
    def test_search_server(self):
        """
        ISA-1588 :【搜索】支持根据服务器IP进行搜索
        1 创建多个不同IP的服务器信息后，在页面右上角输入框中，输入完整的服务器IP，如“192.168.4.193”，单击放大镜图标
        页面展示一条 IP地址为“192.168.4.193”的服务器信息
        2 在页面右上角输入框中，输入IP关键字，如“192.168”，单击放大镜图标
        页面展示IP中包含“192.168”的所有服务器信息
        3 在页面右上角输入框中，不输入任何IP地址，直接单击放大镜图标
        页面信息不会改变，展示已存在的所有服务器信息
        4 在页面右上角输入框中，输入错误的IP地址，如“900.200.55.222”
        页面不显示任何服务器信息
        """
        try:
            self.logging.info('===================开始=====================')
            self.logging.info('1.数据库创建多个不同IP的服务器信息后,1.1.2.10、1.1.2.15,查询1.1.2.10结果')
            resp = SnmpTrapAdd(ip='1.1.2.10').send()
            print(resp.text)
            resp = SnmpTrapAdd(ip='1.1.2.15').send()
            print(resp.text)
            # self.db.update(
            #     "INSERT INTO `soc`.`soc_snmp_trap_config` (`ip`, `port`, `community`, `version`, `status`, `type`, `protocol`, `create_time`) VALUES ('1.1.2.10', '162', 'q', '1', '0', '1', '1', '2022-04-13 16:31:22')")
            # self.db.update(
            #     "INSERT INTO `soc`.`soc_snmp_trap_config` (`ip`, `port`, `community`, `version`, `status`, `type`, `protocol`, `create_time`) VALUES ('1.1.2.15', '162', 'q', '1', '0', '1', '1', '2022-04-13 16:31:22')")
            resp = SnmpTrapQuery(ip='1.1.2.10').send()
            result = resp.json()
            if pytest.assume(result['data']['total'] == 1) and pytest.assume(result['data']['list'][0]['ip'] == '1.1.2.10'):
                self.logging.info('页面展示一条 IP地址为“1.1.2.10”的服务器信息')
            else:
                self.logging.info('步骤1结果失败')
            self.logging.info('2.在页面右上角输入框中，输入IP关键字，如“192.168”,查询结果')
            resp = SnmpTrapQuery(ip='1.1.').send()
            result = resp.json()
            if pytest.assume(result['data']['total'] == 2):
                self.logging.info('页面展示IP中包含“1.1.”的所有服务器信息')
            else:
                self.logging.info('步骤2结果失败')
            self.logging.info('3.在页面右上角不输入任何IP地址')
            resp = SnmpTrapQuery(ip='').send()
            result = resp.json()
            if pytest.assume(result['data']['total'] == 2):
                self.logging.info('页面信息不会改变，展示已存在的所有服务器信息')
            else:
                self.logging.info('步骤3结果失败')
            self.logging.info('4.输入错误的IP地址,888.888.888.88')
            resp = SnmpTrapQuery(ip='888.888.888.88').send()
            result = resp.json()
            if pytest.assume(result['data']['total'] == 0):
                self.logging.info('页面不显示任何服务器信息')
            else:
                self.logging.info('步骤4结果失败')
        except Exception:
            raise Exception
        finally:
            self.logging.info('删除1.1.2.10、1.1.2.15配置')
            # self.db.update("DELETE FROM `soc`.`soc_snmp_trap_config` WHERE  `ip`='1.1.2.10'")
            # self.db.update("DELETE FROM `soc`.`soc_snmp_trap_config` WHERE  `ip`='1.1.2.15'")
            id_dict = self.db.select("select id FROM `soc`.`soc_snmp_trap_config`")
            id = [id['id'] for id in id_dict]
            print(id)
            resp = SnmpTrapDelete(id=id).send()
            result = resp.json()
            print(result)

    @allure.story('系统设置-SNMP Trap告警发送')
    @allure.title('ISA-1580')
    def test_snmp_trap_alarm_send(self, get_header):
        """
        ISA-1580 :SNMP Trap配置后，目标服务器新增SNMP Trap协议日志源信息，可以正常接收到告警信息
        1 输入服务器IP，如：“192.168.4.196”，服务器端口“162”，SNMP版本选择“V1”, 团体字符串输入“test123”,打开状态开关，点击“确定”按钮
        备注:上述IP只是举例说明，测试时，需要输入合规的IP
        提示“操作成功”，页面新增该条服务器信息
        2 在192.168.4.196上，配置日志源信息，协议类型选择“SNMP Trap协议”，设备IP（A网）输入步骤一中的机器IP，团体字符串输入"test123",其他参数合规即可，点击“确定”按钮
        保存该日志源成功
        3 当测试机器产生新的告警信息时，立刻校验192.168.4.196中的日志检索页面信息，
        备注：告警日志是实时发送，测试机器产生告警信息时，服务端应该就能立刻收到日志信息
        1.日志检索页面产生对应的日志信息
        2.日志信息，格式如“ 1.3.6.1.2.1.11.30 =100102|^2021-11-02 10:21:29|^一般|^尝试系统调用|^XX区域|^192.168.40.135|^违反规则访问关键文件或注册表的行为”
        备注：上述的日志示例中，oid的具体值还没定，测试时候请向开发确认
        """
        try:
            self.logging.info('===================开始=====================')
            self.logging.info('1输入服务器IP，如：“192.168.4.196”，服务器端口“162”，SNMP版本选择“V1”, 团体字符串输入“test123”,打开状态开关，点击“确定”按钮')
            resp = SnmpTrapAdd(ip=IP, status=1).send()
            result = resp.json()
            print(result)
            if pytest.assume(result['message'] == '操作成功'):
                self.logging.info('提示“操作成功”，页面新增该条服务器信息')
            else:
                self.logging.info('步骤1结果失败')
            self.logging.info('2在192.168.4.196上，配置日志源信息，协议类型选择“SNMP Trap协议”，设备IP（A网）输入步骤一中的机器IP，团体字符串输入"test123",其他参数合规即可')
            # id_dict = self.db.select("select id FROM `soc`.`soc_log_source_info` WHERE  `asset_ip`='{}'".format(local_ip))  # 获取本机日志源id
            # id= id_dict[0]['id']
            # header = login_test(name=username, pwd=password)
            add = AddLogSource(name=IP, ip=IP, protocolType=5, community='test', normalizeGroup=["1393", "1386", "1400","11404"], ftpMode=1)
            add.headers = get_header[1]
            resp = add.send()  # 修改日志源信息
            result = resp.json()
            print(result)
            time.sleep(2)
            if pytest.assume('操作成功' in result['message']):
                self.logging.info('保存该日志源成功')
            else:
                self.logging.info('步骤2结果失败')
            self.logging.info('3 当测试机器产生新的告警信息时，立刻校验192.168.4.196中的日志检索页面信息')
            # syslog('5|^5B3E862B81FE41DF9AECB98210512D99|^|^重要|^1|^未处理|^null|^null|^2021-06-03 16:00:59.0|^2021-06-03 16:00:59.0|^Firewall201229008|^192.168.100.124|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配|^1|^null|^201229008|^')  #  发送日志
            syslog('<5>DEVIP=192.168.1.137 Type=FileSync TIME=2020-03-10 11:56:09 TASKID=0 SPATH=//192.168.2.2/share1 FILENAME=  RESULT=失败 REMARK=挂载失败 ISOUIT=0')  #  发送日志
            time.sleep(60)
            #   查看告警检索产生告警
            alarm = AlarmRetrieval()
            alarm.headers = get_header[1]
            resp = alarm.send()
            result = resp.json()
            print(result)
            # test1 = pytest.assume(result['data']['list'][0]['alarmPrimaryMessage'] == 'MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配' and result['data']['list'][0]['alarmLevel'] == '重要')
            test1 = pytest.assume(result['data']['list'][0]['alarmPrimaryMessage'] == '安全隔离与信息交换系统-文件交换日志' and result['data']['list'][0]['alarmLevel'] == '重要')
            #   查看日志检索产生日志
            log = LogRetrieve()
            log.headers = get_header[1]
            resp = log.send()
            result = resp.json()
            print(result)
            log1 = result['dataList'][0]['originlog']
            log1_header, log1_tail = log1.split('|')[0], log1.split('|')[2:]
            print(log1_header, log1_tail)
            log2 = result['dataList'][1]['originlog']
            log2_header, log2_tail = log2.split('|')[0], log2.split('|')[2:]
            print(log2_header, log2_tail)
            result1 = log1_header == '1.3.6.1.4.1.51011.3.100102 = 100102' and log1_tail == ['^重要', '^文件保护异常', '^XX区域', '^', '^安全隔离与信息交换系统-文件交换日志']
            result2 = log2_header == '1.3.6.1.4.1.51011.3.100102 = 100102' and log2_tail == ['^重要', '^文件保护异常', '^XX区域', '^', '^安全隔离与信息交换系统-文件交换日志']
            # test2 = pytest.assume(result['dataList'][0]['originlog'] == '1.3.6.1.4.1.51011.3.100102 = 100102|^2022-04-15 16:56:48|^重要|^地址欺诈|^XX区域|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配'or result['dataList'][1]['originlog'] == '1.3.6.1.4.1.51011.3.100102 = 100102|^2022-04-15 16:56:48|^重要|^地址欺诈|^XX区域|^192.168.100.123|^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配')
            # test2 = pytest.assume(log1_header == '1.3.6.1.4.1.51011.3.100102 = 100102' and log1_tail == ['^重要', '^地址欺诈', '^XX区域', '^192.168.100.123', '^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配'] or log2_header == '1.3.6.1.4.1.51011.3.100102 = 100102' and log2_tail == ['^重要', '^地址欺诈', '^XX区域', '^192.168.100.123', '^MAC：d0:37:45:1e:8e:07与 IP：192.168.100.123不匹配'])
            test2 = pytest.assume(result1 or result2)
            if test1 and test2:
                self.logging.info('1.日志检索页面产生对应的日志信息 2.日志信息，格式如“ 1.3.6.1.2.1.11.30 =100102|^2021-11-02 10:21:29|^一般|^尝试系统调用|^XX区域|^192.168.40.135|^违反规则访问关键文件或注册表的行为”')
            else:
                self.logging.info('步骤3结果失败')
        except Exception:
            raise Exception
        finally:
            pass
            self.logging.info('数据库删除服务器配置')
            id_dict = self.db.select("select id FROM `soc`.`soc_snmp_trap_config` WHERE ip='{}'".format(IP))
            id = [id['id'] for id in id_dict]
            resp = SnmpTrapDelete(id=id).send()
            result = resp.json()
            print(result)
            # self.db.update("DELETE FROM `soc`.`soc_snmp_trap_config` WHERE ip='{}'".format(IP))   # 删除snmp配置
            self.db.update("DELETE FROM `soc`.`soc_log_source_info` WHERE asset_ip='{}'".format(IP))  # 删除日志源

    @allure.story('系统设置-用户管理-启用禁用账号')
    @allure.title('ISA-1593')
    def test_disable_enable_user(self, get_header):
        """
        ISA-1593 : 禁用/启用用户操作日志
        1 用admin权限账户启用/禁用系统用户
        操作成功
        2 用audit权限用户登录系统，查看操作日志
        启用和禁用系统用户，均会有操作日志，格式为：启用xxx账号；禁用xxx账号。
        """
        self.logging.info('===================开始=====================')
        self.logging.info('1用admin权限账户启用/禁用系统用户')
        user_id_dict = self.db.select("select user_id from soc.soc_user_info where user_name='tym'")
        user_id = user_id_dict[0]['user_id']
        resp = DisableEnableUser(id=user_id).send()  # 禁用tym
        result = resp.json()
        print(result)
        test1 =pytest.assume(result['message'] == '禁用成功')
        resp = DisableEnableUser(id=user_id).send()  # 启用tym
        result = resp.json()
        print(result)
        test2 = pytest.assume(result['message'] == '启用成功')
        if test1 and test2:
            self.logging.info('操作成功')
        else:
            self.logging.info('步骤1结果失败')
        self.logging.info('2用audit权限用户登录系统，查看操作日志')
        time.sleep(2)
        log = OperatorLog()  # 查看操作日志
        log.headers = get_header[2]
        resp = log.send()
        result = resp.json()
        print(result)
        test3 = pytest.assume(result['data']['list'][0]['context'] == '启用用户[tym]成功')
        test4 = pytest.assume(result['data']['list'][1]['context'] == '禁用用户[tym]成功')
        if test3 and test4:
            self.logging.info('启用和禁用系统用户，均会有操作日志，格式为：启用xxx账号；禁用xxx账号。')
        else:
            self.logging.info('步骤2结果失败')

    @allure.story('系统设置-iec104配置')
    @allure.title('ISA-1884')
    def test_iec_104_produce_operator_log(self, get_header):
        """
        ISA-1884 : 配置iec104服务后，可以正常产生系统操作日志
        1
        1.端口号输入默认值2404
        2.客户端Ip输入iec104客户端所在的Ip
        3.最大连接数设置为5
        4.“转态”按钮打开
        5.点击"保存"按钮
        1.页面提示“操作成功”
        2.audit账户下有对应的操作日志生成
        """
        self.logging.info('===================开始=====================')
        self.logging.info('1.端口号输入默认值2404 2.客户端Ip输入iec104客户端所在的Ip 3.最大连接数设置为5 4.“转态”按钮打开5.点击"保存"按钮')
        resp = Iec104Edit(ip='192.168.1.1').send()
        result = resp.json()
        print(result)
        test1 = pytest.assume(result['message'] == '操作成功')
        time.sleep(2)
        log = OperatorLog()  # 查看操作日志
        log.headers = get_header[2]
        resp = log.send()
        result = resp.json()
        print(result)
        test2 = pytest.assume(result['data']['list'][0]['context'] == '开启IEC104服务端，端口为[2404]，IP范围[192.168.1.1]，最大连接数[5]成功')
        if test1 and test2:
            self.logging.info('1.页面提示“操作成功” 2.audit账户下有对应的操作日志生成')
        else:
            self.logging.info('结果失败')

    @allure.story('系统设置-数据备份')
    @allure.title('ISA-1769')
    def test_backup_policy_config(self):
        """
        ISA-1769 : 只备份策略数据，备份列表备份数据字段显示策略数据
        1 “公共参数配置”勾选策略数据,其他项正确填写,点击保存
        公共参数保存成功
        2点击全量备份，备份成功之后查看列表备份数据字段
        备份数据显示策略数据
        3 登录服务器目录/usr/local/soc/elasticsearch-5.5.0/data/backup 查看备份数据
        mysql下有最新备份的数据,es下没有最新备份的数据
        """
        with allure.step('1公共参数配置”勾选策略数据,其他项正确填写,点击保存'):
            resp = DataBackupSave().send()  # 保存数据备份
            result = resp.json()
            with allure.step('公共参数保存成功'):
                assert result['message'] == '操作成功'
        with allure.step('2点击全量备份，备份成功之后查看列表备份数据字段'):
            resp = FullBackup().send()  # 全量备份
            result = resp.json()
            time_str = datetime.datetime.now()
            assert result['message'] == '后台开始执行数据备份'
            time.sleep(60)
            with allure.step('备份数据显示策略数据'):
                resp = BackupQuery().send()
                result = resp.json()
                time_now = time_str.strftime('%Y%m%d%H')
                task_name = result['data']['list'][0]['taskName']  # 备份名称
                assert f'backup_{time_now}' in result['data']['list'][0]['taskName'] and result['data']['list'][0]['backupMode'] == 'manual' and result['data']['list'][0]['backupType'] =='all' and result['data']['list'][0]['dataType'] == 'mysql'
        with allure.step('3 登录服务器目录/usr/local/soc/elasticsearch-5.5.0/data/backup 查看备份数据'):
            linux = Linux()
            linux.remoteConnect(IP, linux_port, linux_user, linux_pass)
            sql_result = linux.exec_command('ls /usr/local/soc/elasticsearch-5.5.0/data/backup/local/mysql')  #查看 /usr/local/soc/elasticsearch-5.5.0/data/backup/local/mysql
            print(sql_result)
            task_name = task_name.split('_')[1]
            print(task_name, sql_result[0][:-1])
            es_result = linux.exec_command('ls /usr/local/soc/elasticsearch-5.5.0/data/backup/local/es')  #查看 /usr/local/soc/elasticsearch-5.5.0/data/backup/local/es
            print(es_result)
            with allure.step('mysql下有最新备份的数据,es下没有最新备份的数据'):
                assert f'mysql_{task_name}.sql' == sql_result[-1][:-1]
                if es_result != '':
                    assert f'mysql_{task_name}.sql' != es_result[-1][:-1]

    @allure.story('系统设置-数据备份')
    @allure.title('ISA-1770')
    def test_backup_log_config(self):
        """
        ISA-1770 : 只备份日志数据，备份列表备份数据字段显示日志数据
        1 “公共参数配置”勾选日志数据,其他项正确填写,点击保存
        公共参数保存成功
        2点击全量备份，备份成功之后查看列表备份数据字段
        备份数据显示策略数据
        3 登录服务器目录/usr/local/soc/elasticsearch-5.5.0/data/backup 查看备份数据
        es下有最新备份的数据,mysql下没有最新备份的数据
        """
        with allure.step('1公共参数配置”勾选日志数据,其他项正确填写,点击保存'):
            resp = DataBackupSave(dataType='es').send()  # 保存数据备份
            result = resp.json()
            with allure.step('公共参数保存成功'):
                assert result['message'] == '操作成功'
        with allure.step('2点击全量备份，备份成功之后查看列表备份数据字段'):
            resp = FullBackup().send()  # 全量备份
            result = resp.json()
            time_str = datetime.datetime.now()
            assert result['message'] == '后台开始执行数据备份'
            time.sleep(60)
            with allure.step('备份数据显示日志数据'):
                resp = BackupQuery().send()
                result = resp.json()
                time_now = time_str.strftime('%Y%m%d%H')
                snapshotRepoName = result['data']['list'][0]['snapshotRepoName']  # 备份仓库名称
                assert f'backup_{time_now}' in result['data']['list'][0]['taskName'] and result['data']['list'][0]['backupMode'] == 'manual' and result['data']['list'][0]['backupType'] =='all' and result['data']['list'][0]['dataType'] == 'es'
        with allure.step('3 登录服务器目录/usr/local/soc/elasticsearch-5.5.0/data/backup 查看备份数据'):
            linux = Linux()
            linux.remoteConnect(IP, linux_port, linux_user, linux_pass)
            sql_result = linux.exec_command('ls /usr/local/soc/elasticsearch-5.5.0/data/backup/local/mysql')  #查看 /usr/local/soc/elasticsearch-5.5.0/data/backup/local/mysql
            print(sql_result)
            es_result = linux.exec_command('ls /usr/local/soc/elasticsearch-5.5.0/data/backup/local/es')  #查看 /usr/local/soc/elasticsearch-5.5.0/data/backup/local/es
            print(es_result)
            with allure.step('es下有最新备份的数据,mysql下没有最新备份的数据'):
                if sql_result != '':
                    assert snapshotRepoName != sql_result[-1][:-1]
                assert snapshotRepoName == es_result[-1][:-1]

    @allure.story('系统设置-数据备份')
    @allure.title('ISA-1624')
    def test_backup_all_log_config(self):
        """
        ISA-1624 : 备份策略数据和日志数据，备份列表备份数据字段显示策略数据和日志数据
        1 “公共参数配置”勾选策略数据和日志数据,其他项正确填写,点击保存
        公共参数保存成功
        2 点击全量备份，备份成功之后查看列表备份数据字段
        备份数据显示策略数据和日志数据
        3 登录服务器目录/usr/local/soc/elasticsearch-5.5.0/data/backup 查看备份数据
        mysql和es目录下存在当前备份数据
        """
        with allure.step('1“公共参数配置”勾选策略数据和日志数据,其他项正确填写,点击保存'):
            resp = DataBackupSave(dataType='mysql,es').send()  # 保存数据备份
            result = resp.json()
            with allure.step('公共参数保存成功'):
                assert result['message'] == '操作成功'
        with allure.step('2点击全量备份，备份成功之后查看列表备份数据字段'):
            resp = FullBackup().send()  # 全量备份
            result = resp.json()
            print(result)
            time_str = datetime.datetime.now()
            assert result['message'] == '后台开始执行数据备份'
            time.sleep(60)
            with allure.step('备份数据显示日志数据'):
                resp = BackupQuery().send()
                result = resp.json()
                print(result)
                time_now = time_str.strftime('%Y%m%d%H')
                task_name = result['data']['list'][0]['taskName']  # 备份名称
                snapshotRepoName = result['data']['list'][0]['snapshotRepoName']  # 备份仓库名称
                assert f'backup_{time_now}' in result['data']['list'][0]['taskName'] and result['data']['list'][0][
                    'backupMode'] == 'manual' and result['data']['list'][0]['backupType'] == 'all' and \
                       result['data']['list'][0]['dataType'] == 'mysql,es'
        with allure.step('3 登录服务器目录/usr/local/soc/elasticsearch-5.5.0/data/backup 查看备份数据'):
            linux = Linux()
            linux.remoteConnect(IP, linux_port, linux_user, linux_pass)
            sql_result = linux.exec_command(
                'ls /usr/local/soc/elasticsearch-5.5.0/data/backup/local/mysql')  # 查看 /usr/local/soc/elasticsearch-5.5.0/data/backup/local/mysql
            print(sql_result)
            task_name = task_name.split('_')[1]
            print(task_name, sql_result[-1][:-1])
            es_result = linux.exec_command(
                'ls /usr/local/soc/elasticsearch-5.5.0/data/backup/local/es')  # 查看 /usr/local/soc/elasticsearch-5.5.0/data/backup/local/es
            print(es_result)
            with allure.step('mysql和es目录下存在当前备份数据'):
                assert f'mysql_{task_name}'[:-4] in sql_result[-1][:-1]
                assert snapshotRepoName == es_result[-1][:-1]

    # todo 增加   2193
    @allure.story('系统设置-syslog配置-发送syslog加密')
    @allure.title('ISA-2193')
    def test_symmetric_encryption(self, get_header):
        """
        ISA-2193 : syslog传输过程，修改是否加密，两端不对称后接收到的syslog为乱码
        1 编辑日志审计syslog发送配置，修改为加密  态势感知接收到的syslog日志为乱码
        2 日志审计为不加密，态势感知日志源配置为加密  态势感知接收到的syslog日志为乱码
        3 日志审计和态势感知都配置为加密，密钥相同  态势感知接收到的syslog正常，解析正确
        """
        try:
            with allure.step('1 编辑日志审计syslog发送配置，修改为加密'):
                #  发送加密的数据
                syslog(
                    '181CFE736298F1DECB9B6976A5CF08C00B427A4BFC44E75695FF1CEE6630799DDF2F84D8CCDA9D1DFAEB88288C021F4663C1E7796B896D48C7C933C21389E1E17B2A0672AE6313AE9A2422CDA45D752C1BCA36250BBC011BCB3F1B2CD089B4262C7C0BA8D3310AA1F74498035A3F88EE9558845BAB704E4DC3F77A3E5C068BE167FB343D70723F3127B91C77BDB9BF561BA34B74A83F37B3310862CB16ADAB257096F253244C59601A660771A5C590C4FE1EE5E6FCFAEE80CDF243F37C77050AB5601A7AF22EFBD5AD8F080DCE61845FCA1495CA69FD58AF8576A32E23D7B6F2817C47DE09F7563701FA7ABC26B0D12D7F91BBC51B527A6D584F24EDA7EB8FBD4E7931CC7F81C3781598301E4A18C529F574F8E5B4F2D5022F1416530BA3FF51531DD6D59331D578C00EB1F0DF9C3BDCD9F7E3D03DDB018DB3BB3EFBE7AB37B5715112641D3A907F46197930D67B624A')
                time.sleep(40)
                # 日志检索，查看第一条数据
                log = LogRetrieve()
                log.headers = get_header[1]
                resp = log.send()
                result = resp.json()
                print(result)
                data = result['dataList'][0]['originlog']
                # after_total = result['total']
                with allure.step('态势感知接收到的syslog日志为乱码'):
                    # 判断第一条日志
                    assert data == '181CFE736298F1DECB9B6976A5CF08C00B427A4BFC44E75695FF1CEE6630799DDF2F84D8CCDA9D1DFAEB88288C021F4663C1E7796B896D48C7C933C21389E1E17B2A0672AE6313AE9A2422CDA45D752C1BCA36250BBC011BCB3F1B2CD089B4262C7C0BA8D3310AA1F74498035A3F88EE9558845BAB704E4DC3F77A3E5C068BE167FB343D70723F3127B91C77BDB9BF561BA34B74A83F37B3310862CB16ADAB257096F253244C59601A660771A5C590C4FE1EE5E6FCFAEE80CDF243F37C77050AB5601A7AF22EFBD5AD8F080DCE61845FCA1495CA69FD58AF8576A32E23D7B6F2817C47DE09F7563701FA7ABC26B0D12D7F91BBC51B527A6D584F24EDA7EB8FBD4E7931CC7F81C3781598301E4A18C529F574F8E5B4F2D5022F1416530BA3FF51531DD6D59331D578C00EB1F0DF9C3BDCD9F7E3D03DDB018DB3BB3EFBE7AB37B5715112641D3A907F46197930D67B624A'
            with allure.step('2 日志审计为不加密，态势感知日志源配置为加密'):
                source = LogSourcePage()
                source.headers = get_header[1]
                resp = source.send()
                result = resp.json()
                print(result)
                id = result['data']['logSourceList']['list'][0]['id']
                assetIp = result['data']['logSourceList']['list'][0]['assetIp']  # 日志源ip
                # 修改日志源，配置日志源加密
                mod = ModLogSource()
                mod.headers = get_header[1]
                mod.json = {"logSourceName": assetIp, "assetIp": assetIp, "factory": 3, "assetType": 101001, "port": '',
                            "protocolType": 1, "snmpVersion": '', "normalizeGroup": ["1393", "1386", "1400", "11404"],
                            "community": '',
                            "isAnonymousLogin": 0, "userName": '', "password": '', "filePath": '',
                            "originalEncoding": '',
                            "downloadRate": '', "taskInterval": '', "ftpMode": '', "dbType": '', "dbName": '',
                            "customerSqlStatus": 0, "dbTableName": '', "selectSql": '', "isEncryption": 1,
                            "algorithm": 1,
                            "privateKey": 'Admin@1234567890', "id": id}
                resp = mod.send()
                result = resp.json()
                print(result)
                time.sleep(1)
                # 日志检索，查看第一条数据
                resp = log.send()
                result = resp.json()
                before_total = result['total']
                #  发送加密的数据
                syslog(
                    '31|^CA0135050A9E439D825C907C88AEFDA2|^|^2|^1|^0|^|^|^2021-06-03 15:47:00|^2021-06-03 15:47:00|^WIN-PP4LSTF6N3H|^192.168.100.30|^2|^192.168.100.11|^192.168.100.21|^9959|^445|^TCP|^1|^')
                time.sleep(40)
                with allure.step('态势感知接收到的syslog日志为乱码'):
                    # 日志检索，查看第一条数据
                    resp = log.send()
                    result = resp.json()
                    print(result)
                    data = result['dataList'][0]['originlog']
                    after_total = result['total']
                    # 判断第一条日志
                    assert data == '31|^CA0135050A9E439D825C907C88AEFDA2|^|^2|^1|^0|^|^|^2021-06-03 15:47:00|^2021-06-03 15:47:00|^WIN-PP4LSTF6N3H|^192.168.100.30|^2|^192.168.100.11|^192.168.100.21|^9959|^445|^TCP|^1|^'
                    assert result['dataList'][0]['eventlevel'] == '一般'
                    assert int(after_total) - int(before_total) == 1  # 判断新增一条数据
            with allure.step('3 日志审计和态势感知都配置为加密，密钥相同'):
                # resp = LogSourcePage().send()
                # result = resp.json()
                # print(result)
                # id = result['data']['logSourceList']['list'][0]['id']
                # assetIp = result['data']['logSourceList']['list'][0]['assetIp']  # 日志源ip
                # # 修改日志源，配置日志源加密
                # mod = ModLogSource()
                # mod.json = {"logSourceName": assetIp, "assetIp": assetIp, "factory": 3, "assetType": 101001, "port": '',
                #             "protocolType": 1, "snmpVersion": '', "normalizeGroup": ["1393", "1386", "1400", "11404"],
                #             "community": '',
                #             "isAnonymousLogin": 0, "userName": '', "password": '', "filePath": '', "originalEncoding": '',
                #             "downloadRate": '', "taskInterval": '', "ftpMode": '', "dbType": '', "dbName": '',
                #             "customerSqlStatus": 0, "dbTableName": '', "selectSql": '', "isEncryption": 1, "algorithm": 1,
                #             "privateKey": 'Admin@1234567890', "id": id}
                # resp = mod.send()
                # result = resp.json()
                # print(result)
                # time.sleep(1)
                # 日志检索，查看第一条数据
                resp = log.send()
                result = resp.json()
                before_total = result['total']
                #  发送加密的数据
                syslog(
                    '181CFE736298F1DECB9B6976A5CF08C00B427A4BFC44E75695FF1CEE6630799DDF2F84D8CCDA9D1DFAEB88288C021F4663C1E7796B896D48C7C933C21389E1E17B2A0672AE6313AE9A2422CDA45D752C1BCA36250BBC011BCB3F1B2CD089B4262C7C0BA8D3310AA1F74498035A3F88EE9558845BAB704E4DC3F77A3E5C068BE167FB343D70723F3127B91C77BDB9BF561BA34B74A83F37B3310862CB16ADAB257096F253244C59601A660771A5C590C4FE1EE5E6FCFAEE80CDF243F37C77050AB5601A7AF22EFBD5AD8F080DCE61845FCA1495CA69FD58AF8576A32E23D7B6F2817C47DE09F7563701FA7ABC26B0D12D7F91BBC51B527A6D584F24EDA7EB8FBD4E7931CC7F81C3781598301E4A18C529F574F8E5B4F2D5022F1416530BA3FF51531DD6D59331D578C00EB1F0DF9C3BDCD9F7E3D03DDB018DB3BB3EFBE7AB37B5715112641D3A907F46197930D67B624A')
                time.sleep(40)
                with allure.step('态势感知接收到的syslog正常，解析正确'):
                    # 日志检索，查看第一条数据
                    resp = log.send()
                    result = resp.json()
                    data = result['dataList'][0]['originlog']
                    after_total = result['total']
                    # 判断第一条日志
                    assert data == '12|^01B00E3B18D44C108DFFA43DB497E058_e9ddf443-553f-483a-ad5f-7b9b7ccf5904|^201229008|^192.168.100.124|^Probe201229008|^2021-06-03 16:28:37|^17|^192.168.100.123|^|^64766|^224.0.0.252|^|^5355|^d0:37:45:1e:8e:07|^01:00:5e:00:00:fc|^2021-12-27 16:26:20|^2021-12-27 16:26:20|^3|^2|^0|^132|^0|^01B00E3B18D44C108DFFA43DB497E058|^17|^'
                    assert result['dataList'][0]['eventlevel'] == '一般'
                    assert int(after_total) - int(before_total) == 1  # 判断新增一条数据
        except Exception as e:
            raise e
        finally:
            # 修改日志源，取消日志源加密
            mod = ModLogSource()
            mod.headers = get_header[1]
            mod.json = {"logSourceName": assetIp, "assetIp": assetIp, "factory": 3, "assetType": 101001,
                        "port": '', "protocolType": 1, "snmpVersion": '', "normalizeGroup": [1386, 1393, 1400, 11404],
                        "community": '', "isAnonymousLogin": 0, "userName": '', "password": '', "filePath": '',
                        "originalEncoding": '', "downloadRate": '', "taskInterval": '', "ftpMode": '', "dbType": '',
                        "dbName": '', "customerSqlStatus": 0, "dbTableName": '', "selectSql": '', "isEncryption": 0,
                        "algorithm": 1, "privateKey": "", "id": id}
            resp = mod.send()
            result = resp.json()
            print(result)
