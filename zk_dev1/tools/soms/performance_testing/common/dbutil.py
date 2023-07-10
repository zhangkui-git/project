import paramiko
import pymysql

from zk_dev1.tools.soms.performance_testing.common.file_load import load_yaml_file
from zk_dev1.tools.soms.performance_testing.config.config import local_ip, IP, rdp_ip
from zk_dev1.tools.soms.performance_testing.setting import DIR_NAME


class DB:

    def __init__(self, project_name):
        self.dbinfo = load_yaml_file('/config/db.yml')[project_name]
        self.connect = pymysql.connect(
                                host=self.dbinfo['ip'],
                                port=self.dbinfo['port'],
                                user=self.dbinfo['username'],
                                password=self.dbinfo['password'],
                                  charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def select(self, sql):
        cursor = self.connect.cursor()
        cursor.execute(sql) #执行sql
        data = cursor.fetchall() #获取查询得到的数据
        self.connect.commit() #查询也要加，否则一次连接多次查询时会有问题
        cursor.close()
        return data

    def update(self, sql):
        # cursor = self.connect.cursor()
        cursor = self.connect.cursor()
        cursor.execute(sql)
        self.connect.commit()  # 但凡是更新语句都要提交，update/delete/insert
        cursor.close()

    def close(self):
        if self.connect != None:
            self.connect.close()

class Linux():
    """linux操作"""
    def __init__(self):
        self.ssh = paramiko.SSHClient()

    def remoteConnect(self, ip, port, user, pas):
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(ip, port, user, pas, timeout=10)
            print('{}连接成功'.format(ip))
        except Exception as e:
            raise e
            print('{}连接失败'.format(ip))

    def exec_command(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        result2 = stdout.readlines()
        if result2 != []:
            result2 = result2
        else:
            result2 = ''
        return result2

    # def upload(self, src_file, dsc_path):
    #     self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     transport = paramiko.Transport(('ip', '端口号'))
    #     sftp = paramiko.SFTPClient.from_transport('22')
    #     try:
    #         sftp.put(DIR_NAME + src_file, dsc_path + '/' + src_file)
    #         print('上传成功')
    #     except Exception as e:
    #         print(e)
    def upload(self, localpath, remotepath):

        ftp = self.ssh.open_sftp()
        ftp.put(localpath, remotepath)
        print(localpath, remotepath)
        return True

    def download(self, remotepath, localpath):

        ftp = self.ssh.open_sftp()
        ftp.get(remotepath, localpath)
        print(remotepath, localpath)
        return True

    def close(self):
        self.ssh.close()
        print('连接关闭')


if __name__ == '__main__':
    db = DB('database')
    db.update("UPDATE `soms`.`system_config` SET `sys_value`='2880' WHERE  `sys_key`='system_timeout';")    # 修改系统超时时间
    db.update("UPDATE `soms`.`system_config` SET `sys_value`='2880' WHERE  `sys_key`='session_timeout';")    # 修改系统超时时间
    db.update("UPDATE `soms`.`system_config` SET `sys_value`='100' WHERE  `sys_key`='max_login_user';")    # 修改最大并发登录用户数
    rdp_id = db.select(f"select id from soms.soms_asset_info where ip='{rdp_ip}';")  # rdp 192.168.4.119的id
    rdpId = rdp_id[0]['id']
    for i in range(1, 101):   # 新增资产用户 test1-test100   密码 Admin@123
        db.update(f"INSERT INTO `soms`.`soms_asset_user_pwd` (`asset_id`, `username`, `password`, `create_time`, `update_time`, `protocol`) VALUES ('{rdpId}', 'test{i}', '6933921fa54e5ef3b5be8ccb015329b3', '2023-05-23 14:33:44', '2023-05-23 14:33:44', 'RDP');")

    update_time = db.select("select last_update_pwd_time from soms.system_user where user_name='admin'")
    updateTime = update_time[0]['last_update_pwd_time']
    user_name = db.select("select user_name from soms.system_user")
    users = [user['user_name'] for user in user_name]
    user_password = db.select("select password from soms.system_user where user_name='admin'")
    user_password = user_password[0]['password']
    salt = db.select("select salt from soms.system_user where user_name='admin'")
    salt = salt[0]['salt']
    for i in range(1, 61):  # 新增operator账户 op1-op60 密码 wnt8000LLy&y
        if f'op{i}' not in users:
            db.update(
                f"INSERT INTO `soms`.`system_user` (`user_name`, `real_name`, `password`, `salt`, `telephone`, `email`, `department`, `position`, `role_id`, `create_type`, `create_time`, `last_update_pwd_time`) VALUES ('op{i}', '', '{user_password}', '{salt}', '', '', '', '', '2', '1', '{updateTime}', '{updateTime}');")
    db.close()

    print("执行完成...")


