from get_token import *

token = user_login()


def asset_add():
    asset_add_url = f"{host}/asset/assetadd"
    asset_add_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    asset_add_body = {"name":"123@@@@!!!!!!!!!","groupId":3,"ip":"111.2.3.2","ipStandby":"","ipV6":"","ipV6Standby":"","platform":"2eb1b7c4e81fef49b43177a34f879900","protocol":["SSH/22"],"scriptName":"","url":"","db":"","serverName":3,"somsAssetScripts":[]}
    res = requests.post(url=asset_add_url, headers=asset_add_headers, json=asset_add_body, verify=False)
    print(res.json())


def asset_adds(n):
    asset_adds_url = f"{host}/asset/assetadd"
    asset_adds_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    asset_adds_body = {"name": f"test1-13.{n}","groupId": 3,"ip": f"192.168.13.{n}","ipStandby": "","ipV6": "","ipV6Standby": "","platform": "Windows","protocol": ["SSH/22"]}
    res = requests.post(url=asset_adds_url, headers=asset_adds_headers, json=asset_adds_body, verify=False)
    print(res.json())


def asset_password():
    asset_password_url = f"{host}/userPwd/passwordadd"
    asset_password_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    asset_password_body = {"assetId": 376, "username": "test2", "password": "Admin@123", "protocol": "RDP"}
    res = requests.post(url=asset_password_url, headers=asset_password_headers, json=asset_password_body, verify=False)
    print(res.json())


def asset_passwords(n):
    asset_passwords_url = f"{host}/userPwd/passwordadd"
    asset_passwords_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    asset_passwords_body = {"assetId": 5, "username": f"ztest{n}", "password": "Admin@123", "protocol": "RDP"}
    res = requests.post(url=asset_passwords_url, headers=asset_passwords_headers, json=asset_passwords_body, verify=False)
    print(res.json())


def add_user():
    add_user_url = host + '/userpermission/usermanage/addUser'
    add_user_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token}'}
    add_user_body = {"userName": "30KNENd6WgKaHCnsPzFNgQ==", "roleId": 1, "telephone": "13211131113", "email": "123@qq.com", "realName": "a11", "authType": 0, "validTime": "2023-06-13", "invalidTime": "2023-06-29", "password": "X+XejHe8D7IO6NfwCRH+hQ==", "description": "a11", "updateType": 3}
    res = requests.post(url=add_user_url, headers=add_user_headers, json=add_user_body, verify=False)
    print(res.json())


if __name__ == '__main__':
    # n = 1
    # while n <= 250:
    #     asset_adds(n)
    #     n += 1
    # asset_add()
    # n = 2
    # while n <= 40:
    #     asset_passwords(n)
    #     n += 1
    # asset_password()
    add_user()


