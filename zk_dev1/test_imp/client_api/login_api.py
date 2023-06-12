from zk_dev1.test_imp.common_tool.SM4_CBC import *
from client import *


class SomsLogin(RequestsClient):
    def __init__(self, user, pas):
        print(111, user, pas)
        RequestsClient.__init__(self)
        self.url = host + "/login/userLogin"
        self.method = 'post'
        user = SM4Utils().encryptData_CBC(bytes(user, "UTF-8"))
        pas = SM4Utils().encryptData_CBC(bytes(pas, "UTF-8"))
        self.json = {"userName": f"{user}", "password": f"{pas}"}


if __name__ == '__main__':
    SomsLogin('admin_zk1', 'Admin@123').send()
