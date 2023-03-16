import pytest
# from zk_dev1.dev_imp.test_api import test_Login, test_fanhua_up_del, test_log_source
from zk_dev1.dev_imp.test_api import test_imp
from zk_dev1.dev_imp.common_tool.logger import GetLog
import allure
write_log = GetLog().get_log()


# test1 = test_Login.TestLogin.Login()
# test2 = test_fanhua_up_del.TestDel.UpDel()
# test3 = test_log_source.Testlogsrc.log_source_Add()
# test4 = test_log_source.Testlogsrc.log_source_Del()

test1 = test_imp.Login()
test2 = test_imp.UpDel()
test3 = test_imp.log_source_Add()
test4 = test_imp.log_source_Del()


@pytest.fixture(scope="session")
def if1no1():
    a = [200, '操作成功']
    return a


@allure.epic('登录页面')
@allure.feature('登录功能')
# @allure.story('')
@allure.severity("normal")
@allure.description('用例描述信息:  登录页面功能验证')
def test_Login(if1no1):
    write_log.info(f"返回结果---：{test1[1]}")
    # allure.attach(f"{test1[1]}", name="log", attachment_type=allure.attachment_type.TEXT)  # 添加网页
    assert test1[0] == if1no1


@pytest.fixture(scope="session")
def if2no1():
    a = [200, '1条数据删除成功！']
    return a


@allure.epic('策略配置')
@allure.feature('范化-列表上方删除功能')
# @allure.story('')
@allure.severity("normal")
@allure.description('用例描述信息: 策略配置-范化-列表上方删除功能')
def test_upDel(if2no1):
    write_log.info(f"返回结果---：{test2[1]}")
    # 添加网页
    # allure.attach(f"{test2[1]}", name="log", attachment_type=allure.attachment_type.TEXT)
    assert test2[0] == if2no1


@pytest.fixture(scope='session')
def if3no1():
    a = [200, '操作成功']
    return a


# 按照模块子模块或功能点子功能点, 对测试用例进行分组
@allure.epic('日志采集')
@allure.feature('日志源管理-列表上方-新增')
# @allure.story('列表上方-新增')
@allure.severity("normal")
@allure.description('用例描述信息:  新增日志源')
def test_logsrcAdd(if3no1):
    # 设置一条测试用例的每个步骤（方法2）
    write_log.info(f"返回结果---：{test3[1]}")
    # allure.attach(f"{test3[1]}", name="log", attachment_type=allure.attachment_type.TEXT)
    assert test3[0] == if3no1


@pytest.fixture(scope='session')
def if3no2():
    a = [200, '操作成功']
    return a


# 按照模块子模块或功能点子功能点, 对测试用例进行分组
@allure.epic('日志采集')
@allure.feature('日志源管理-列表上方-删除')
# @allure.story('列表上方-删除')
@allure.severity("normal")
@allure.description('用例描述信息:  删除日志源')
def test_logsrcDel(if3no2):
    # 设置一条测试用例的每个步骤（方法2）
    write_log.info(f"返回结果：{test4[1]}")
    # allure.attach(f"{test4[1]}", name="log", attachment_type=allure.attachment_type.TEXT)
    assert if3no2 == test4[0]


# if __name__ == '__main__':
#     pytest.main(["-s", '--alluredir', '../report/result', "test_case_imp.py"])
#     # split = 'allure ' + 'generate ' + '/report/result ' + '-o ' + './report/html ' + '-–clean'
#     split = 'allure ' + 'serve ' + '../report/result/'
#     os.system(split)


