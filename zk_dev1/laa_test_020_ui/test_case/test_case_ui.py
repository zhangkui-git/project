import pytest
# import os
from dev_ui.test_api import test_login
import allure

test1 = test_login.test_C001001()


@pytest.fixture(scope="session")
def if2no1():
    a = '用户名不能为空'
    return a


@allure.epic('登录页面')
@allure.feature('用户名为空')
@allure.title('测试登录')
@allure.tag("回  归   测   试")
@allure.description('用例描述信息: 测试用户名为空登录')
# 设置测试用例的级别  blocker > critical > normal > minor > trivial
@allure.severity("normal")
def testLogin(if2no1):
    # 添加网页
    allure.attach(f"{test1}", name="log", attachment_type=allure.attachment_type.TEXT)
    assert test1 == if2no1
