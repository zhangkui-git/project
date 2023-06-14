import pytest
import allure
from zk_dev1.test_imp.client_soms_api.soms_api import *
write_log = GetLogger().get_logger()


@allure.feature('堡垒机冒烟测试')
class Test_Soms_Smoke(object):

    @allure.story('登录')
    @allure.title('soms-1')
    def test_Login(self):
        res = Soms_Login('admin_zk1', 'Admin@123').send()
        pytest.assume(res.json()['statusCode'] == 200)

    @allure.story('新增用户')
    @allure.title('soms-2')
    def test_Add_user(self):
        res = Soms_AddUser().send()
        print(1111111111111, res.json()['statusCode'])
        # pytest.assume(res.json()['statusCode'] == 200)

    @allure.story('新增规则')
    @allure.title('soms-3')
    def test_Add_Role(self):
        res = Soms_AddRole().send()
        pytest.assume(res.json()['statusCode'] == 200)

    @allure.story('删除用户')
    @allure.title('soms-4')
    def test_Del_User(self):
        res = Soms_DelUser().send()
        pytest.assume(res.json()['statusCode'] == 200)


if __name__ == '__main__':
    # test_Soms_Smoke().test_adduser()
    print("--------测试完成--------")











