import time
from selenium import webdriver
import os
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
options = webdriver.ChromeOptions()
# 这个是绝对路径
driver = webdriver.Chrome(executable_path="C:/Users/xus17/downloads/chromedriver", options=options)
driver.get("https://workflow.ecust.edu.cn/default/work/uust/zxxsmryb/mrybtb.jsp")
 
# 最大化浏览器
driver.maximize_window()
time.sleep(5)
driver.find_element_by_id("username").send_keys(username)
time.sleep(5)
driver.find_element_by_id("password").send_keys(password)
time.sleep(5)
driver.find_element_by_class_name("auth_login_btn").click()
time.sleep(5)
driver.find_element_by_id("sui-select-xcm4").send_keys(1)
time.sleep(5)
driver.find_element_by_id("sui-select-sfycxxwc33").send_keys(1)
time.sleep(5)
driver.find_element_by_id("post").click()
time.sleep(5)
driver.close()