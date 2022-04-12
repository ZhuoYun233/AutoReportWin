import time, os
from configparser import ConfigParser,NoSectionError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException,NoSuchElementException,InvalidSessionIdException

#chromedriver路径
DRIVER_PATH = 'chromedriver.exe'
if not os.path.exists(DRIVER_PATH):
    print('找不到ChromeDriver!')
    input()
    exit(0)

options = webdriver.ChromeOptions()
# 忽略无用日志
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

configINI = "config.ini"
s = Service(DRIVER_PATH)

def fillIn(username, password, driver):
    driver.get("https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/mrybtb.jsp")
    driver.maximize_window()
    time.sleep(1)
    driver.find_element(by = By.ID, value = 'username').send_keys(username)
    time.sleep(1)
    driver.find_element(by = By.ID, value = "password").send_keys(password)
    time.sleep(1)
    driver.find_element(by = By.CLASS_NAME, value = "auth_login_btn").click()
    time.sleep(3)
    driver.find_element(by = By.ID, value = "sui-select-swjkzk19").send_keys(1)
    time.sleep(1)
    driver.find_element(by = By.ID, value = "sui-select-xcm4").send_keys(1)
    time.sleep(1)
    driver.find_element(by = By.ID, value = "sui-select-sfycxxwc33").send_keys(1)
    time.sleep(1)
    driver.find_element(by = By.ID, value = "post").click()
    time.sleep(1)
    driver.find_element(by = By.CLASS_NAME, value = "layui-layer-btn0").click()
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
        driver = webdriver.Chrome(service=s, options=options)
        fillIn(accountNow,passwordNow,driver)
        fillIn(accountNow,passwordNow)
    except NoSectionError:
        print('已经全部填报或存在序号跳跃')
        break
    except ElementClickInterceptedException:
        print('账号'+str(i-1)+':'+accountNow+'今日已经填报过了')
        try:
            driver.close()
        except:
            print('chromedriver已经关闭了')
        continue
    except NoSuchElementException:
        print('账号'+str(i-1)+'密码错误或账号错误')
        try:
            driver.close()
        except:
            print('chromedriver已经关闭了')
        continue
exit(0)

