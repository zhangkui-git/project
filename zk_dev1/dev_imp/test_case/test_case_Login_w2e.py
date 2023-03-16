# import pytest
# import os
from dev_imp.test_api.test_Login import TestLogin
from dev_imp.test_config.config import url, headers, body
import allure
import openpyxl

test1 = TestLogin().Login(url, headers, body)


@allure.tag("回归测试", "重要")
# 设置测试用例的级别  blocker > critical > normal > minor > trivial
@allure.title('测试登录')
@allure.description('测试用例描述信息: 测试登录')
@allure.severity("blocker")
class TestClass(object):
    def testLogin(self):
        aa = [200, '操作成功']
        # assert test1 == aa
        get_excel = openpyxl.load_workbook(r"D:\MyInfo_file\python_t\Allure_Report.xlsx")
        sheet = get_excel['Sheet1']
        if test1 == aa:
            data = ['登录接口', '回归测试', 'normal', 'PASS']
        else:
            data = ['登录接口', '回归测试', 'normal', 'NOT PASS']
        sheet.append(data)
        get_excel.save(r"D:\MyInfo_file\python_t\Allure_Report.xlsx")


# if __name__ == '__main__':
#     pytest.main(["-s", '--alluredir', 'report/result', "test_case_Login_w2e.py"])
#     # split = 'allure ' + 'generate ' + '/report/result ' + '-o ' + './report/html ' + '-–clean'
#     split = 'allure ' + 'serve ' + './report/result/'
#     os.system(split)


