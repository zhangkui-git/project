
# print(str(datetime.datetime.now())[:11])


from fake_useragent import UserAgent
import requests

ua = UserAgent()
header = {'User-Agent': f'{ua.firefox}'}
url = 'http://jszg.hee.gov.cn/zige/detail/272273/136.html'
res = requests.get(url=url, headers=header, verify=False)
res.encoding = res.apparent_encoding
r_html = res.text
# soup5 = bs(r_html, "html.parser")
# soup5 = bs(r_html, 'lxml')
print(r_html)





