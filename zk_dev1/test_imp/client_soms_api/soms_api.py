from client import *
from zk_dev1.test_imp.common_soms_tool.SM4_CBC import *


class SomsLogin(RequestsClient):
    def __init__(self, user, pas):
        RequestsClient.__init__(self)
        self.url = host + "/login/userLogin"
        self.method = 'post'
        user = SM4Utils().encryptData_CBC(bytes(user, "UTF-8"))
        pas = SM4Utils().encryptData_CBC(bytes(pas, "UTF-8"))
        self.json = {"userName": f"{user}", "password": f"{pas}"}