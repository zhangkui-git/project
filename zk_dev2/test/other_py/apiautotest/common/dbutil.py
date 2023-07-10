import paramiko
import pymysql

from zk_dev2.test.other_py.apiautotest.common.file_load import load_yaml_file


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
            return result2
        else:
            return ''
    # def upload(self, src_file, dsc_path):
    #     self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #     transport = paramiko.Transport(('ip', '端口号'))
    #     sftp = paramiko.SFTPClient.from_transport('22')
    #     try:
    #         sftp.put(DIR_NAME + src_file, dsc_path + '/' + src_file)
    #         print('上传成功')
    #     except Exception as e:
    #         print(e)
    def upload(self, inpath,outpath):

        ftp = self.ssh.open_sftp()
        ftp.put(inpath, outpath)
        print(inpath, outpath)
        return True


    def close(self):
        self.ssh.close()
        print('连接关闭')

if __name__ == '__main__':
    db = DB('database')
    print(db.select("select id from soc.soc_asset_info where ip in ('192.168.56.77','192.168.56.78','192.168.56.79')"))
    db.connect.close()
    n = [{'id': 18}, {'id': 19}, {'id': 20}]
    # for i in n:
    #     print(i.values())
    nlist = [id['id'] for id in n]
    print(nlist)
