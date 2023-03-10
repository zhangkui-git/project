import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg_from = '161503323@qq.com'
msg_from_pwd = 'htupqnttmcatcaec'
msg_to = ['kui.zhang@winicssec.com']

msg = MIMEMultipart()
con_text = '11111111'
msg.attach(MIMEText(con_text, 'plain', 'utf-8'))

subject = 'Python SMTP 邮件测试'
msg['Subject'] = subject
msg['From'] = "菜鸟教程"
msg['To'] = "测试"

s = smtplib.SMTP_SSL('smtp.qq.com', 465)
s.login(msg_from, msg_from_pwd)
s.sendmail(msg_from, msg_to, msg.as_string())
print("邮件发送成功")