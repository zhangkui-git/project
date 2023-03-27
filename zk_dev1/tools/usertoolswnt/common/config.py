'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/3/11 12:19
software: PyCharm
'''

IP = "192.168.4.153"  # 服务器地址
host = f"https://{IP}:8440"
admin = 'admin' #初始用户名
operator = 'operator'  #默认operator用户名
password = 'wnt8000LLy&y'  # 默认账号的密码
# password = 'Admin@123456'  # 默认账号的密码
password_new = 'Admin@123456' #新建所有账户后，设置的统一密码
role_name = ['operator', 'audit', 'admin', 'operator_p']  # 角色
# role_name = ['operator', 'audit', 'admin']  # 角色
# role_name = ['audit']  # 角色
# user_name = ['cyt', 'sll', 'zt', 'whl',  'zlm', 'zk', 'hsq', 'xrg', 'ws']  # 测试人员名字
user_name = ['zk']  # 测试人员名字


