
from zk_dev1.test_imp.client_soms_api.base_api import *
from zk_dev1.test_imp.client_soms_api.soms_json_data import *
from zk_dev1.test_imp.common_soms_tool.s_mysql import *
write_log = GetLogger().get_logger()


class Soms_Login(RequestsClient):
    # 登录接口
    def __init__(self, user, pas):
        RequestsClient.__init__(self)
        self.url = host + "/login/userLogin"
        self.method = 'post'
        user1 = SM4Utils().encryptData_CBC(bytes(user, "UTF-8"))
        pas1 = SM4Utils().encryptData_CBC(bytes(pas, "UTF-8"))
        self.json = {"userName": f"{user1}", "password": f"{pas1}"}


class Soms_AddUser(BaseApi):
    # 新增用户
    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/userpermission/usermanage/addUser'
        self.method = 'post'
        self.json = add_user


class Soms_AddRole(BaseApi):
    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/userpermission/rolemanage/add'
        self.method = 'post'
        self.json = user_role


class Soms_DelUser(BaseApi):
    # 删除用户
    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/userpermission/usermanage/delete'
        self.method = 'delete'
        del_user_id = select('select id from system_user where user_name = "a11"')[0]['id']
        self.json = {'ids': [del_user_id]}


if __name__ == '__main__':
    # Soms_Login('admin_zk', 'Admin@123').send()
    Soms_AddUser().send()
    # Soms_DelUser().send()





































































































