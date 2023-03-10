
import pymysql as mysql
import pandas as pd
import xlrd2
import datetime
start = datetime.datetime.now()
print(start)

worksheet = xlrd2.open_workbook(r'D:\work_down\python_t\runoob_tb_test1.xlsx')
sheet_names = worksheet.sheet_names()
print(sheet_names)

sheet = worksheet.sheet_by_name(sheet_names[0])
rows = sheet.nrows
cols = sheet.ncols
res = []
for i in range(1, rows):
    f = 0
    tmp = []
    while f <= 2:
        data = str(sheet.cell(i, f))[6:-1]
        tmp.append(data)
        f += 1
    res.append(tuple(tmp))
print("数据结果------", res)


# 连接数据库
con = mysql.connect(host="192.168.92.128", port=3305, user="root", passwd="family2021", db="testzk", charset="utf8")
mycursor = con.cursor()
print("连接成功")

# 创建一个游标对象
cur = con.cursor(cursor=mysql.cursors.DictCursor)

# 读取excel结果插入
count = 1
for e in range(len(res)):
    insert_sql = "insert into runoob_tb_test(runoob_title, runoob_author, submission_date) value" \
        + str(res[e]) \
        + ";"
    if count <= 500:
        res_insert = cur.execute(insert_sql)
        count += 1
    con.commit()
    count = 1
# 查询
sql1 = "select count(*) from runoob_tb_test;"
result = pd.read_sql(sql1, con=con)
print(result)
# 删除
# sql = "delete from 数据库表名"
# mycursor.execute(sql)
# print("删除数据长度：", mycursor.rowcount)

end = datetime.datetime.now()

print(end - start)


