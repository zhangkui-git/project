from selenium import webdriver
import time


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
chrome_driver_path = r"D:\work_soft\python\pythonamd\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
chrome_driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver_path)



def test_001(url):
    print('用例002: 新增SYSLOG日志源')
    chrome_driver.get(url)
    chrome_driver.maximize_window()
    # 点击输入框
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[1]').click()
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[1]').send_keys('op_zk')
    # 点击密码框
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[2]').click()
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[2]').send_keys('Admin@123456')
    time.sleep(2)
    # 点击登陆
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[3]').click()
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[4]').click()
    time.sleep(5)
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/ul/div[7]/a/li').click()
    time.sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[1]/ul[1]/li[1]/ul/li').click()
    time.sleep(3)
    # 填写日志源名称
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[2]/form/div[1]/div/div/input').click()
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[2]/form/div[1]/div/div/input').send_keys("test_syslog1")
    time.sleep(1)
    # 选择协议类型
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[2]/form/div[2]/div/div/div/input').click()
    time.sleep(3)
    # 选择Syslog协议，利用xpath定位动态元素
    chrome_driver.find_element_by_xpath("/html/body/div[last()]/div[1]/div[1]/ul/li[1]").click()
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[1]').click()
    # 填写设备A网
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[2]/form/div[3]/div/div[1]/input').click()
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[2]/form/div[3]/div/div[1]/input').send_keys("1.1.1.111")
    # 选择设备类型，选择服务器类型，利用xpath定位动态元素
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[last()]/section/div/div[3]/div/div[2]/form/div[5]/div/div/div[1]/input').click()
    time.sleep(1)
    chrome_driver.find_element_by_xpath('/html/body/div[last()]/div[1]/div[1]/ul/li[4]').click()
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[1]').click()
    # 所属区域，选择所属区域，利用xpath定位动态元素
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[2]/form/div[6]/div/div/div/div/input').click()
    time.sleep(1)
    chrome_driver.find_element_by_xpath('//*[contains(@id,"cascader-menu") and contains(@id,"-0-0")]/span/span/span[text()="XX集团"]').click()
    time.sleep(1)
    chrome_driver.find_element_by_xpath('//*[contains(@id,"cascader-menu") and contains(@id,"-1-0")]/span/span/span[text()="河北"]').click()
    time.sleep(1)
    chrome_driver.find_element_by_xpath('//*[contains(@id,"cascader-menu") and contains(@id,"-2-0")]/label/span[1]/span').click()
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[1]').click()
    # 范化组，选择范化组，利用xpath定位动态元素，且解决元素相互覆盖问题
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[2]/form/div[7]/div/div/div/div[1]/input').click()
    time.sleep(1)
    chrome_driver.find_element_by_xpath('//*[contains(@id,"cascader-menu") and contains(@id,"-0-4")]/span/span/span').click()
    time.sleep(1)
    element = chrome_driver.find_element_by_xpath('//*[contains(@id,"cascader-menu") and contains(@id,"-1-16")]/label/span/span')
    time.sleep(1)
    chrome_driver.execute_script("arguments[0].click();", element)
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[1]').click()
    # 点击确定
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[3]/div/div[2]/form/div[8]/div/button[2]/span').click()
    time.sleep(5)
    chrome_driver.close()


if __name__ == '__main__':
    url = "https://192.168.100.149:8440/#/login?redirect=%2F/"
    test_001(url)

