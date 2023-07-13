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


def on_message(ws, message):
    # print("监听到服务器返回的消息,内容如下：")
    print('收到' + message)
    with open(DIR_NAME + f'/write_file/num1', 'a') as f:
        f.write(message)

def on_ping(ws, frame_data):
    print('on_ping', frame_data, sep=',')
    time_t = int(round(time.time() * 1000))  # 时间戳
    time_str = f'0.,4.ping,13.{time_t}'
    ws.send(time_str, opcode=ABNF.OPCODE_PING)
    print('发送时间戳:', time_str)
    time.sleep(0.5)


def on_error(ws, error):
    print("-----连接出现异常，异常信息如下-----")
    print(error)


def connect(rdp_url):
    print(rdp_url)

    ws = websocket.WebSocketApp(rdp_url, on_message=on_message, on_ping=on_ping, on_error=on_error)
    ws.keep_running = True
    ws.run_forever(ping_interval=30, ping_timeout=5, sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == '__main__':
    rdp_url = "wss://192.168.5.163:8440/webSocket?token=0dd6503580ff0ae060525a745587832f2b2c3f86ceb5f6a228e468b3a4397806174ed6e9df276dcbdc2c11071cd64e67e8cbc4bebc5aa664e0dac922964af7cd20bb2c4ec4652b905e94b433cbcf46ea90e1bea2b214f074f532837c04281ec1bfbf16516c0820a26c748cd335f6dc716efdea78cf8514dc2054eed4cf9f6fcb9f5f094c93ae6373fbafb2ad000b703c4759019faf2397d5d479a72e41e18409e7c303524b7b3968389d817a3d9fe45f9d5acd9c347620e98e31fd086d9a933c9273fe1b83be346e7cef74c7ded2aefd8e43f4e02bcdd457a40bb3d8f775af127c3e66b8be65345ce18be8c5a90bf173cc6705f652aee13751db7a832a4cf55a1c444cce2b837213572b6d871a833997abc54a8645dde501&loginUserId=6&loginUserName=op1&loginIp=&browser=Chrome-98.0.4758.81&sessionId=bdc0489f379444c38166a87726f0cce3&assetId=2&assetsIp=192.168.4.119&protocol=RDP&port=3389&assetUserId=20&assetUserName=test1&password=Admin@123&width=1670&height=874&dpi=96&security=RDP&applicationPublishingAssetId=&connectivityId=&somsIp=&domain=WNT&"
    connect(rdp_url)

