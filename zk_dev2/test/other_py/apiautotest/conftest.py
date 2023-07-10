import time
from typing import List

# 下面这个函数时pytest自带的钩子函数

import pytest
import urllib3

from api.base_api import BaseApi
from api.isa.admin import SshConnect
from api.isa.policy_config import AddLogSource
from api.login_api import login_test
from common.dbutil import Linux, DB
from config.config import IP, linux_port, linux_user, linux_pass, local_ip
from data.common_data import username, password, admin, audit


def pytest_collection_modifyitems(
        session: "Session", config: "Config", items: List["Item"]
) -> None:
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")

"""
fixture 作用域 session指的是在一次pytest执行的过程只会执行一次，不管调用多少次
        作用域 function指的是在函数里调用一次就执行一次，有多少个函数就执行多少次
        作用域 module 指的是在同一个模块里只执行一次，不管被调用多少次
        作用域 package 指的是在同一个包中只执行一次，不管被调用多少次
autouse=True 指的是测试一开始或者结束就自动执行，无需调用        
"""


@pytest.fixture(scope='session', autouse=True)
def initDriver():
    # 开启SSH服务
    admin_header = login_test(admin, password)
    ssh = SshConnect()
    ssh.headers = admin_header
    ssh.send()
    time.sleep(2)
    linux = Linux()
    linux.remoteConnect(IP, linux_port, linux_user, linux_pass)
    # 关闭防火墙
    linux.exec_command('systemctl stop firewalld.service')
    # # 打开远程ssh开关
    # linux.exec_command('systemctl  start sshd')
    linux.close()
    db = DB('database')
    # 添加tym 用户,判断tym是否存在，如果存在跳过
    id = db.select("select user_id from `soc`.`soc_user_info` where user_name = 'tym'")
    # print(id)
    # print(len(id))
    if len(id) == 0:
        db.update("INSERT INTO `soc`.`soc_user_info` (`user_name`, `user_description`, `user_password`, `user_salt`, `role_id`, `last_login_time`, `create_time`, `pwd_update_time`) VALUES ('tym', '', '8b9b55a4ff529b6760da4dac1a62a535da6ed9cdc4448cb1600916809f81f666', '157cda60745105e1be13f19c8fbc57ff', '2', '2022-03-02 16:19:43', '2022-03-01 10:06:07', '2022-03-01 10:06:07')")
    # 添加日志源,判断日志源是否存在，如果存在跳过
    value = db.select("select * from soc.soc_log_source_info where asset_ip = '{}'".format(local_ip))
    print(value)
    print(len(value))
    if len(value) == 0:
        AddLogSource(name=local_ip, ip=local_ip, normalizeGroup=[1386, 1393, 1400, 11404]).send()
        # db.update("INSERT INTO `soc`.`soc_log_source_info` (`id`,`log_source_name`, `asset_ip`, `fk_asset_type_path`, `fk_factory_path`, `fk_normalize_group_path`, `select_sql`, `non_normalizate_count`, `today_count`, `create_time`, `update_time`, `is_encryption`, `algorithm`, `private_key`) VALUES ('621f31a3561ee6631bbfff2f','{}', '{}', '101001', '3', '1393,1386,1400,11404', NULL, '1', '10', '2022-03-02 16:20:37', '2022-03-02 16:21:30', '0', '1', '')".format(local_ip, local_ip))
    # 关闭告警归并
    db.update("UPDATE `soc`.`soc_alarm_merge_info` SET `merge_status`='2' WHERE  `merge_name`='告警归并策略'")
    db.close()

    yield

    # 打开告警归并
    # db = DB('database')
    # db.update("UPDATE `soc`.`soc_alarm_merge_info` SET `merge_status`='1' WHERE  `merge_name`='告警归并策略'")
    # db.close()
    # # 关闭SSH服务
    # admin_header = login_test(admin, password)
    # ssh = SshConnect(isopen=False)
    # ssh.headers = admin_header
    # linux = Linux()
    # linux.remoteConnect(IP, linux_port, linux_user, linux_pass)
    # # 关闭防火墙
    # linux.exec_command('systemctl start firewalld.service')
    # # # 打开远程ssh开关
    # # linux.exec_command('systemctl  start sshd')
    # linux.close()


@pytest.fixture(scope='module', autouse=True)
def get_token():
    # resp = IsaLogin().send()
    # result =json.loads(resp.text)
    # # BaseApi.buyer_token = jsonpath.jsonpath(resp.json(),'$.access_token')[0]
    header = login_test(username, password)
    BaseApi.Authorization = header['Authorization']
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 取消ssl安全提示

@pytest.fixture(scope='function', autouse=True)
def get_header():
    admin_header = login_test(admin, password)
    operator_header = login_test(username, password)
    audit_header = login_test(audit, password)
    yield admin_header, operator_header, audit_header


# if __name__ == '__main__':
#     operator_header = login_test(username, password)
#     add = AddLogSource(name=local_ip, ip=local_ip, normalizeGroup=[1386, 1393, 1400, 11404])
#     add.headers = operator_header
#     resp = add.send()
#     print(resp.json())