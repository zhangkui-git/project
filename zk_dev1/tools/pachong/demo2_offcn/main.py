from get5info import *
from send_mail import *
import os

url = {"教师": 'http://hb.offcn.com/html/jiaoshi/zhaokaoxinxi/hengshui/', "公务员": 'http://hb.offcn.com/html/hebeigongwuyuan/zhaokaoxinxi/hengshui/', "事业单位": 'http://hb.offcn.com/html/shiyedanwei/zhaokaoxinxi/hengshui/'}


def get2txt():
    for i in url:
        get5info(url[i], i)


def read2txt():
    file = './tmp_info.txt'
    info2 = ''
    for line in open(file):
        info2 = info2 + line
    return info2


if __name__ == '__main__':
    os.remove('./tmp_info.txt')
    get2txt()
    # read2txt()
    sendmail(read2txt())
    os.remove('./tmp_info.txt')
