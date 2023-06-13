import pytest
import os

from common_tool.makezip_ssh import make_zip, sshzk, com_time, get_url
from common_tool.send_mail import send_mail


if __name__ == '__main__':
    # pytest.main(["-s", '--alluredir', f'report/result{com_time}', "./test_case/test_soms_case.py"])
    pytest.main(["-s", '--alluredir', f'report/result{com_time}', "./end_py/test_soms_case.py"])
    split = 'allure ' + 'generate ' + '-–clean ' + f'./report/result{com_time} ' + '-o ' + f'./report/result{com_time}/html'
    # split = 'allure ' + 'serve ' + os.path.join(os.path.abspath('./report'), 'result')
    os.system(split)
    make_zip()
    sshzk()
    send_mail(get_url, com_time)
    # print("测试报告连接：", get_url)




