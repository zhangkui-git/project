'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2023/3/31 11:42
software: PyCharm
'''
import asyncio
import re
import ssl
import threading
import time

import websocket
from websocket import ABNF

from login_interface import loginGetParams
from zk_dev1.tools.soms.performance_testing.config.config import host, local_ip, IP
from zk_dev1.tools.soms.performance_testing.setting import DIR_NAME


def send_ping(ws):
    while True:
        time_t = int(round(time.time() * 1000))  # 时间戳
        time_str = f'0.,4.ping,13.{time_t}'
        ws.send(time_str, opcode=ABNF.OPCODE_PING)
        print('发送时间戳:', time_str)
        time.sleep(0.5)


def send_nop(ws):
    while True:
        ws.send('3.nop', opcode=ABNF.OPCODE_PING)
        print('发送时间戳:nop')
        time.sleep(5)


def on_message(ws, message):
    # print("监听到服务器返回的消息,内容如下：")
    print('收到' + message)
    with open(DIR_NAME + f'/write_file/num1', 'a') as f:
        f.write(message + '\n')
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


def on_ping(ws, frame_data, ):
    print('on_ping', frame_data, sep=',')
    time_t = int(round(time.time() * 1000))  # 时间戳
    time_str = f'0.,4.ping,13.{time_t}'
    ws.send(time_str, opcode=ABNF.OPCODE_PING)
    print('发送时间戳:', time_str)
    time.sleep(0.5)


def on_pong(ws, frame_data):
    print('on_pong', frame_data, sep=',')


def on_data(ws, frame_data, frame_opcode, frame_in):
    print('on_data', frame_data, frame_opcode, frame_in, sep=',')


def on_error(ws, error):
    print("-----连接出现异常，异常信息如下-----")

    print(error)


# 定义一个用来处理关闭连接的方法
def on_close():
    print("-------连接已关闭------")


def on_open(ws):
    # def run(*args):
    print('on_open')

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

    threading.Thread(target=send_ping()).start()
    threading.Thread(target=send_nop()).start()


class SocketConnect:

    def __init__(self, num, rdp_url, username, user_password, rdp_ip, rdp_name, rdpPassword):
        # self.url = f'wss://{self.host}/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName=op1&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={rdp_password}&width=1670&height=427&dpi=96&security=ANY&?undefined'  # url
        # self.url = rdp_url  # url
        self.username = username  # 远程桌面ip
        self.user_password = user_password  # 远程桌面用户名
        self.rdp_ip = rdp_ip  # 远程桌面密码
        self.rdp_name = rdp_name  # 远程桌面密码
        self.rdpPassword = rdpPassword
        self.num = num
        self.rdp_url = rdp_url
        self.threads = []

    def add_thread(self):
        for n, rdp_name in enumerate(rdp_name_list):
            num = 1 + n
            print(str(num) + '+++++')
            t1 = threading.Thread(target=self.connect())
            self.threads.append(t1)

            with open(DIR_NAME + f'/write_file/num{n + 1}', 'w') as f:
                f.write('')
        # print(threads)
        # for t in threads:  # 启动线程
        #     print('111111111111111111111111111111111111111111111111111111')
        #     t.start()
        #     num_list.append(num)
        # loop = asyncio.get_event_loop()
        # tasks = [self.connect(num) for num in num_list]
        # loop.run_until_complete(asyncio.wait(tasks))
        # loop.close()

    def connect(self):
        # headers, sessionId, user_id, asset_id, asset_user_id = loginGetParams(name=self.username,
        #                                                                       pwd=self.user_password,
        #                                                                       rdp_ip=self.rdp_ip,
        #                                                                       rdp_name=self.rdp_name)
        # rdp_url = f'wss://{IP}:8440/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName=op1&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={self.rdpPassword}&width=1670&height=427&dpi=96&security=ANY&?undefined'
        # print(rdp_url)
        # print(f'第{n}个线程')
        ws = websocket.WebSocketApp(url=self.rdp_url, on_message=self.on_message, on_ping=on_ping,
                                         on_pong=on_pong, on_error=on_error)
        ws.keep_running = True
        ws.run_forever(ping_interval=30, ping_timeout=5, sslopt={"cert_reqs": ssl.CERT_NONE})

    async def websocket_starting(self, n):
        print("\nwebsocket_starting")
        with open(DIR_NAME + f'/write_file/num{n}', 'w') as f:
            f.write('')
        self.connect()

    def on_message(self, ws, message):
        print('收到' + message)
        with open(DIR_NAME + f'/write_file/num{self.num}', 'a') as f:
            f.write(message + '\n')
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

    def on_ping(self, ws, frame_data):
        print('on_ping', frame_data, sep=',')
        time_t = int(round(time.time() * 1000))  # 时间戳
        time_str = f'0.,4.ping,13.{time_t}'
        ws.send(time_str, opcode=ABNF.OPCODE_PING)
        print('发送时间戳:', time_str)
        time.sleep(0.5)

    def on_pong(self, ws, frame_data):
        print('on_pong', frame_data, sep=',')

    def on_data(self, ws, frame_data, frame_opcode, frame_in):
        print('on_data', frame_data, frame_opcode, frame_in, sep=',')

    def on_error(self, ws, error):
        print("-----连接出现异常，异常信息如下-----")

        print(error)

    # 定义一个用来处理关闭连接的方法
    @staticmethod
    def on_close():
        print("-------连接已关闭------")

    def on_open(self, ws):
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

        threading.Thread(target=send_ping).start()
        threading.Thread(target=send_nop).start()


# def socketConnect(username, user_password, rdp_ip, rdp_name):
#     # # self.url = f'wss://{self.host}/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName=op1&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={rdp_password}&width=1670&height=427&dpi=96&security=ANY&?undefined'  # url
#     # self.url = rdp_url  # url
#     # self.rdpIp = rdpIp  # 远程桌面ip
#     # self.rdpName = rdpName  # 远程桌面用户名
#     # self.rdpPassword = rdpPassword  # 远程桌面密码
#     # self.ws = ''
#
#     # def connect(self):
# headers, sessionId, user_id, asset_id, asset_user_id = loginGetParams(name='op1', pwd='Admin@123456',
#                                                                       rdp_ip='192.168.4.119',
#                                                                       rdp_name='test20')
# header = {
#
#     'Sec-WebSocket-Key': 'xlfCeQoEN3rTk64DTR8U7Q=='
# }
# print(header)
# rdp_url = f'wss://{IP}:8440/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName=op1&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp=192.168.4.119&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName=test20&password=Admin@123&width=1670&height=427&dpi=96&security=ANY&?undefined'
# print(rdp_url)
# ws = websocket.WebSocketApp(url=rdp_url, on_message=on_message, on_ping=on_ping,
#                             on_pong=on_pong, on_error=on_error)
# ws.keep_running = True
# ws.run_forever(ping_interval=30, ping_timeout=5, sslopt={"cert_reqs": ssl.CERT_NONE})

if __name__ == '__main__':
    rdp_ip = '192.168.4.119'
    rdp_name = 'test20'
    rdp_name_list = ['test20', 'test21']
    rdpPassword = 'Admin@123'
    name = 'op1'
    password = 'Admin@123456'
    threads = []
        # headers, sessionId, user_id, asset_id, asset_user_id = loginGetParams(name=name, pwd=password, rdp_ip=rdp_ip,
        #                                                                       rdp_name=rdp_name)
        # url = f'wss://{IP}:8440/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName=op1&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={rdpPassword}&width=1670&height=427&dpi=96&security=ANY&?undefined'
        # print(url)
        # socketConnect(username=name, user_password=password, rdp_ip=rdp_ip, rdp_name=rdp_name)
    headers, sessionId, user_id, asset_id, asset_user_id = loginGetParams(name=name,
                                                                          pwd=password,
                                                                          rdp_ip=rdp_ip,
                                                                          rdp_name=rdp_name)
    rdp_url = f'wss://{IP}:8440/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName=op1&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={rdpPassword}&width=1670&height=427&dpi=96&security=ANY&?undefined'
    print(rdp_url)

    for i in range(1):
        SocketConnect(1, rdp_url, username=name, user_password=rdpPassword, rdp_ip=rdp_ip, rdp_name=rdp_name_list[0],
                                  rdpPassword=rdpPassword).connect()
# async def main():
#     # The length AccessTokens, ClientDescriptions and SQLTablesFix determines how many websockets we need to open
#     L = await asyncio.gather(
#         SocketConnect(1, rdp_url, username=name, user_password=rdpPassword, rdp_ip=rdp_ip, rdp_name=rdp_name_list[0],
#                                   rdpPassword=rdpPassword).websocket_starting(1),
#         SocketConnect(2, rdp_url, username=name, user_password=rdpPassword, rdp_ip=rdp_ip, rdp_name=rdp_name_list[1],
#                                             rdpPassword=rdpPassword).websocket_starting(2)

#   )
#
#
# asyncio.get_event_loop().run_until_complete(main())
    # for n, rdp_name in enumerate(rdp_name_list):
    #     num1 = n + 1
    #     with open(DIR_NAME + f'/write_file/num{n + 1}', 'w') as f:
    #         f.write('')
    #     s = SocketConnect(num1, rdp_url, username=name, user_password=rdpPassword, rdp_ip=rdp_ip, rdp_name=rdp_name,
    #                       rdpPassword=rdpPassword)
    #     # s.add_thread()
    #     s.connect()


# SocketConnect(n=1, username=name, user_password=password, rdp_ip=rdp_ip, rdp_name=rdp_name,
#               rdpPassword=rdpPassword).connect()
# for num, rdp_name in rdp_name_list:
#     headers, sessionId, user_id, asset_id, asset_user_id = loginGetParams(name=name, pwd=password, rdp_ip=rdp_ip,
#                                                                           rdp_name=rdp_name)
#     url = f'wss://{IP}:8440/webSocket?token={headers["Authorization"]}&loginUserId={user_id}&loginUserName=op1&loginIp={local_ip}&browser=Chrome-98.0.4758.81&sessionId={sessionId}&assetId={asset_id}&assetsIp={rdp_ip}&protocol=RDP&port=3389&assetUserId={asset_user_id}&assetUserName={rdp_name}&password={rdpPassword}&width=1670&height=427&dpi=96&security=ANY&?undefined'
#     print(url)
#     socketConnect(rdp_url=url)
