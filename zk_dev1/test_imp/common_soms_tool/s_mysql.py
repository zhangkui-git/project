import pymysql as mysql
from zk_dev1.test_imp.common_soms_tool.common_conf import *


def select(sql):
    # 连接数据库
    con = mysql.connect(host=db_host, port=db_port, user=db_name, passwd=db_pas, db=db_scn_name, charset="utf8")
    # 创建一个游标对象
    cur = con.cursor(cursor=mysql.cursors.DictCursor)
    # print("连接成功")
    cur.execute(sql)
    res1 = cur.fetchall()
    con.commit()  # 查询也要加，否则一次连接多次查询时会有问题
    cur.close()
    return res1


if __name__ == '__main__':
    sql1 = "select id from soc_log_source_info slsi where log_source_name = 'testzk2'"
    sql2 = "select rule_id from soc_normalize_info slsi where rule_name = '配置变更日志-副本11111'"
    select(sql2)


