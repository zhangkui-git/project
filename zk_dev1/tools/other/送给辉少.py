import gzip

path = "D:\MyInfo_file\edpi.gz"  # 你的文件路径
f = gzip.open(path, 'rb')
num_zu = []
num_zu_1 = []
num_end = []
tmp_a_s = ''


for line in f.readlines():  # 按行进行读取
    # s 为string类型，就是我们读取的文件中的一行
    s = line.decode('utf-8', errors='ignore').rstrip('\n')  # 读取之后要进行解码
    # s = str(line, encoding="utf-8")
    # print(s)
    # 取出秒数之前的字符串区别分组名称
    a_s = s.split('||')[0][:-1]
    a_ip = s.split('||')[1]

    name_zu = a_s + '0'
    if a_s != '' and a_s not in num_zu_1:
        num_zu.append(name_zu)
        num_zu_1.append(a_s)
        tmp_a_s = a_s
        tmp_num_end = {}
        num_end.append(tmp_num_end)
    elif a_s != '' and a_s in num_zu_1:
        a_s_index = num_zu_1.index(a_s)
        if a_ip in num_end[a_s_index]:
            num_end[a_s_index][a_ip] = num_end[a_s_index][a_ip] + 1
        else:
            num_end[a_s_index][a_ip] = 1

    elif a_s != '' and a_s == tmp_a_s and a_ip not in tmp_num_end:
        tmp_num_end[a_ip] = 1
    elif a_s != '' and a_s == tmp_a_s and a_ip in tmp_num_end:
        tmp_num_end[a_ip] = tmp_num_end[a_ip] + 1

# 打印分组的名称
print(num_zu)


for x, i in enumerate(num_end):
    a_val = list(i.values())
    a_key = list(i.keys())
    # print(sorted(a_val, reverse=True))
    # print(a_val.index(599))
    # print(a_key[285])
    num_max = str(sorted(i.values(), reverse=True)[0])
    print(num_zu[x] + '|' + a_key[a_val.index(sorted(i.values(), reverse=True)[0])] + '|' + num_max)