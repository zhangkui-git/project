from zk_dev1.test_imp.common_soms_tool.SM4_CBC import *
from client import *


def SomsLogin():
    url = host + "/login/userLogin"
    user = SM4Utils().encryptData_CBC(bytes(username, "UTF-8"))
    pas = SM4Utils().encryptData_CBC(bytes(password, "UTF-8"))
    body = {"userName": f"{user}", "password": f"{pas}"}
    res = requests.post(url=url, json=body, verify=False)
    print(res.json())


def about():
    url = host + '/systeminfo/detail'
    res = requests.get(url=url, verify=False)
    print(res.json())


if __name__ == '__main__':
    SomsLogin()
    about()










