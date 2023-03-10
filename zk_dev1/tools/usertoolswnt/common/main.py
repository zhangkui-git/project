'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/3/10 11:07
software: PyCharm
'''
import time
import os
import requests
import urllib3
from config import host, admin, operator, password, role_name, user_name, password_new
from encry_decry import RsaEncrypt
from encry_decry import generate_public_rsa
from add_admin import *
import winreg  # 和注册表交互，获取chrom浏览器的版本号
DIR_NAME = os.path.dirname(os.getcwd())


def get_chrome_version():
    """
    通过windows注册表获取chrome版本号
    :return: 版本号（str）
    """
    # 从注册表中获得版本号
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    _v, _type = winreg.QueryValueEx(key, 'version')
    return _v  # 返回版本号

chrome_version = get_chrome_version()


def login(name, pwd, chrome_version=chrome_version):
    """
    用户登录接口
    param name:用户名
    param pwd:密码
    """
    url = host + '/login/userLogin'
    user = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(name)  # 加密后的用户名
    pas = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(pwd)  # 加密后的密码
    ua = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Safari/537.36'

    json_a = {"userName": user, "userPassword": pas}
    headers_login = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': ua,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    #如果后面的接口请求都加上头的话，那么登录接口的请求头参数也必须要加上
    resp = requests.post(url=url,  json=json_a, headers=headers_login, verify=False)

    result = resp.json()

    header = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Authorization':result["data"]["accessToken"],
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': ua,
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    # print(type(header))
    return header

def user_created(header, user_describ, name, pwd):
    """
    创建用户
    header: 登录header
    user_describ: 用户描述
    name: 用户名
    pwd: 密码
    """
    url = host + '/userpermission/usermanage/addUser'
    user = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(name)  # 加密后的用户名
    pas = RsaEncrypt(DIR_NAME + '/common/public_key.keystore').encrypt_data(pwd)  # 加密后的密码
    if user_describ == 'operator':  # 判断角色id值为2，用户描述为'operator'，值为3用户描述为'audit'
        roleId = 2
    elif user_describ == 'audit':
        roleId = 3
    elif user_describ == 'admin':
        roleId = 2
    elif user_describ == 'operator_p':
        roleId = 4

    else:
        print('输入的roleId值错误')
        raise Exception
    json_u = {
        "userName": user,
        "userPassword": pas,
        "roleId": roleId, "userDescription": user_describ}

    requests.post(url=url, json=json_u, headers=header, verify=False)


def confirm_ssh(header):
    '''判断ssh开关的状态'''
    ssh_url = host + '/sysconfig/sshdStatus'
    resp = requests.get(url=ssh_url, headers=header, verify=False)
    return resp.json()['data']['status']

def open_ssh(header):
    '''打开ssh开关'''
    ssh_url = host + '/sysconfig/editSshdManage/?isopen=true'
    json_data = {
        'isopen': 'true'
    }
    requests.post(url=ssh_url, json=json_data, headers=header, verify=False)

def close_ssh(header):
    '''关闭ssh开关'''
    ssh_url = host + '/sysconfig/editSshdManage/?isopen=false'
    json_data = {
        'isopen': 'false'
    }
    requests.post(url=ssh_url, json=json_data, headers=header, verify=False)


def open_fire(IP):
    # 创建SSH 连接客户端
    s = paramiko.SSHClient()
    # 取消安全认证
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接linux
    s.connect(hostname=IP, username='root', password='Wnt.1@34568')
    s.exec_command('systemctl start firewalld')   # 执行结束后，打开防火墙
    time.sleep(1)


def main():
    '''将执行过程封装'''
    generate_public_rsa()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 取消ssl安全提示
    header = login(admin, password)  # admin登录返回header
    user_list = []  # 所有用户列表
    for role in role_name:  # 遍历角色
        for user in user_name:  # 遍历测试组名字
            userName = '{}_{}'.format(role, user)  # 平台用户名 例如： operator_cyt
            user_created(header=header, user_describ=role, name=userName, pwd=password_new)
            user_list.append(userName)
    operator_header = login(operator, password) #获取operator账户的header
    status = confirm_ssh(operator_header)  #判断ssh开关是否打开

    print('ssh开关是否打开？on为开，false为关闭', status)
    if status == 'off':
        '''需要打开ssh开关'''
        open_ssh(operator_header)
        time.sleep(2)
        #按照内置账户"admin_"的表字段值，将admin开头的账号对应的字段值都进行修改，使之变成admin权限的账户
        for user1 in user_name:
            sql = f'UPDATE soc_user_info SET role_id = 1, delete_flag = 0, disable_flag = 0, disable_state = 0 WHERE user_name = "admin_{user1}";' #
            # sql = f'UPDATE soc_user_info SET role_id = 1, disable_flag = 0, disable_state = 0 WHERE user_name = "admin_{user1}";' #
            con_linux(sql=sql)
            time.sleep(0.5)
            print(f'成功执行update语句，修改用户admin_{user1}为admin权限')
        open_fire(IP)
        close_ssh(operator_header)
    else:
        for user2 in user_name:
            sql = f'UPDATE soc_user_info SET role_id = 1, delete_flag = 0, disable_flag = 0, disable_state = 0 WHERE user_name = "admin_{user2}";' #
            # sql = f'UPDATE soc_user_info SET role_id = 1, disable_flag = 0, disable_state = 0 WHERE user_name = "admin_{user2}";' #
            con_linux(sql=sql)
            time.sleep(0.5)
            print(f'成功执行update语句，修改用户admin_{user2}为admin权限')
        open_fire(IP)
    print('执行结束，已经打开了防火墙，已添加的账号：', user_list)  # 打印添加的用户名


if __name__ == '__main__':
    main()



