from zk_dev2.test.many_login.encry_decry import *
from conf import *


def login(user_body):
    url = f"{host}/login/userLogin"
    headers = {"Content-Type": "application/json"}
    # body = list_data[num]
    body = user_body
    res = requests.post(url=url, headers=headers, json=body, verify=False)
    print("======操作结果是======", f"{res.json()}")
    print("======token是======", f"{res.json()['data']['accessToken']}")
    token = res.json()['data']['accessToken']
    print(token)
    return token


def many_token():
    generate_public_rsa()
    # user_list = [21, 11]
    user_list = users
    data_list = []
    for i, name in enumerate(user_list):
        user = RsaEncrypt('public_key.keystore').encrypt_data(user_list[0])
        pas = RsaEncrypt('public_key.keystore').encrypt_data(f'{pwd}')
        data = {"userName": user, "userPassword": pas}
        print(f"用户名：op{name}----登录成功", data)
        data_list.append(login(data))
    print(data_list)
    return data_list


if __name__ == '__main__':
    many_token()
    # user_list = [12, 11]
    # for i, name in enumerate(user_list):
    #     user = RsaEncrypt('public_key.keystore').encrypt_data(f'op{name}')
    #     pas = RsaEncrypt('public_key.keystore').encrypt_data('Admin@123456')
    #     data = {"userName": user, "userPassword": pas}
    #     print("用户名：", name)
    #     login(data)


















