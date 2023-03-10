import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.qiye.163.com"  # 设置服务器
mail_user = "kui.zhang@winicssec.com"  # 用户名
mail_pass = "KrCqLpKHbYNduL8U"  # 口令

sender = "kui.zhang@winicssec.com"
receivers = ['kui.zhang@winicssec.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def send_mail(url, time1):
    # 邮件附带资源的模式
    buildup = MIMEMultipart('related')
    # 邮件主题
    subject_content = "接口自动化测试报告_{}".format(time1)
    # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
    buildup["From"] = "<kui.zhang@winicssec.com>"
    # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
    buildup["To"] = "<kui.zhang@winicssec.com>"
    # 设置邮件主题
    buildup["Subject"] = Header(subject_content, 'utf-8')
    # 邮件正文内容
    body_text = f"Hi，all\n接口自动化报告访问地址：{url}"
    # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
    message_text = MIMEText(body_text, "plain", "utf-8")
    # 向MIMEMultipart对象中添加文本对象
    buildup.attach(message_text)
    # # 构造附件
    # atta = MIMEText(open(DIR_NAME + '/report/html/index.html', 'rb').read(), 'html', 'utf-8')
    # # 设置附件信息
    # atta["Content-Disposition"] = 'attachment; filename="index.html"'
    # # 添加附件到邮件信息当中去
    # buildup.attach(atta)
    try:
        # 创建SMTP对象
        stp = smtplib.SMTP_SSL(mail_host)
        # 设置发件人邮箱的域名和端口，端口地址为465
        stp.connect(mail_host, 465)
        # set_debuglevel(1)可以打印出和SMTP服务器交互的所有信息
        # stp.set_debuglevel(1)
        # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
        stp.login(mail_user, mail_pass)
        # 发送邮件，传递参数1：发件人邮箱地址，参数2：收件人邮箱地址，参数3：把邮件内容格式改为str
        stp.sendmail(sender, receivers, buildup.as_string())
        print("邮件发送成功")
        # 关闭SMTP对象
        stp.quit()
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


# if __name__ == '__main__':
#     url = 111111111
#     time1 = '20220811201411'
#     send_mail(url, time1)

