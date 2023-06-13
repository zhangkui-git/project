import time

import requests
# import pytest
# import allure
from zk_dev1.test_imp.common_soms_tool.logger import GetLog
# from zk_dev1.test_imp.common_soms_tool.s_mysql import *
# from zk_dev1.test_imp.common_soms_tool.encry_decry import *
from zk_dev1.test_imp.client_soms_api.soms_api import *
write_log = GetLog().get_log()


class Soms_test_smoke(BaseApi):
    def __init__(self):
        BaseApi.__init__(self)

    def start(self):
        Soms_Login('admin_zk1', 'Admin@123').send()
        Soms_AddUser().send()
        Soms_DelUser().send()


if __name__ == '__main__':
    Soms_test_smoke().start()












def user_login():   # 登录
    url = f"{host}/login/userLogin"
    headers = {"Content-Type": "application/json"}
    body = {"userName": f"{user}", "userPassword": f"{pas}"}
    # body = {'userName': 'hLCCDHQsDnMJrY27wg81WTFCA47LrpypWjy5Kvw8t1t2vnO2XOlsWb0V1Mp8WeTzvUwEAeH39BbA/9q+XAbYfvd9SCjbDW8H9krRqD/wegYz6o0lVuodqkjOFik7flmcdimYq1gjR/ftrCqPGjgeIbRDv6DdJWiyUtGRmYYMFjlu9oN0huJcXbodDawHea1IOmQd6tCI8Po1VhzHsnhJBXqbIMdwE3traRGaTku+Uaa/KM8Fjg3q7Do6Js0B6eoecvvg0ogOdd459NF5eXU3qipNUhsxI6e3NuUWH9h26z4uB7kJbKreCJ9Aua2iS09mDTwAHODz9p3yO1YkoXyInw==', 'userPassword': 'O1tHGqbKK0Zw7Od63xE9CHWSAguF6to8JA97m1w+jdApBfAX06MZDJt/pyJjOhpjrl1taimLItgaln+ebEwUc0yPojhM2aavnLnoExWUTG4GDdW0+T4sPNpCby2ijTlaBHyK0amd3M6hleDeSs5X7bwD97V47vz4IOuQQj5DS9G2bFPmPkxd7t1P7wEbHzrQJIGxIxk+MGNRsshLG1Fn2ZZbY2kW9jHxl7e2ypiA6E5YTotZ7EPWd6DDvdU49WvOT/48jFww3nj/aGbAM2ctWLNQDxiKkSMN+uXthoflAv0WDUyS6JQTsaaOwuxeDI8ASv/aPRaiuR+CGsrSfdilkA=='}
    res = requests.post(url=url, headers=headers, json=body, verify=False)
    a = []
    a.append(res.json()['statusCode'])
    a.append(res.json()['message'])
    write_log.info(f"登录成功1：{a}")
    # print(a, res.json()['data']['accessToken'])
    return a, res.json()['data']['accessToken']


