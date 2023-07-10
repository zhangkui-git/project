import datetime
import os
import time

import pytest

from common.send_emal import move_file, SendEmail

if __name__ == '__main__':
    # 执行时会按照pytest.ini这个配置所配的相关信息进行执行
    pytest.main()
    os.system('allure generate ./report/shop -o ./report/html --clean')

    time.sleep(3)
    file = datetime.datetime.now().strftime('%Y%m%d%H%M')
    move_file('/report/', 'D:\\apache-tomcat-8.5.20-8440\\webapps\\{}\\report'.format(file))  # 报告复制到tomcat下

    # time.sleep(3)
    # SendEmail(file).send_email()  # 发送邮件
