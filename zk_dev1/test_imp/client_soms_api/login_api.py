from zk_dev1.test_imp.common_soms_tool.SM4_CBC import *


def SomsLogin(user, pas):
    url = host + "/login/userLogin"
    user = SM4Utils().encryptData_CBC(bytes(user, "UTF-8"))
    pas = SM4Utils().encryptData_CBC(bytes(pas, "UTF-8"))
    body = {"userName": f"{user}", "password": f"{pas}"}
    res = requests.post(url=url, json=body, verify=False)
    # print(res.json()['data']['accessToken'])
    return res.json()['data']['accessToken']


def about():
    url = host + '/systeminfo/detail'
    res = requests.get(url=url, verify=False)
    print("产品名称：", res.json()['data']['name'])
    print("产品版本：", res.json()['data']['version'])


if __name__ == '__main__':
    SomsLogin('admin_zk', 'Admin@123')
    # about()










