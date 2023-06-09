import logging
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from log2file import *

# 第三方 SMTP 服务
mail_host = "smtp.qiye.163.com"  # 设置服务器
mail_user = "kui.zhang@winicssec.com"  # 用户名
mail_pass = "zbYhpA53QmArUdGZ"  # 口令

sender = "kui.zhang@winicssec.com"
receivers = ['kui.zhang@winicssec.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


def sendmail(product, version, host, mem, time1, speed, py_send_sum, sys_sum, es_lost_sum, speed1):
    py_send_lost = round((py_send_sum - sys_sum) / py_send_sum, 5)
    py_send_lost_res = '{:.3%}'.format(py_send_lost)
    # sys_lost = round(es_lost_sum / sys_sum, 5)
    sys_lost = round(es_lost_sum / py_send_sum, 5)
    sys_lost_res = '{:.3%}'.format(sys_lost)
    if float(sys_lost_res[:-1]) <= 3:
        res = f"{product}的{version}版本{time1}H_{mem}_{speed}EPS的规格性能测试结果达标，通过"
    else:
        res = f"{product}的{version}版本{time1}H_{mem}_{speed}EPS的规格性能测试结果未达标，未通过"
    # 邮件附带资源的模式
    buildup = MIMEMultipart('related')
    # 邮件主题
    subject_content = f"{product}的{version}版本{time1}H_{mem}_{speed}EPS的性能测试报告"
    # 设置发送者,注意严格遵守格式,里面邮箱为发件人邮箱
    buildup["From"] = "<kui.zhang@winicssec.com>"
    # 设置接受者,注意严格遵守格式,里面邮箱为接受者邮箱
    buildup["To"] = "<kui.zhang@winicssec.com>"
    # 设置邮件主题
    buildup["Subject"] = Header(subject_content, 'utf-8')
    # 邮件正文内容
    body_text = f'''
    <p style="font-size:20px; color:red">Hi, 性能测试已完成，详细数据如下:</p>
    <hr style="border-color:black; height: 3px"><br>
    <table border="1" cellspacing="0">
        <tr bgcolor="#D6D6AD">
            <th style="font-size:15px; color:blue; width: 160px">产品名称</th>
            <th style="font-size:15px; color:blue; width: 190px">版本号</th>
            <th style="font-size:15px; color:blue; width: 160px">服务器</th>
            <th style="font-size:15px; color:blue; width: 60px">内存</th>
            <th style="font-size:15px; color:blue; width: 60px">时间</th>
            <th style="font-size:15px; color:blue; width: 90px">规格速率</th>
            <th style="font-size:15px; color:blue; width: 127px">脚本打日志总数</th>
            <th style="font-size:15px; color:blue; width: 127px">系统收日志总数</th>
            <th style="font-size:15px; color:blue; width: 127px">系统丢日志总数</th>
            <th style="font-size:15px; color:blue; width: 127px">实际丢日志总数</th>
            <th style="font-size:15px; color:blue; width: 100px">实际丢失率</th>
            <th style="font-size:15px; color:blue; width: 100px">系统丢失率</th>
            <th style="font-size:15px; color:blue; width: 150px">实际平均速率</th>
        </tr>
        <tr style="height: 40px">
            <th>{product}</th>
            <th>{version}</th>
            <th>{host}</th>
            <th>{mem}</th>
            <th>{time1}H</th>
            <th>{speed}EPS</th>
            <th>{py_send_sum}</th>
            <th>{sys_sum}</th>
            <th>{es_lost_sum}</th>
            <th>{py_send_sum - sys_sum}</th>
            <th>{py_send_lost_res}</th>
            <th>{sys_lost_res}</th>
            <th>{speed1}EPS</th>
        </tr>
    </table>
    <br><hr style="border-color:black; height: 3px">
    <p style="font-size:20px; color:red">测试结果如下:</p>
    <p style="font-size:15px; color:black">{res}</p> 
    '''
    # 构造文本,参数1：正文内容，参数2：文本格式，参数3：编码方式
    message_text = MIMEText(body_text, "html", "utf-8")
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
        logging.info("邮件发送成功")
        print("邮件发送成功")
        # 关闭SMTP对象
        stp.quit()
    except smtplib.SMTPException:
        logging.info("Error: 无法发送邮件")
        print("Error: 无法发送邮件")


if __name__ == '__main__':
    product = "日志审计与分析系统"
    version = 'V100R007C01B070'
    host = "192.168.4.152"
    mem = 4
    time1 = 5
    speed = 6
    count = 7
    sys_sum = 8
    es_lost_sum = 9
    avg = 10
    sendmail(product, version, host, mem, time1, speed, count, sys_sum, es_lost_sum, avg)


