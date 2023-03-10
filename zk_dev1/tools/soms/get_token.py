from SM4_CBC import *

user = SM4Utils().encryptData_CBC(bytes(user, "UTF-8"))
pas = SM4Utils().encryptData_CBC(bytes(pas, "UTF-8"))


def user_login():   # 登录
    url = f"{host}/login/userLogin"
    headers = {"Content-Type": "application/json"}
    # body = {"userName": f"{user}", "password": f"{pas}"}
    body = {"userName": f"{user}", "password": f"{pas}"}
    res = requests.post(url=url, headers=headers, json=body, verify=False)
    print(res.json())
    print("\ntoken信息：", res.json()['data']['accessToken'])
    return res.json()['data']['accessToken']


if __name__ == '__main__':
    user_login()





