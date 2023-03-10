
from selenium import webdriver
import time

url = 'http://192.168.100.97/bugfree/index.php/site/login'
chrome_driver = r"D:\work_soft\python\pythonamd\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver)
driver.get(url)

# 登录账号
driver.find_element_by_xpath('//*[@id="LoginForm_username"]').send_keys('kui.zhang')
# 登录密码
driver.find_element_by_xpath('//*[@id="LoginForm_password"]').send_keys('123456')
# 点击登录
driver.find_element_by_xpath('//*[@id="SubmitLoginBTN"]').click()

time.sleep(3)
driver.find_element_by_xpath('//*[@id="top"]/div[3]/a[2]').click()

time.sleep(2)
driver.close()
