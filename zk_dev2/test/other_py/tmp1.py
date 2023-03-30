
# print(str(datetime.datetime.now())[:11])

import gzip
import time

path = "D:\MyInfo_file\edpi.gz"  # 你的文件路径
f = gzip.open(path, 'rb')
num_zu = []
num_zu_1 = []
num_end = []
tmp_a_s = ''

test_a_s = '20230328 06:09:4'
test_a_ip = '36.248.128.89'
num = 0

for line in f.readlines():  # 按行进行读取
    # s 为string类型，就是我们读取的文件中的一行
    s = line.decode('utf-8', errors='ignore').rstrip('\n')  # 读取之后要进行解码
    # print(s)
    # 取出秒数之前的字符串区别分组名称
    a_s = s.split('||')[0][:-1]
    a_ip = s.split('||')[1]
    # print(a_s, a_ip)
    if a_s == test_a_s and a_ip == test_a_ip and a_s != '':
        num += 1
        # print(s)

    # time.sleep(60)


print(f"{test_a_s}组内ip----{test_a_ip}个数是{num}")
# print(num_zu_1)
# print(tmp_num_end)
# print(num_end)
# file = './num.txt'
# myfile = open(file, 'w')
# myfile.write(str(num_end))
# myfile.close()















