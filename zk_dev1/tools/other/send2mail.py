import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "zkuuuuuu@163.com"  # 用户名
mail_pass = "HPTKRCFAVXELKBIZ"  # 口令

sender = 'zkuuuuuu@163.com'
receivers = ['kui.zhang@winicssec.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def send_mail(url, time):
    message = MIMEText(f'自动化测试报告访问URL：{url}', 'plain', 'utf-8')
    message['From'] = Header("AutoImp@163.com", 'utf-8')
    message['To'] = Header("大数据测试组", 'utf-8')

    subject = f'自动化测试报告_{time}'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("----------邮件发送成功--------")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")




