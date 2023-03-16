import os
import pytest
from common_tool.makezip_ssh import make_zip, sshzk, com_time, get_url
from common_tool.send_mail import send_mail

if __name__ == '__main__':
    # pytest.main(["-s", '--alluredir', f'report/result{com_time}', "./test_case/test_case_ui.py"])
    pytest.main(["-s", '--alluredir', f'report/result{com_time}', "./test_api/test_login.py"])
    split = 'allure ' + 'generate ' + '-–clean ' + f'./report/result{com_time} ' + '-o ' + f'./report/result{com_time}/html'
    os.system(split)
    make_zip()
    sshzk()
    print('UI测试报告URL：', get_url)
    send_mail(get_url, com_time)



