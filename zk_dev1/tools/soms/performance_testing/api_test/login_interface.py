'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2023/3/31 12:03
software: PyCharm
'''
import json

import requests
from Crypto.PublicKey import RSA

from zk_dev1.tools.soms.performance_testing.common.dbutil import DB
from zk_dev1.tools.soms.performance_testing.common.encry_decry import Sm4Encrypt, RsaEncrypt
from zk_dev1.tools.soms.performance_testing.config.config import host
from zk_dev1.tools.soms.performance_testing.logger import GetLogger
from zk_dev1.tools.soms.performance_testing.setting import DIR_NAME


class Login:

    @staticmethod
    def login(name, pwd):
        global resp
        url = host + '/login/userLogin'
        method = 'post'
        headers = {
            'Authorization': '',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive"
        }

        if Login.get_encry_type() == '1':
            Login.generate_public_rsa()
            user = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(name)
            pictureCode = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(' ')
            pas = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(pwd)
            json = {"userName": user,
                    "pictureCode": pictureCode,
                    "password": pas}
            resp = requests.request(method=method, url=url, json=json, headers=headers, verify=False)

        elif Login.get_encry_type() == '2':
            iv_value, key_value = Login.get_iv_key()
            user = Sm4Encrypt().encrypt_data(key_value=key_value, iv_value=iv_value, input_data=name)
            pas = Sm4Encrypt().encrypt_data(key_value=key_value, iv_value=iv_value, input_data=pwd)
            json = {"userName": str(user, 'utf-8'),
                    "password": str(pas, 'utf-8')}
            resp = requests.request(method=method, url=url, json=json, headers=headers, verify=False)
        return resp

    @staticmethod
    def generate_public_rsa():
        """ 获取密钥，写到文件 """
        url = host + '/login/getPublicKey'
        GetLogger().get_logger().info('接口地址:{}'.format(url))
        res = requests.get(url=url, verify=False)
        GetLogger().get_logger().info('接口信息:{}'.format(res.text))
        res_json = json.loads(res.text)
        # print(res_json['data']['key'])

        with open(DIR_NAME + '/common/public_key.keystore', 'w') as f:
            f.write('-----BEGIN PUBLIC KEY-----\n')
            f.write(res_json['data']['key'] + '\n')
            f.write('-----END PUBLIC KEY-----')

        data = RSA.importKey(open(DIR_NAME + '/common/public_key.keystore').read())
        return data

    @staticmethod
    def get_encry_type():
        """ 获取加密类型 """
        url = host + '/login/getEncryptAndDecryptType'
        GetLogger().get_logger().info('接口地址:{}'.format(url))
        res = requests.get(url=url, verify=False)
        GetLogger().get_logger().info('接口信息:{}'.format(res.text))
        result = res.json()
        type = result['data']['type']

        return type

    @staticmethod
    def get_iv_key():
        """ publicKey获取iv，key """

        url = host + '/login/getPublicKey'
        GetLogger().get_logger().info('接口地址:{}'.format(url))
        res = requests.get(url=url, verify=False)
        GetLogger().get_logger().info('接口信息:{}'.format(res.text))
        result = res.json()
        iv = result['data']['iv']
        key = result['data']['key']
        return iv, key


def get_iv_key():
    """ publicKey获取iv，key """

    url = host + '/login/getPublicKey'
    # GetLogger().get_logger().info('接口地址:{}'.format(url))
    res = requests.get(url=url, verify=False)
    # GetLogger().get_logger().info('接口信息:{}'.format(res.text))
    result = res.json()
    iv = result['data']['iv']
    key = result['data']['key']
    return iv, key


def sm4_login(name, pwd, key_value, iv_value):
    """  登录 """

    url = host + '/login/userLogin'
    method = 'post'
    headers = {
        'Authorization': '',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive"
    }
    soms = Sm4Encrypt()
    user = soms.encrypt_data(key_value=key_value, iv_value=iv_value, input_data=name)
    pas = soms.encrypt_data(key_value=key_value, iv_value=iv_value, input_data=pwd)
    json = {"userName": str(user, 'utf-8'),
            "password": str(pas, 'utf-8')}
    resp = requests.request(method=method, url=url, json=json, headers=headers, verify=False)

    return resp


def loginGetParams(assetsIp, name, pwd, rdp_ip, rdp_name):
    """
    登录获取参数:
    sessionId, user_id, asset_id, asset_user_id
    """
    db = DB('database')
    userId = db.select("select id from soms.system_user where user_name='op1'")  # loginUserId 用户id
    user_id = userId[0]['id']
    assetId = db.select(f"select id from soms.soms_asset_info where ip='{rdp_ip}'")  # assetsId 资产id
    asset_id = assetId[0]['id']
    assetUserId = db.select(
        f"select id from soms.soms_asset_user_pwd where username='{rdp_name}'")  # assetUserId 资产用户id
    asset_user_id = assetUserId[0]['id']
    iv_value, key_value = get_iv_key()
    resp = sm4_login(name=name, pwd=pwd, key_value=key_value, iv_value=iv_value)
    result = json.loads(resp.text)
    headers = {'Authorization': result["data"]["accessToken"],
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Content-Type": "application/json;charset=UTF-8",
               "Cookie": "sidebarStatus=1",
               "Connection": "keep-alive"
               }
    json1 = {"assetId": asset_id, "assetsIp": assetsIp, "protocol": "RDP", "port": "3389",
             "assetUserId": asset_user_id,
             "userName": "", "password": ""}
    resp = requests.post(url=f'{host}/loginAsset/init', headers=headers, json=json1, verify=False)  # 获取 session
    result = resp.json()
    print(result)
    sessionId = result['data']['sessionId']

    return headers, sessionId, user_id, asset_id, asset_user_id
