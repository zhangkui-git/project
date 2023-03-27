#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : 2022/5/20 14:51
# @Author : 卫运腾
import paramiko
import pymysql
from config import IP

def get_conn():
    '''目前只将IP进行了参数化，'''

    conn = pymysql.connect(host=IP, user = 'root' # 用户名
                           ,passwd='Wnt.1@3456' # 密码
                           ,port= 3306 # 端口，默认为3306
                           ,db='soc' # 数据库名称
                           ,charset='utf8')
    return conn

def update(sql):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()



def con_linux(hostname=IP, username='root', psd='Wnt.1@3456', sql=''):
    s = paramiko.SSHClient()
    #取消安全认证
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #连接linux
    s.connect(hostname=hostname,username=username,password=psd)
    #执行命令
    stdin,stdout,stderr=s.exec_command('systemctl status firewalld')
    #读取执行结果
    result = stdout.read().decode('UTF-8')

    #判断结果是否存在某个字段
    if result.find('active (running)') > 0:
        print('防火墙是打开状态,为了执行sql，暂时关闭防火墙')
        s.exec_command('systemctl stop firewalld')
        from time import sleep
        sleep(1)
        update(sql)
        # s.exec_command('systemctl start firewalld') #更新成功后，打开防火墙
        # print('成功执行完了update语句')

    elif result.find('inactive (dead)') > 0: #如果防火墙状态时关闭状态，直接执行update sql语句
        print('防火墙是关闭状态, 直接执行sql语句')
        update(sql)
        # s.exec_command('systemctl start firewalld')#更新成功后，打开防火墙
        # print('成功执行完了update语句')

    else:
        print('未知状态，需要检查linux机器状态')

    #关闭linux
    s.close()
    #返回执行结果
    #print(result)



if __name__ == '__main__':

    print(con_linux('192.168.100.63', 'root', 'Wnt.1@3456'))





