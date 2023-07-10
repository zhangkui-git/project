'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2021/11/17 14:08
software: PyCharm
'''
import json
import time

import requests
import urllib3
from Crypto.PublicKey import RSA
from zk_dev2.test.other_py.apiautotest.common.client import RequestsClient
from zk_dev2.test.other_py.apiautotest.common.encry_decry import RsaEncrypt
from zk_dev2.test.other_py.apiautotest.config.config import host
from zk_dev2.test.other_py.apiautotest.data.common_data import username, password, personal_username
from zk_dev2.test.other_py.apiautotest.setting import DIR_NAME


class IsaLogin():
    def __init__(self):
        self.url = host + '/login/userLogin'
        self.method = 'post'
        self.json = {"userName": username, "userPassword": password}


class GetRsa():
    def __init__(self):
        self.url = host + '/login/getPublicKey'
        self.method = 'get'


class Login(RequestsClient):
    def __init__(self, name, pwd):
        RequestsClient.__init__(self)
        self.url = host + '/login/userLogin'
        self.method = 'post'

        user = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(name)
        pas = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(pwd)
        self.json = {"userName": user,
                     "userPassword": pas}


def login_test(name, pwd):
    # print(generate_public_rsa())
    generate_public_rsa()
    # login = Login(name, pwd).send()
    login = Login(name, pwd).send()
    result = json.loads(login.text)
    if name == 'audit':
        time.sleep(1)
    # print(result)
    # header = {'Authorization': result["data"]["accessToken"]}
    header = result["data"]["accessToken"]
    return header


def about():
    """ 关于接口获取日志审计、态势感知关于中的名称及版本信息 """
    header = login_test()
    url = host + '/systeminfo/detail'
    resp = requests.get(url=url, headers=header, verify=False)
    result = json.loads(resp.text)
    # 工业安全态势感知平台 日志审计与分析系统
    if result['data']['name'] == '工业安全态势感知平台':
        name = result['data']['name'][2:-2]
    else:  # 日志审计与分析系统
        name = result['data']['name']
    version = result['data']['version'][5:-1]
    return name, version


# def tym_login():
#     print(generate_public_rsa())
#     login = Login(personal_username,password).send()
#
#     result = json.loads(login.text)
#     # print(result)
#     header = {'Authorization': result["data"]["accessToken"]}
#     return header
def generate_public_rsa():
    url = host + '/login/getPublicKey'
    res = requests.get(url=url, verify=False)
    res_json = json.loads(res.text)
    # print(res_json['message'])

    with open(DIR_NAME + '/common/public_key.keystore', 'w') as f:
        f.write('-----BEGIN PUBLIC KEY-----\n')
        f.write(res_json['message'] + '\n')
        f.write('-----END PUBLIC KEY-----')

    data = RSA.importKey(open(DIR_NAME + '/common/public_key.keystore').read())
    return data


def about():
    """ 获取日志审计、态势感知关于中的名称及版本信息 """
    header = {'Authorization': login_test(username, password)}
    url = host + '/systeminfo/detail'
    resp = requests.get(url=url, headers=header, verify=False)
    result = json.loads(resp.text)
    # 工业安全态势感知平台 日志审计与分析系统
    if result['data']['name'] == '工业安全态势感知平台':
        name = result['data']['name'][2:-2]
    else:  # 日志审计与分析系统
        name = result['data']['name']
    version = result['data']['version'][5:-1]
    return name, version


if __name__ == '__main__':
    # pass
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 取消ssl安全提示
    header = login_test(username, password)
    Authorization = header
    print(header)
    print(about())
    # IsaLogin().a()
    # print(about())
    # data = {
    #     "startPage": 1,
    #     "pageSize": 10,
    #     "keyword": ""
    # }
    #
    # res = requests.post(url=host + '/assets/confirm/page', json=data, headers=Authorization, verify=False)
    # print(res.text)
