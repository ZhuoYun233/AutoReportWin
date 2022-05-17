import time, os
from configparser import ConfigParser,NoSectionError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException,NoSuchElementException,InvalidSessionIdException

import autoReport

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

def report(num,admin_mail_report,user_reports,admin_json_report,account,status):
    print('账号'+str(num)+':'+account+status)
    admin_mail_report = admin_mail_report + (' 账号'+str(num)+':'+account+status+'\n')
    user_reports.append('账号'+account+':'+status+'\n')
    admin_json_report['账号'+str(num)+':'+account] = status
    return (admin_mail_report,user_reports,admin_json_report)

def do_report(admin_mail_report,user_reports,receivers,admin_json_report):
    admin_mail_report = admin_mail_report + ('\nヾ(๑╹ꇴ◠๑)ﾉ”祝您天天开心!')
    #autoReport.mail(admin_mail_report) #启用管理员邮件反馈
    autoReport.mails(user_reports,receivers) #启用用户邮件反馈
    autoReport.pushplus('填报反馈(ˊᗜˋ*)',admin_json_report) #启用管理员pushplus反馈

#主程序
if __name__ == "__main__":
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
    #初始化变量
    admin_json_report = {}
    user_reports = []
    receivers = {}
    try_count = 0 #尝试填报计数
    error_flag = False #错误标志
    error_account_number = [] #错误账户序号
    i=1
    admin_mail_report = '今日自动填报结果：\n\n'

    while True:
        while True:

            #第一次尝试时填写全部账户
            if(try_count==0):
                account="ACCOUNT"+str(i)
            #重复尝试时只填写出现错误的账户
            else:
                #检查是否遍历出错账户
                if(i>len(error_account_number)):
                    break
                account="ACCOUNT"+str(error_account_number[i-1])
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
                if not i-1 in error_account_number:
                    error_account_number.append(i-1)
                error_flag=True
                try:
                    driver.close()
                except:
                    print('chromedriver已经关闭了')
                continue
        try_count+=1
        #出现错误则重试，至多重试三次
        if(try_count<3 and error_flag):
            i=1
        else:
            do_report(admin_mail_report,user_reports,receivers,admin_json_report)
            break
    exit(0)
