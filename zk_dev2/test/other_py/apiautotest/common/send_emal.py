'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/1/22 16:51
software: PyCharm
'''
import datetime
import os
import shutil
import smtplib
import time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from api.login_api import about
from config.config import *

from setting import DIR_NAME


class SendEmail:
    def __init__(self, path):
        self.mm = MIMEMultipart('related')
        # 邮件主题
        name, version = about()
        self.tm = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.subject_content = "{}{}自动化测试报告".format(name, version) + "_" + self.tm
        # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
        self.mm["From"] = "<yumeng.tian@winicssec.com>"
        # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
        self.mm[
            "To"] = "<hlyu@winicssec.com>,<myzhang@winicssec.com>,<yanting.chen@winicssec.com>,<yumeng.tian@winicssec.com>,<gaibei.liu@winicssec.com>,<lili.shi@winicssec.com>,<yunteng.wei@winicssec.com>,<lemin.zheng@winicssec.com>,<xubo.mu@winicssec.com>,<kui.zhang@winicssec.com>"
        # 设置邮件主题
        self.mm["Subject"] = Header(self.subject_content, 'utf-8')
        # 邮件正文内容
        # body_content = "Hi，all\nLAA&ISA自动化测试报告见如下地址: http://{}:8080/report/index.html".format(local_ip)
        body_content = "Hi，all\n{}{}接口自动化测试报告见如下地址: http://{}:8080/{}/report/html/index.html".format(name, version,
                                                                                                     local_ip, path)
        # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
        message_text = MIMEText(body_content, "plain", "utf-8")
        # 向MIMEMultipart对象中添加文本对象
        self.mm.attach(message_text)

        # # 构造附件
        # self.atta = MIMEText(open(DIR_NAME + '/report/html/index.html', 'rb').read(), 'html', 'utf-8')
        # # 设置附件信息
        # self.atta["Content-Disposition"] = 'attachment; filename="index.html"'
        # # 添加附件到邮件信息当中去
        # self.mm.attach(self.atta)

    def send_email(self):
        try:
            # 创建SMTP对象
            stp = smtplib.SMTP_SSL()
            # 设置发件人邮箱的域名和端口，端口地址为465
            stp.connect(mail_host, port)
            # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
            # stp.set_debuglevel(1)
            # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
            stp.login(mail_sender, mail_license)
            # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
            stp.sendmail(mail_sender, mail_receivers, self.mm.as_string())
            print("邮件发送成功")
        except Exception as e:
            print(e)
            print("发送失败")

        finally:
            # 关闭SMTP对象
            stp.quit()


def move_file(source, target):
    """ 报告复制到tomcat下 """
    source_path = os.path.abspath(DIR_NAME + source)
    target_path = os.path.abspath(target)

    if not os.path.exists(target_path):
        # 如果目标路径不存在原文件夹的话就创建
        os.makedirs(target_path)

    if os.path.exists(source_path):
        # 如果目标路径存在原文件夹的话就先删除
        shutil.rmtree(target_path)

    shutil.copytree(source_path, target_path)
    print('复制到tomcat成功!')


if __name__ == '__main__':
    time1 = datetime.datetime.now().strftime('%Y%m%d%H%M')
    move_file('//report/', 'D:\\apache-tomcat-8.5.20-8440\\webapps\\{}\\report'.format(time1))
    SendEmail(time1).send_email()
