import pytest
import os


if __name__ == '__main__':
    pytest.main(["-s", '--alluredir', 'report/result', "./test_case/test_case_Login_w2e.py"])
    # split = 'allure ' + 'generate ' + '-–clean ' + './report/result ' + '-o ' + f'./report/result{com_time}/html'
    # # split = 'allure ' + 'serve ' + os.path.join(os.path.abspath('./report'), 'result')
    # os.system(split)




