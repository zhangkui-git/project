from fake_useragent import UserAgent
import requests
import os

ua = UserAgent()
url1 = 'https://ppt.1ppt.com/uploads/soft/1907/1-1ZGR05445.zip'
header = {'User-Agent': f'{ua.firefox}'}


def downloadfile(url, filename=None):
  if(not filename):                         # 如果参数没有指定文件名
    filename = os.path.basename(url)          # 取用url的尾巴为文件名
  leng = 1
  while(leng==1):
    torrent = requests.get(url, headers=header)
    leng = len(list(torrent.iter_content(1024)))  # 下载区块数
    if(leng == 1):                                # 如果是1 就是空文件 重新下载
      print(filename,'下载失败,重新下载')
      time.sleep(1)
    else:
      print('下载完成')
  with open(filename, 'wb') as f:
    for chunk in torrent.iter_content(1024):    # 防止文件过大，以1024为单位一段段写入
      f.write(chunk)


if __name__ == '__main__':
    downloadfile(url1)