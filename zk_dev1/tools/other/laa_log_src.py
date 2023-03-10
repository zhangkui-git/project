import requests
import pymysql as mysql
import pandas as pd
import time
common_url = "https://192.168.4.154:8440"


class Test1(object):
    def login():
        login_url = f"{common_url}/login/userLogin"
        login_headers = {"Content-Type": "application/json"}
        login_body = {"userName":"IgkDoFihpl4xEL+tPRz1VgHvez6/7EORy9hFEYXHadi7cifFusX1lyJMEjCtgs7YxCqvtQmJ5djgwbychc0/SQTl2eve7P4HhM9M/vHC0MkVu+n6XPWwTgVOs6tTaa/22fX/FepFHwb4/DAQ+b+EaNO9+DsBR6xDwb+xjAMvf+0WVqf3qNh8fzr+1QMGopg9jIErFmX2qwzGB73bjv+iWe2WiOW7jcVb8hNuzfw0fm2pyhG9Ha6sNk/V3umf5P42aosSXJLK0IzF9BRyK09EjgSES8W3SJgyDwvKB+4mBX7LO0/hJs71+jCz9qw80ZtyYpQGWaf8XWFoN/uPCJgSDQ==","userPassword":"tUNcuBetcE4bcLWnSj5aAdEaH7xmjmfMfqjB0NLxIQyyqQurntpjK2OWiBwAVoy2n6MhxKEvUYzfsixvZFm5IYPdjzVGPeUr+zpm4yGQW/9Yl1WmJlftefPSWOJd1MNT7yPnshPBY8tORchvL5TxeTeTfPdnYc/oOzmlYsqdLzr3ymGCsvLvfAJY4J6+HQIA86BUkZU/4Xx6galocT9eECUWu5p4k9BKmmKLTaRR9YyFaqahlwC3uRv+KvI/l31Hu2fLWrSAKXl+ibLlhpOg836m0ys4LZg9izZEGP+gyzPi8vG/wsb8xTLSpBZk6hc0iyNeqaOHmQgquYPQhArtiw=="}
        res = requests.post(url=login_url, headers=login_headers, json=login_body, verify=False)
        res1 = res.json()
        token1 = res1["data"]["accessToken"]
        return token1
        print(token1)

    def logsrc_add(num):
        token1 = Test1.login()
        add_url = f"{common_url}/log/source/add"
        add_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token1}'}
        add_body = {"logSourceName":f"test_syslog{num}","assetIp":f"1.1.1.{num}","assetType":4,"factory":3,"port":"null","protocolType":1,"snmpVersion":1,"normalizeGroup":[1386],"community":"","isAnonymousLogin":0,"userName":"","password":"","filePath":"","originalEncoding":"UTF-8","downloadRate":1000,"taskInterval":300,"ftpMode":1,"dbType":"MySQL","dbName":"","customerSqlStatus":0,"dbTableName":"","selectSql":"","logType":[]}
        res = requests.post(add_url, headers=add_headers, json=add_body, verify=False)
        print(res.json())

    def db_select():
        # 连接数据库
        con = mysql.connect(host="192.168.4.154", port=3306, user="root", passwd="Wnt.1@3456", db="soc",
                            charset="utf8")
        # 查询
        sql = "select id,log_source_name,status from soc_log_source_info slsi where log_source_name = 'test3_zk_ftp'"
        result = pd.read_sql(sql, con=con)
        print(result.values)
        return result.values[0][0]


    def logsrc_del():
        token1 = Test1.login()
        del_url = f"{common_url}/log/source/delete/batch"
        del_headers = {"Content-Type": "application/json;charset=UTF-8", "Authorization": f'{token1}'}
        del_body = {'ids': [Test1.db_select()]}
        res = requests.delete(del_url, headers=del_headers, json=del_body, verify=False)
        print(res.json())


if __name__ == '__main__':
    num = 1
    while num <= 40:
        Test1.logsrc_add(num)
        num += 1
    # time.sleep(5)
    # Test1.logsrc_del()










