"""
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2023/5/9 17:36
software: PyCharm
"""
import json
import ssl
import threading
import time

import requests
import websocket

from zk_dev1.tools.soms.performance_testing.api_test.login_interface import sm4_login, get_iv_key, Login
from zk_dev1.tools.soms.performance_testing.common.dbutil import DB
from zk_dev1.tools.soms.performance_testing.config.config import host, local_ip, password, IP, ssh_ip, linux_user

failed_asset = []  # 运行失败的资产
thread_list = []  # 登录用户数
asset_list = []  # 资产数


def ssh_connect(count, param):
    """
    单用户连接
    """
    try:
        ws = websocket.create_connection(f'wss://{IP}:8440/webssh', sslopt={"cert_reqs": ssl.CERT_NONE})
        # print(param)
        ws.send(json.dumps(param))
        time.sleep(4)
        for i in range(count):  # 一次一分钟 传入次数统计时常
            # ws.recv()
            # ws.send('{"operate":"command","command":"\\r"}')  # 回车返回目录
            # time.sleep(1)
            ws.send('{"operate":"command","command":"pwd"}')
            # print(f'{i}结果', ws.recv())
            # ws.recv()
            time.sleep(1)
            ws.send('{"operate":"command","command":"\\r"}')  # 回车返回目录
            time.sleep(1)
            # # result = ws.recv()
            # ws.send('{"operate":"command","command":"\\r"}')  # 回车返回目录
            time.sleep(60)
    finally:
        ws.close()


def ssh_test(name, ssh_name, count, ip=ssh_ip):
    """
    单用户并发十个
    """
    # iv_value, key_value = get_iv_key()
    # resp = sm4_login(name=name, pwd=password, key_value=key_value, iv_value=iv_value)
    resp = Login.login(name=name, pwd=password)  # 登录
    result = json.loads(resp.text)
    # print(result)
    headers = {'Authorization': result["data"]["accessToken"],
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Content-Type": "application/json;charset=UTF-8",
               "Cookie": "sidebarStatus=1",
               "Connection": "keep-alive"
               }
    token = result["data"]["accessToken"]
    db = DB('database')
    userId = db.select(f"select id from soms.system_user where user_name='{name}'")  # loginUserId 用户id
    print(222, userId)
    user_id = userId[0]['id']
    assetId = db.select(f"select id from soms.soms_asset_info where ip='{ip}'")  # assetsId 资产id
    print(1111111, assetId)
    asset_id = assetId[0]['id']
    assetUserId = db.select(
        f"select id from soms.soms_asset_user_pwd where username='{ssh_name}' and asset_id={asset_id}")  # assetsId 资产id
    assetUserId = assetUserId[0]['id']
    db.close()
    json1 = {"assetId": asset_id, "assetsIp": ip, "protocol": "SSH", "port": "22",
             "assetUserId": assetUserId,
             "userName": "", "password": ""}
    resp = requests.post(url=f'{host}/loginAsset/init', headers=headers, json=json1, verify=False)  # 获取 session
    result = resp.json()
    print(result)
    sessionId = result['data']['sessionId']
    param = {"operate": "connect",
             "token": token,
             "loginUserId": user_id, "loginUserName": name, "browser": "Chrome-98.0.4758.81", "loginIp": local_ip,
             "sessionId": sessionId, "type": "connect", "assetId": asset_id,
             "assetsIp": ip, "protocol": "SSH", "port": "22", "assetUserId": assetUserId, "assetUserName": "",
             "password": ""}
    # print(param)
    for i in range(1, 11):  # 创建十个ssh连接
        try:
            t = threading.Thread(target=ssh_connect, name=f'ssh_{name}_{i}', args=(count, param))
            asset_list.append(t)
            t.start()
            time.sleep(1)
        except:
            failed_asset.append(t.name)
    # print(asset_list)
    # for asset in asset_list:
    #     # try:
    #     asset.start()
    #     time.sleep(1)
    # except:
    #     print('失败')
    #     failed_asset.append(asset.name)


def users_ssh(count):
    """
    并发数多用户ssh
    """
    name_list = [f'op{num}' for num in range(21, 41)]  # 用户名列表
    for name in name_list:  # 创建 用户线程
        t = threading.Thread(target=ssh_test, name=f'ssh_{name}', args=(name, linux_user, count))
        thread_list.append(t)
    # print(thread_list)
    for thread in thread_list:  # 5秒执行登录一个用户
        thread.start()
        time.sleep(5)
    # for i in range(count):  # 循环检索 运行情况
    #     time.sleep(30)
    #     print('登录的用户数：', len(thread_list), '创建的资产数:', len(asset_list), '执行命令次数:', count, '运行失败的资产数:', len(failed_asset), failed_asset)
