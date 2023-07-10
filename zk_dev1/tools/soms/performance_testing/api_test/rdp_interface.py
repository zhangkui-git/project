'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2023/5/9 17:48
software: PyCharm
'''
import datetime
import json
import os
import random
import re
import ssl
import threading
import time

import requests
import websocket
from websocket import ABNF

from zk_dev1.tools.soms.performance_testing.api_test.login_interface import get_iv_key, sm4_login, Login
from zk_dev1.tools.soms.performance_testing.common.dbutil import DB
from zk_dev1.tools.soms.performance_testing.config.config import IP, local_ip, host, password, rdp_ip, rdpPassword, name_list
from zk_dev1.tools.soms.performance_testing.setting import DIR_NAME

# name_list = ['op1', 'op2', 'op3', 'op4', 'op5', 'op6', 'op7', 'op8', 'op9']  # 堡垒机用户名

threads = []  # 线程数
failed_asset = []  # 运行失败的资产

def on_open(ws):
    # def run(*args):
    #     print('on_open')

    def send_ping():
        while True:
            time_t = int(round(time.time() * 1000))  # 时间戳
            time_str = f'0.,4.ping,13.{time_t}'
            ws.send(time_str, opcode=ABNF.OPCODE_PING)
            print('发送时间戳:', time_str)
            time.sleep(0.5)

    def send_nop():
        while True:
            ws.send('3.nop', opcode=ABNF.OPCODE_PING)
            print('发送时间戳:nop')
            time.sleep(5)

    num1 = random.randint(100, 200)

    def send_mouse():
        while True:
            ws.send('5.mouse,2.13,2.59,1.1;', opcode=ABNF.OPCODE_PING)
            # print('发送mouse')
            time.sleep(30)

    threading.Thread(target=send_mouse).start()
    # threading.Thread(target=send_ping).start()
    # threading.Thread(target=send_nop).start()


def on_message(ws, message):
    # print("监听到服务器返回的消息,内容如下：")
    print('收到' + message)
    with open(DIR_NAME + f'/write_file/num1', 'a') as f:
        f.write(message)
    sync_list = []  # sync列表
    if '4.sync' in message:
        addr = [substr.start() for substr in re.finditer('4.sync', message)]  # 查找字串位置
        # print(addr)   # 打印角标
        for st in addr:
            sync_list.append(message[st:st + 21])
        print('旧串', sync_list)
        new_list = list(set(sync_list))  # 去重
        print('新串', new_list)
        for sync in new_list:
            # print(f'发送{sync}')
            ws.send(sync)
            print(f'发送{sync}完成')
        ws.send('3.nop;')
        print('发送:3.nop;')
        ws.send('4.size,4.1670,3.457;')
        print('4.size,4.1670,3.457;')


def on_ping(ws, frame_data, ):
    print('on_ping', frame_data, sep=',')
    time_t = int(round(time.time() * 1000))  # 时间戳
    time_str = f'0.,4.ping,13.{time_t}'
    ws.send(time_str, opcode=ABNF.OPCODE_PING)
    print('发送时间戳:', time_str)
    time.sleep(0.5)


def on_error(ws, error):
    print("-----连接出现异常，异常信息如下-----")
    print(error)


def connect(num, username, rdp_name, rdp_ip, rdpPassword, headers, sessionId, user_id, asset_id, asset_user_id):
    # rdp_url = f'wss://{IP}:8440/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName={username}&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={rdpPassword}&width=1670&height=874&dpi=96&security=ANY&?undefined'
    # rdp_url = f'wss://{IP}:8440/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName={username}&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={rdpPassword}&width=1670&height=874&dpi=96&security=ANY&applicationPublishingAssetId=&connectivityId=&'
    rdp_url = f'wss://{IP}:8440/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName={username}&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={rdpPassword}&width=1670&height=874&dpi=96&security=RDP&applicationPublishingAssetId=&connectivityId=&somsIp={local_ip}&domain=WNT&'

    print(rdp_url)

    def on_pong(ws, frame_data):
        print(f'on_pong{num}', frame_data, sep=',')

    def on_message(ws, message):
        # print("监听到服务器返回的消息,内容如下：")
        # print('收到' + message)
        # with open(DIR_NAME + f'/write_file/{num}', 'a') as f:   # 持续写入
        with open(DIR_NAME + f'/write_file/{num}', 'w') as f:  # 覆盖写入
            f.write(message)
        sync_list = []  # sync列表
        # if '10.filesystem' in message:
        #     ws.send('4.size,4.1670,3.873;')
        #     print('4.size,4.1670,3.873;')
        if '4.sync' in message:
            addr = [substr.start() for substr in re.finditer('4.sync', message)]  # 查找字串位置
            # print(addr)   # 打印角标
            for st in addr:
                sync_list.append(message[st:st + 21])
            # print('旧串', sync_list)
            new_list = list(set(sync_list))  # 去重
            # print('新串', new_list)
            for sync in new_list:
                # print(f'发送{sync}')
                ws.send(sync)
                # print(f'发送{sync}完成')
            ws.send('3.nop;')
            # print('发送:3.nop;')
            ws.send('4.size,4.1670,3.873;')
            # print('4.size,4.1670,3.873;')

    ws = websocket.WebSocketApp(rdp_url, on_message=on_message, on_ping=on_ping, on_error=on_error)
    ws.keep_running = True
    # ws.on_open = on_open
    ws.run_forever(ping_interval=30, ping_timeout=5, sslopt={"cert_reqs": ssl.CERT_NONE})


def user_rdp():
    global ten  # 十位
    global bit  # 个位
    global sessionId
    start_time = datetime.datetime.now()
    # name_list = [f'op{i}' for i in range(1, 21)]
    db = DB('database')
    # iv_value, key_value = get_iv_key()
    for index, name in enumerate(name_list):  # 内层循环控制百位和十位0-19
        # resp = sm4_login(name=name, pwd=password, key_value=key_value, iv_value=iv_value)
        resp = Login.login(name=name, pwd=password)
        result = json.loads(resp.text)
        # print(result)   # 登录结果
        headers = {'Authorization': result["data"]["accessToken"],
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36",
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Content-Type": "application/json;charset=UTF-8",
                   "Cookie": "sidebarStatus=1",
                   "Connection": "keep-alive"
                   }

        for bit in range(10):  # 外层循环控制个位
            if index == 0:
                rdp_num = str(bit + 1)
                rdp_name = f'test{rdp_num}'  # 1-10
                # continue
                if bit == 9:
                    num = len(name_list)
                    rdp_num = str(num * 10)
                    rdp_name = f'test{num}0'

            else:
                rdp_num = f'{index}{bit}'
                rdp_name = f'test{index}{bit}'
            # print(rdp_num, rdp_name, name)    # 打印 rdp数量，名字，用户名

            try:
                userId = db.select(f"select id from soms.system_user where user_name='{name}'")  # loginUserId 用户id
                user_id = userId[0]['id']
                assetId = db.select(f"select id from soms.soms_asset_info where ip='{rdp_ip}'")  # assetsId 资产id
                asset_id = assetId[0]['id']
                assetUserId = db.select(
                    f"select id from soms.soms_asset_user_pwd where username='{rdp_name}'")  # assetUserId 资产用户id
                # print(f"select id from soms.soms_asset_user_pwd where username='{rdp_name}'")
                # print(assetUserId)
                asset_user_id = assetUserId[0]['id']

                json1 = {"assetId": asset_id, "assetsIp": rdp_ip, "protocol": "RDP", "port": "3389",
                         "assetUserId": asset_user_id,
                         "userName": rdp_name, "password": rdpPassword}
                # print(f'{host}/loginAsset/init')
                # print(headers)
                # print(json1)
                resp = requests.post(url=f'{host}/loginAsset/init', headers=headers, json=json1,
                                     verify=False)  # 获取 session
                result = resp.json()
                # print(result)
                sessionId = result['data']['sessionId']
                # print(sessionId)
                with open(DIR_NAME + f'/write_file/{rdp_num}', 'w') as f:   # 执行时清空/write_file/{rdp_num}中的内容
                    f.write('')
                t = threading.Thread(target=connect, name=f'Thread{rdp_num}', args=(
                    rdp_num, name, rdp_name, rdp_ip, rdpPassword, headers, sessionId, user_id, asset_id, asset_user_id))
                threads.append(t)
            except:
                failed_asset.append(rdp_name)
    db.close()
    # print(threads)  # 打印线程
    print('连接失败的用户:', failed_asset)

    for th in threads:  # 启动线程
        th.start()
        time.sleep(1)

def result_compare(start_time):
    """" 结果比对 """

    file_list = os.listdir(DIR_NAME + '/write_file/')  # 所有的文件
    file_list_order = []  # 排序后的文件列表[1,2,3,4,5,6,7,8,9,10]

    for num in file_list:  # 排序
        file_list_order.append(int(num))
        file_list_order.sort(reverse=False)

    user_num = len(name_list) * 10  # rdp_数量
    while True:
        time.sleep(30)
        result_list_before = []  # 结果
        result_list_after = []  # 5分钟之后的结果
        faild_stop_asset = []  # 失败或者停止的资产
        success_asset = []  # 失败或者停止的资产
        for file_name in file_list_order[:user_num]:
            with open(DIR_NAME + f'/write_file/{file_name}', 'r') as f:
                result = f.readline()
                result_list_before.append(result)
        print(result_list_before)
        time.sleep(300)
        # print(file_list_order[:user_num])
        for file_name in file_list_order[:user_num]:
            with open(DIR_NAME + f'/write_file/{file_name}', 'r') as f:
                result = f.readline()
                result_list_after.append(result)
        print(result_list_after)
        for index, file_name in enumerate(file_list_order[:user_num]):  # 对比前后五分钟的结果，
            if result_list_before[index] == result_list_after[index]:
                faild_stop_asset.append('test{}'.format(file_name))
            else:
                success_asset.append('test{}'.format(file_name))
        create_threads = len(threads)
        success_asset = len(success_asset)
        now_time = datetime.datetime.now()
        print(
            f'创建线程数{create_threads},存在线程数{success_asset},失败或者停止运行的资产数量：{len(faild_stop_asset)}，{faild_stop_asset}，当前时间:{now_time}，运行时间:{now_time - start_time}')
        time.sleep(270)