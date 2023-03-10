import datetime
import requests
import time
ip = '192.168.100.248'
user = 'op1'
pwd = 'Admin@123456'


def one_login():
    url = f"https://{ip}:8440/login/remote/authorize"
    headers = {"Content-Type": "application/json"}
    body = {"name": f"{user}", "password": f"{pwd}"}
    res = requests.post(url=url, headers=headers, json=body, verify=False)
    print("时间是：", datetime.datetime.now(), "\n单点登录的url：", res.json()['data'], "\n......等候1分钟测试url的token有效期")
    time.sleep(65)
    print("请再次测试单点登录的url：", res.json()['data'])


if __name__ == '__main__':
    one_login()





