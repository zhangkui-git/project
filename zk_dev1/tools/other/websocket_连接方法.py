import datetime
import json
import os
import random
import re
import ssl
import threading
import time

import websocket
from websocket import ABNF

from zk_dev1.tools.soms.performance_testing.setting import DIR_NAME


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
    # sync_list = []  # sync列表
    # if '4.sync' in message:
    #     addr = [substr.start() for substr in re.finditer('4.sync', message)]  # 查找字串位置
    #     # print(addr)   # 打印角标
    #     for st in addr:
    #         sync_list.append(message[st:st + 21])
    #     print('旧串', sync_list)
    #     new_list = list(set(sync_list))  # 去重
    #     print('新串', new_list)
    #     for sync in new_list:
    #         # print(f'发送{sync}')
    #         ws.send(sync)
    #         print(f'发送{sync}完成')
    #     ws.send('3.nop;')
    #     print('发送:3.nop;')
    #     ws.send('4.size,4.1670,3.457;')
    #     print('4.size,4.1670,3.457;')


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


def connect(num, url):
    # rdp_url = f'wss://{IP}:8440/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName={username}&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={rdpPassword}&width=1670&height=874&dpi=96&security=RDP&applicationPublishingAssetId=&connectivityId=&somsIp={local_ip}&domain=WNT&'
    rdp_url = url
    print(rdp_url)

    def on_pong(ws, frame_data):
        print(f'on_pong{num}', frame_data, sep=',')

    # def on_message(ws, message):
    #     # print("监听到服务器返回的消息,内容如下：")
    #     print('收到' + message)
    #     # with open(DIR_NAME + f'/write_file/{num}', 'a') as f:   # 持续写入
    #     with open(DIR_NAME + f'/write_file/{num}', 'w') as f:  # 覆盖写入
    #         f.write(message)
    #     sync_list = []  # sync列表
    #     # if '10.filesystem' in message:
    #     #     ws.send('4.size,4.1670,3.873;')
    #     #     print('4.size,4.1670,3.873;')
    #     if '4.sync' in message:
    #         addr = [substr.start() for substr in re.finditer('4.sync', message)]  # 查找字串位置
    #         # print(addr)   # 打印角标
    #         for st in addr:
    #             sync_list.append(message[st:st + 21])
    #         # print('旧串', sync_list)
    #         new_list = list(set(sync_list))  # 去重
    #         # print('新串', new_list)
    #         for sync in new_list:
    #             # print(f'发送{sync}')
    #             ws.send(sync)
    #             # print(f'发送{sync}完成')
    #         ws.send('3.nop;')
    #         # print('发送:3.nop;')
    #         ws.send('4.size,4.1670,3.873;')
    #         # print('4.size,4.1670,3.873;')
    print(111111111111)
    ws = websocket.WebSocketApp(rdp_url, on_message=on_message, on_ping=on_ping, on_error=on_error)
    print(3333333333)
    ws.keep_running = True
    # ws.on_open = on_open
    print(444444444444444444)
    ws.run_forever(ping_interval=30, ping_timeout=5, sslopt={"cert_reqs": ssl.CERT_NONE})
    print(2222222222222)


if __name__ == '__main__':
    url = "wss://192.168.5.163:8440/webSocket?token=0dd6503580ff0ae060525a745587832f2b2c3f86ceb5f6a228e468b3a4397806174ed6e9df276dcbdc2c11071cd64e67e8cbc4bebc5aa664e0dac922964af7cd20bb2c4ec4652b905e94b433cbcf46ea90e1bea2b214f074f532837c04281ec1bfbf16516c0820a26c748cd335f6dc716efdea78cf8514dc2054eed4cf9f6fcb9f5f094c93ae6373fbafb2ad000b703c4759019faf2397d5d479a72e41e18409e7c303524b7b3968389d817a3d9fe45f9d5acd9c347620e98e31fd086d9a933c9273fe1b83be346e7cef74c7ded2aefd8e43f4e02bcdd457a40bb3d8f775af127c3e66b8be65345ce18be8c5a90bf173cc6705f652aee13751db7a832a4cf55a1c444cce2b837213572b6d871a833997abc54a8645dde501&loginUserId=6&loginUserName=op1&loginIp=&browser=Chrome-98.0.4758.81&sessionId=bdc0489f379444c38166a87726f0cce3&assetId=2&assetsIp=192.168.4.119&protocol=RDP&port=3389&assetUserId=20&assetUserName=test1&password=Admin@123&width=1670&height=874&dpi=96&security=RDP&applicationPublishingAssetId=&connectivityId=&somsIp=&domain=WNT&"
    connect(1, url)

