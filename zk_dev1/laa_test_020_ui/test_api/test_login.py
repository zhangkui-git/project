import logging
import time
import pytest
import allure
import os
from selenium import webdriver

logger = logging.getLogger('allure_log')
url = "https://192.168.100.149:8440/"


@pytest.fixture(scope="session")
def if2no2():
    a = '下载中心'
    return a


# @allure.epic('登录成功页面')
@allure.feature('测试登录是否成功')
@allure.description('用例描述信息: 测试登录成功')
# 设置测试用例的级别  blocker > critical > normal > minor > trivial
@allure.severity("normal")
def test_0001(chrome_driver, if2no2):
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
    time.sleep(2)
    res = chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[3]/span[2]').text
    logger.info(f"登录成功：{res}")
    # chrome_driver.close()
    assert res == if2no2


# @allure.epic('数据采集-日志源管理')
@allure.feature('数据采集-新增SYSLOG日志源')
@allure.description('用例描述信息: 新增SYSLOG日志源')
# 设置测试用例的级别  blocker > critical > normal > minor > trivial
@allure.severity("normal")
def test_0002(chrome_driver):
    # chrome_driver.get(url)
    # chrome_driver.maximize_window()
    # # 点击输入框
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[1]').click()
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[1]').send_keys('op_zk')
    # # 点击密码框
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[2]').click()
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[2]').send_keys('Admin@123456')
    # time.sleep(2)
    # # 点击登陆
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[3]').click()
    # # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[4]').click()
    # 切换到数据采集菜单
    time.sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/ul/div[7]/a/li').click()
    time.sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[1]/ul[1]/li[1]/ul/li').click()
    time.sleep(1)
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
    time.sleep(1)
    logger.info(f"新建日志源成功")
    res = chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div/span[text()="test_syslog1"]').text
    # chrome_driver.close()
    assert res == "test_syslog1"


# @allure.epic('数据采集-日志源管理')
@allure.feature('数据采集-删除--新增SYSLOG日志源')
@allure.description('用例描述信息: 删除--新增SYSLOG日志源')
# 设置测试用例的级别  blocker > critical > normal > minor > trivial
@allure.severity("normal")
def test_0003(chrome_driver):
    # chrome_driver.get(url)
    # chrome_driver.maximize_window()
    # # 点击输入框
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[1]').click()
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[1]').send_keys('op_zk')
    # # 点击密码框
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[2]').click()
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[2]').send_keys('Admin@123456')
    # time.sleep(2)
    # # 点击登陆
    # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[3]').click()
    # # chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div/input[4]').click()
    # 切换到数据采集菜单
    time.sleep(1)
    chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/ul/div[7]/a/li').click()
    # 点击删除
    time.sleep(1)
    element1 = chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[15]/div/div/span[3]/span')
    time.sleep(1)
    chrome_driver.execute_script("arguments[0].click();", element1)
    time.sleep(1)
    chrome_driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/button[2]/span').click()
    time.sleep(1)
    res = chrome_driver.find_element_by_xpath('//*[@id="app"]/div/div[3]/section/div/div[2]/div[1]/div[3]/table/tbody/tr/td[2]/div/span').text
    chrome_driver.close()
    logger.info("删除日志源成功")
    assert res == 'test_zk_syslog3'

