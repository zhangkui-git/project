import requests
import pytest
import allure
from zk_dev1.dev_imp.common_tool.common_conf import common_url, username, password
from zk_dev1.dev_imp.common_tool.logger import GetLog


write_log = GetLog().get_log()


def user_login():   # 登录
    url = f"{common_url}/login/userLogin"
    headers = {"Content-Type": "application/json"}
    body = {"userName": f"{username}", "userPassword": f"{password}"}
    res = requests.post(url=url, headers=headers, json=body, verify=False)
    a = []
    a.append(res.json()['statusCode'])
    a.append(res.json()['message'])
    write_log.info(f"登录成功1：{a}")
    return a, res.json()['data']['accessToken']


@pytest.fixture(scope="session")
def if1no1():
    a = [200, '操作成功']
    return a


@allure.epic('登录页面')
@allure.feature('登录功能')
# @allure.story('')
@allure.severity("normal")
@allure.description('用例描述信息:  登录页面功能验证')
def test_login(if1no1):
    write_log.info(f"登录结果返回2：{user_login()[0]}")
    assert user_login()[0] == if1no1


@pytest.fixture(scope='session')
def if3no1():
    a = [200, '操作成功']
    return a


@allure.epic('日志采集')
@allure.feature('日志源管理-列表上方-新增')
# @allure.story('列表上方-新增')
@allure.severity("normal")
@allure.description('用例描述信息:  新增日志源')

def test_log_source_add(if3no1):   # 添加日志源
    token = user_login()[1]
    log_source_add_url = f"{common_url}/log/source/add"
    write_log.info(f"登陆成功，日志源管理-列表上方-新增的url是：{log_source_add_url}")
    log_source_add_headers = {"Content-Type": "application/json;charset=UTF-8",
                    "Authorization": f'{token}'}
    log_source_add_body = {"logSourceName":"testzk2","assetIp":"192.168.92.128","assetType":1,"factory":3,"port":"","protocolType":1,"snmpVersion":1,"normalizeGroup":[1399],"community":"","isAnonymousLogin":0,"userName":"","password":"","filePath":"","originalEncoding":"UTF-8","downloadRate":1000,"taskInterval":300,"ftpMode":1,"dbType":"MySQL","dbName":"","customerSqlStatus":0,"dbTableName":"","selectSql":"","logType":[]}
    res = requests.post(log_source_add_url, headers=log_source_add_headers, json=log_source_add_body, verify=False)
    b = []
    b.append(res.json()['statusCode'])
    b.append(res.json()['message'])
    write_log.info(f'添加日志源返回：{res.json()}')
    assert b == if3no1


@pytest.fixture(scope='session')
def if3no2():
    a = [200, '操作成功']
    return a


@allure.epic('日志采集')
@allure.feature('日志源管理-列表上方-删除')
# @allure.story('列表上方-删除')
@allure.severity("normal")
@allure.description('用例描述信息:  删除日志源')
def test_log_source_del(if3no2):   # 删除日志源
    token = user_login()[1]
    log_source_del_url = f"{common_url}/log/source/delete/batch"
    write_log.info(f"登陆成功，日志源管理-列表上方-删除的url是：{log_source_del_url}")
    log_source_del_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    ids = input("请输入ids---:")
    log_source_del_body = {"ids": [f'{ids}']}
    res = requests.delete(log_source_del_url, headers=log_source_del_headers, json=log_source_del_body, verify=False)
    c = []
    c.append(res.json()['statusCode'])
    c.append(res.json()['message'])
    write_log.info(f"删除日志源返回：{res.json()}")
    assert c == if3no2


@pytest.fixture(scope='session')
def if2no1():
    a = [200, '1条数据删除成功！']
    return a


@allure.epic('策略配置')
@allure.feature('范化-列表上方删除功能')
# @allure.story('')
@allure.severity("normal")
@allure.description('用例描述信息: 策略配置-范化-列表上方删除功能')
def test_up_del(if2no1):    # 删除日志
    token = user_login()[1]
    up_del_url = f"{common_url}/normalize/delete/batch"
    write_log.info(f"登陆成功，范化-列表上方删除功能的url是：{up_del_url}")
    up_del_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    up_del_body = {'ids': ['62zhangkuiac9']}
    res = requests.delete(up_del_url, headers=up_del_headers, json=up_del_body, verify=False)
    d = []
    d.append(res.json()['statusCode'])
    d.append(res.json()['message'])
    write_log.info(f"返回结果---：{res.json()}")
    assert d == if2no1




