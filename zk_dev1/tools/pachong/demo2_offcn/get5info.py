
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup as bs

ua = UserAgent()
header = {'User-Agent': f'{ua.firefox}'}


def write_file(cmd):
    file = './tmp_info.txt'
    tmp_file = open(file, 'a')
    tmp_file.write(cmd)
    tmp_file.close()


def get5info(url, i):
    res = requests.post(url=url, headers=header, verify=False)
    res.encoding = res.apparent_encoding
    r_html = res.text
    soup = bs(r_html, "html.parser")
    word_list = soup.find('ul', class_="lh_newBobotm02")('li')
    # print(word_list)
    info1 = f'-----------{i}-----------\n'
    n = 1
    for b in word_list:
        if n <= 5:
            tmp_info = b.find_next('span').text.replace('\n', '').strip() + '  ' + b.select('a')[1].text + '  ' + b.select('a')[1]['href']
            # print(b.find_next('span').text.replace('\n', '').strip(), b.select('a')[1].text, b.select('a')[1]['href'])
            # print(tmp_info)
            # time.sleep(300)
            info1 = info1 + tmp_info + '\n'
            n += 1
        else:
            break
    # print(info1)
    write_file(info1)


if __name__ == '__main__':
    url = {"教师": 'http://hb.offcn.com/html/jiaoshi/zhaokaoxinxi/hengshui/',
           "公务员": 'http://hb.offcn.com/html/hebeigongwuyuan/zhaokaoxinxi/hengshui/',
           "事业单位": 'http://hb.offcn.com/html/shiyedanwei/zhaokaoxinxi/hengshui/'}
    for i in url:
        get5info(url[i])


