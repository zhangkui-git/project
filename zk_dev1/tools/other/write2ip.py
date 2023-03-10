import random

tmp = 1
file = open('D:\MyInfo_file\python_t\getip.txt', 'w')
while tmp <= 200:
    getip1 = random.randint(1, 200)
    getip2 = random.randint(1, 200)
    getip3 = random.randint(1, 200)
    getip4 = random.randint(1, 200)
    getip = f'{getip1}' + '.' + f'{getip2}' + '.' + f'{getip3}' + '.' + f'{getip4}' + '\n'
    tmp += 1
    file.write(getip)
file.close()

