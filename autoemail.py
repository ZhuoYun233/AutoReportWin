#coding:utf-8 #强制使用utf-8编码格式
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

#####################################
#请修改这里的内容！
SENDER_MAIL='xxxxxx@outlook.com' #发件人邮箱账号
SENDER_PWD='xxxxxx' #发件人邮箱密码
RECEIVE_MAIL='xxxxxxx' #收件人邮箱账号
RECEIVER = 'xxxxxx' #收件人昵称
#####################################

#可以自定义发件人昵称和主题
SENDER = '填报小助手' #发件人昵称
SUBJECT = '填报反馈(ˊᗜˋ*)' #主题
def mail(content):
    try:
        msg=MIMEText(content,'plain','utf-8')
        msg['From']=formataddr([SENDER,SENDER_MAIL])
        msg['To']=formataddr([RECEIVER,RECEIVE_MAIL])
        msg['Subject']=SUBJECT

        server=smtplib.SMTP("smtp.office365.com",587) #发件人邮箱中的SMTP服务器，这里使用的是outlook邮箱
        server.starttls() #发件人邮箱的加密方式，请自行修改
        server.login(SENDER_MAIL,SENDER_PWD)
        server.sendmail(SENDER_MAIL,[RECEIVE_MAIL,],msg.as_string())
        server.quit() #关闭连接
        print("Auto email Successful!") #发送成功
    except Exception: 
        print("Auto email Filed.") #发送失败