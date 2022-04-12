import time, os
from configparser import ConfigParser,NoSectionError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException,NoSuchElementException,InvalidSessionIdException

import autoReport

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

#生成反馈信息，各参数以此为：编号，管理员邮件反馈，用户邮件反馈，管理员pushplus反馈，当前账号，结果
def report(num,admin_mail_report,user_reports,admin_json_report,account,status):
    print('账号'+str(num)+':'+account+status) #命令行反馈
    admin_mail_report = admin_mail_report + (' 账号'+str(num)+':'+account+status+'\n') #管理员邮件反馈
    user_reports.append('账号'+account+':'+status+'\n') #用户邮件反馈
    admin_json_report['账号'+str(num)+':'+account] = status #管理员pushplus反馈
    return (admin_mail_report,user_reports,admin_json_report)

#执行反馈操作
def do_report(admin_mail_report,user_reports,receivers,admin_json_report):
    admin_mail_report = admin_mail_report + ('\nヾ(๑╹ꇴ◠๑)ﾉ”祝您天天开心!')
    #autoReport.mail(admin_mail_report) #启用管理员邮件反馈
    autoReport.mails(user_reports,receivers) #启用用户邮件反馈
    autoReport.pushplus('填报反馈(ˊᗜˋ*)',admin_json_report) #启用管理员pushplus反馈

admin_json_report = {} #管理员反馈
user_reports = [] #用户反馈内容列表
receivers = {} #用户清单
admin_mail_report = '今日自动填报结果：\n\n'

i=1
while True:
    account="ACCOUNT"+str(i)
    try:
        accountNow=getConfig(account,"ACCOUNT")
        passwordNow=getConfig(account,"PASSWORD")
        # 尝试获取邮件信息
        aliasNow = getConfig(account,"ALIAS")
        mailNow = getConfig(account,"MAIL")
        receivers[aliasNow]=mailNow
            
        i += 1
        driver = webdriver.Chrome(service=s, options=options)
        fillIn(accountNow,passwordNow,driver)
        admin_mail_report,user_reports,admin_json_report = report(num=i-1,admin_mail_report=admin_mail_report,user_reports=user_reports,admin_json_report=admin_json_report,account=accountNow,status='完成！')
        
    except NoSectionError:
        print('已经全部填报或存在序号跳跃')
        do_report(admin_mail_report,user_reports,receivers,admin_json_report)
        break
    except ElementClickInterceptedException:
        admin_mail_report,user_reports,admin_json_report = report(num=i-1,admin_mail_report=admin_mail_report,user_reports=user_reports,admin_json_report=admin_json_report,account=accountNow,status='今日已填报')
        try:
            driver.close()
        except:
            print('chromedriver已经关闭了')
        continue
    except NoSuchElementException:
        admin_mail_report,user_reports,admin_json_report = report(num=i-1,admin_mail_report=admin_mail_report,user_reports=user_reports,admin_json_report=admin_json_report,account=accountNow,status='账号或密码错误')
        try:
            driver.close()
        except:
            print('chromedriver已经关闭了')
        continue
exit(0)