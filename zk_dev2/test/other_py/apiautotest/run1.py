import datetime
import os
import time

import pytest

from common.send_emal import move_file, SendEmail

if __name__ == '__main__':
    # 执行时会按照pytest.ini这个配置所配的相关信息进行执行
    pytest.main(["-s", '--alluredir', f'report/result11', "./testcases/test_isa/test_v2r6/test_smoke_v2r6_1.py"])

