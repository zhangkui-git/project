'''
author:tianyumeng
contact: yumeng.tian@winicssec.com
datetime:2022/4/13 14:59
software: PyCharm
'''
from zk_dev2.test.other_py.apiautotest.api.base_api import BaseApi
from zk_dev2.test.other_py.apiautotest.config.config import host


class DisableEnableUser(BaseApi):
    """ 禁用启用账户"""

    def __init__(self, id):
        BaseApi.__init__(self)
        self.url = host + '/userpermission/usermanage/batch'
        self.method = 'post'
        self.params = {
            'id': id
        }

    def getdata(self):
        print(self.headers)


class SshConnect(BaseApi):
    """ 远程连接服务配置 """

    def __init__(self, isopen=True):
        BaseApi.__init__(self)
        self.url = host + '/sysconfig/editSshdManage/'
        self.method = 'post'
        self.params = {
            'isopen': isopen
        }


class SnmpTrapAdd(BaseApi):
    """ SMNP TRAP新增 """

    def __init__(self, ip='192.168.100.89', port=162, community='test', status=0, type=1, protocol=1):
        BaseApi.__init__(self)
        self.url = host + '/snmpTrapConfig/save'
        self.method = 'post'
        self.json = {"ip": ip, "port": port, "version": 1, "community": community, "status": status, 'type': type,
                     "protocol": protocol}


class SnmpTrapDelete(BaseApi):
    """ SMNP TRAP删除 """

    def __init__(self, id):
        BaseApi.__init__(self)
        self.url = host + '/snmpTrapConfig/delete/batch'
        self.method = 'delete'
        self.json = {"ids": id}


class SnmpTrapQuery(BaseApi):
    """ SMNP TRAP查询 """

    def __init__(self, ip):
        BaseApi.__init__(self)
        self.url = host + '/snmpTrapConfig/list'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "ip": ip}


class Iec104Edit(BaseApi):
    """ iec104更新 """

    def __init__(self, ip, port=2404, iec104ServerMaxConnect=5, status='on'):
        BaseApi.__init__(self)
        self.url = host + '/iec104/update'
        self.method = 'post'
        self.json = {"iec104ServerPort": port, "iec104ServerIpScope": ip,
                     "iec104ServerMaxConnect": iec104ServerMaxConnect,
                     "iec104ServerStatus": status}


class DataBackupSave(BaseApi):
    """ 保存数据备份 """

    def __init__(self, dataType='mysql'):
        BaseApi.__init__(self)
        self.url = host + '/dataBackup/saveBaseConfig'
        self.method = 'post'
        self.json = {"id": 1, "snapshotRepoName": "repo_20220416094240", "transferRate": 20, "dataType": dataType,
                     "remotePath": '', "uid": "1039", "gid": "1039", "pathType": "local", "status": "success",
                     "isESRestart": 'false'}


class FullBackup(BaseApi):
    """ 全量备份 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/dataBackup/backupData/all'
        self.method = 'post'


class BackupQuery(BaseApi):
    """ 查看备份列表 """

    def __init__(self):
        BaseApi.__init__(self)
        self.url = host + '/dataBackup/list'
        self.method = 'post'
        self.json = {"startPage": 1, "pageSize": 10, "taskName": "", "pathType": "", "status": "",
                     "createTimeStart": "", "createTimeEnd": ""}


if __name__ == '__main__':
    DisableEnableUser(BaseApi).getdata()