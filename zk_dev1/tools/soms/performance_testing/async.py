"""
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2023/4/3 16:34
software: PyCharm
"""
import asyncio
import datetime
import json
import os
import random
import re
import ssl
import threading
import time
import warnings

import requests
import websocket
import websockets
from websocket import ABNF
import time
from api_test.login_interface import loginGetParams, get_iv_key, sm4_login, Login
from api_test.rdp_interface import connect, result_compare, user_rdp
from api_test.ssh_interface import users_ssh
from common.dbutil import DB
from config.config import local_ip, IP, host, password
from setting import DIR_NAME

if __name__ == '__main__':
    ssl._create_default_https_context = ssl.create_default_context()
    warnings.filterwarnings('ignore')  # 忽略提示信息
    users_ssh(1440)  # ssh测试
    start_time = datetime.datetime.now()
    # user_rdp()  # rdp测试
    t_result = threading.Thread(target=result_compare(start_time))
    t_result.start()  # 启动结果比对线程
