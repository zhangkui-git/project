
import pytest
import allure
import os

print(os.getcwd())

# 设置一条测试用例的每个步骤（方法1）
@allure.step("测试第一步")
def step_1():
    pass



# 按照模块子模块或功能点子功能点, 对测试用例进行分组
@allure.epic('后台管理模块')
@allure.feature('登录功能点')
@allure.story('正常登录')
# @allure.title('测试登录: 登录成功')
@pytest.fixture(scope='module')
def step_2():
    return 123
def test_a(step_2):
    # 设置一条测试用例的每个步骤（方法2）
    with allure.step("测试第一步"):
        pass
    with allure.step("测试第二步"):
        assert step_2 == 2
    with allure.step("测试第三步"):
        pass

@allure.epic('后台管理模块')
@allure.feature('登录功能点')
@allure.story('用户名错误登录')
@allure.issue('http://127.0.0.1:80/zantaopms/')
@allure.testcase('http://www.baidu.com/')
# 设置测试用例的标签, 可以设置多个
@allure.tag("回归测试", "重要")
# 设置测试用例的级别  blocker > critical > normal > minor > trivial
@allure.title('测试登录:用户名错误')
@allure.description('测试登录:测试用例描述信息')
@allure.severity("blocker")
@pytest.fixture(scope="module")
def step_3():
    zk1 = 12
    return zk1
def test_b1(step_3):
    assert step_3 == 12



@allure.epic('后台管理模块')
@allure.feature('商品管理')
def test_c():
    assert 1 == 1
def test_d():
    assert 1 == 2
def test_e():
    assert 1 == 2


# pytest.main() 相当于执行pytest命令


if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', 'report/result', 'testome.py'])
    print(1111111)
    split = 'allure ' + 'serve ' + os.path.join(os.path.abspath('./report'), 'result')
    os.system(split)