@allure.feature('冒烟测试')
class Test_isav2r7():

    # @allure.epic('登录页面')
    # @allure.feature('登录功能')
    # @allure.severity("normal")
    # @allure.description('用例描述信息:  登录页面功能验证')
    @allure.story('ISA-3119: 登录功能')
    def test_login(self):
        """
        ISA-3119 : 【已确认资产】新增字段信息为添加资产时填写的信息
        1 点击新增资产	弹出新增资产弹窗
        2 手动输入归属单位，归属专业，归属系统，主机名，物理端口编号，注册时间，资产业务价值，资产机密性，资产完整性，资产可用性、安全责任人 输入其他必填项并保存 查看新增资产信息	列表中： 归属单位，归属专业，归属系统，主机名，物理端口编号，注册时间，资产业务价值，资产机密性，资产完整性，资产可用性，安全责任人 显示为新增资产时手动填写的信息
        """
        write_log.info(f"登录结果返回2：{user_login()[0]}")
        assert user_login()[0] == [200, '操作成功']


    # @allure.epic('日志采集')
    # @allure.feature('日志源管理-列表上方-新增')
    @allure.story('ISA-3120：日志源管理-列表上方-新增')
    # @allure.severity("normal")
    # @allure.description('用例描述信息:  新增日志源')
    def test_log_source_add(self):   # 添加日志源
        token = user_login()[1]
        log_source_add_url = f"{host}/log/source/add"
        write_log.info(f"登陆成功，日志源管理-列表上方-新增的url是：{log_source_add_url}")
        log_source_add_headers = {"Content-Type": "application/json;charset=UTF-8",
                        "Authorization": f'{token}'}
        log_source_add_body = {"logSourceName":"testzk2","assetIp":"192.168.92.128","assetType":1,"factory":3,"port":"","protocolType":1,"snmpVersion":1,"normalizeGroup":[1399],"community":"","isAnonymousLogin":0,"userName":"","password":"","filePath":"","originalEncoding":"UTF-8","downloadRate":1000,"taskInterval":300,"ftpMode":1,"dbType":"MySQL","dbName":"","customerSqlStatus":0,"dbTableName":"","selectSql":"","logType":[]}
        res = requests.post(log_source_add_url, headers=log_source_add_headers, json=log_source_add_body, verify=False)
        b = []
        b.append(res.json()['statusCode'])
        b.append(res.json()['message'])
        write_log.info(f'添加日志源返回：{res.json()}')
        assert b == [200, '操作成功']


    # @allure.epic('日志采集')
    # @allure.feature('日志源管理-列表上方-删除')
    @allure.story('ISA-3121：日志源管理-列表上方-删除')
    # @allure.severity("normal")
    # @allure.description('用例描述信息:  删除日志源')
    def test_log_source_del(self):   # 删除日志源
        token = user_login()[1]
        log_source_del_url = f"{host}/log/source/delete/batch"
        write_log.info(f"登陆成功，日志源管理-列表上方-删除的url是：{log_source_del_url}")
        log_source_del_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
        # ids = input("请输入ids---:")
        sql1 = "select id from soc_log_source_info slsi where log_source_name = 'testzk2'"
        ids = select(sql1)[0]['id']
        log_source_del_body = {"ids": [f'{ids}']}
        res = requests.delete(log_source_del_url, headers=log_source_del_headers, json=log_source_del_body, verify=False)
        c = []
        c.append(res.json()['statusCode'])
        c.append(res.json()['message'])
        write_log.info(f"删除日志源返回：{res.json()}")
        assert c == [200, '操作成功']

    @allure.story('ISA-3122：策略配置-范化-复制新策略')
    def test_up_add(self):
        token = user_login()[1]
        print(token, 111111)
        up_add_url = f"{host}/normalize/copy"
        write_log.info(f"登陆成功，策略配置-范化-复制新策略url是：{up_add_url}")
        up_add_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
        up_add_body = {"ruleName":"配置变更日志-副本11111","ruleId":"62d691c37794295966c3571b"}
        res = requests.post(up_add_url, headers=up_add_headers, json=up_add_body, verify=False)
        c = []
        c.append(res.json()['statusCode'])
        c.append(res.json()['message'])
        write_log.info(f"复制范化规则返回：{res.json()}")
        assert c == [200, '操作成功']


    # @allure.epic('策略配置')
    # @allure.feature('范化-列表上方删除功能')
    # @allure.severity("normal")
    # @allure.description('用例描述信息: 策略配置-范化-列表上方删除功能')
    @allure.story('ISA-3123：策略配置-范化-列表上方删除功能')
    def test_up_del(self):
        token = user_login()[1]
        up_del_url = f"{host}/normalize/delete/batch"
        write_log.info(f"登陆成功，范化-列表上方删除功能的url是：{up_del_url}")
        up_del_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
        sql2 = "select rule_id from soc_normalize_info slsi where rule_name = '配置变更日志-副本11111'"
        ids = select(sql2)[0]['rule_id']
        up_del_body = {'ids': [f'{ids}']}
        res = requests.delete(up_del_url, headers=up_del_headers, json=up_del_body, verify=False)
        d = []
        d.append(res.json()['statusCode'])
        d.append(res.json()['message'])
        write_log.info(f"返回结果---：{res.json()}")
        pytest.assume(d[0] == 2100)
        pytest.assume(d[1] == '1条数据删除成功！')
        # assert d == [200, '1条数据删除成功！']




