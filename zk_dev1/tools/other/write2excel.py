
# ----------追加方式写入excel

import openpyxl
import datetime
start = datetime.datetime.now()
# 读取excel文件，获取workbook对象
get_excel = openpyxl.load_workbook(r"D:\work_down\python_t\runoob_tb_test1.xlsx")
# get_excel = xlrd.open_workbook(r"D:\work_down\python_t\runoob_tb_test1.xls")
# 通过名称获取工作薄
sheet = get_excel['Sheet1']

# 批量造数据，格式：("日志级别1", "mysql1", "2022-05-21")
now_time = datetime.datetime.now()
add_start_time = datetime.timedelta(days=1)
add_end_time = now_time + datetime.timedelta(days=100000)
end_now = str(add_end_time.strftime('%Y/%m/%d'))

offset = now_time
n = 1
while str(offset.strftime('%Y/%m/%d')) != end_now:
    offset += add_start_time
    # print(type(offset.strftime('%Y-%m-%d')))
    tmp = n
    data = [f'日志级别{tmp}', f'mysql{tmp}', f'{offset.strftime("%Y/%m/%d")}']
    n += 1
    sheet.append(data)

# 插入数据
# sheet.append(('日志级别28', 'mysql28', '2022/05/28'))
# 具体修改哪一行那一列的数据
# 注意：cell的参数row、column必须是大于等于1的。
# sheet.cell(行, 列).value = 数据
# 保存,传入原文件则在原文件上追加数据，也可以保存为新文
get_excel.save(r"D:\work_down\python_t\runoob_tb_test1.xlsx")
end = datetime.datetime.now()
print('写入完成，用时消耗：', end - start)

