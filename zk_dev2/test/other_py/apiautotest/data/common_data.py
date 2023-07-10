'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/2/23 11:39
software: PyCharm
'''
import datetime

admin = 'admin'
audit = 'audit'
username = 'op1'
personal_username = 'tym'
password = 'Admin@123'
field = '@123ni好，！@#￥都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清你哦按什么难度就弄完你都去弄清'
small_field = 'usernameusernameusernameusernameusernameusernameusernameusername'  # 64字符
today = str(datetime.datetime.now())[:10] + ' 00:00:00'
last_week = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")