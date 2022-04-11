from configparser import ConfigParser,NoSectionError
import time
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException,NoSuchElementException,InvalidSessionIdException
import os
options = webdriver.ChromeOptions()
# 以下存放chromedriver路径，按需要修改
configINI = "config.ini"
webdriver_path=os.path.dirname(os.path.realpath(__file__)) +'/chromedriver.exe'
driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

def fillIn(username, password):
    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)
    driver.get("https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/mrybtb.jsp")
    
    driver.maximize_window()
    time.sleep(1)
    driver.find_element_by_id("username").send_keys(username)
    time.sleep(1)
    driver.find_element_by_id("password").send_keys(password)
    time.sleep(1)
    driver.find_element_by_class_name("auth_login_btn").click()
    time.sleep(3)
    driver.find_element_by_id("sui-select-swjkzk19").send_keys(1)
    time.sleep(1)
    driver.find_element_by_id("sui-select-xcm4").send_keys(1)
    time.sleep(1)
    driver.find_element_by_id("sui-select-sfycxxwc33").send_keys(1)
    time.sleep(1)
    driver.find_element_by_id("post").click()
    time.sleep(1)
    driver.find_element_by_class_name("layui-layer-btn0").click()
    time.sleep(1)
    driver.close()
def getConfig(section,key):
    config=ConfigParser()
    config.read(configINI)
    return config.get(section,key)
i=1
while True:
    account="ACCOUNT"+str(i)
    try:
        accountNow=getConfig(account,"ACCOUNT")
        passwordNow=getConfig(account,"PASSWORD")
        i += 1
        fillIn(accountNow,passwordNow)
    except NoSectionError:
        print('已经全部填报或存在序号跳跃')
        break
    except ElementClickInterceptedException:
        print('账号'+str(i-1)+':'+accountNow+'今日已经填报过了')
        driver.close()
        continue
    except NoSuchElementException:
        print('账号'+str(i-1)+'密码错误或账号错误')
        driver.close()
        continue
