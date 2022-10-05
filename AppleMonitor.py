from enum import Flag
from random import choice
import requests
import re
from time import sleep

import smtplib
from email.mime.text import MIMEText


#设置服务器所需信息
#163邮箱服务器地址
mail_host = 'smtp.163.com'  
#163用户名
mail_user = '163用户名'  
#密码(部分邮箱为授权码) 
mail_pass = '授权码'   
#邮件发送方邮箱地址
sender = '发送方邮箱地址'  
#邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['邮件接受方邮箱地址']  

def sendMail():
    #设置email信息
    #邮件内容设置
    message = MIMEText('AppleMonitor:ip14pro苏州有货！','plain','utf-8')
    #邮件主题       
    message['Subject'] = 'AppleMonitor Notification' 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误


user_agent_list=['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko)','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)','Opera/9.80 (Windows NT 6.1; WOW64; U; zh-cn) Presto/2.10.229 Version/11.62']



def AppleMonitor(flag0,count):
    try:
        #根据需要修改地址及产品id，location、product（parts.0=后面的）
        location='江苏 苏州 姑苏区'
        product='MPXR3CH/A'
        url='https://www.apple.com.cn/shop/fulfillment-messages?pl=true&mts.0=regular&parts.0='+product+'&location='+location

        kv = {'user-agent': choice(user_agent_list)}
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        pattern = re.compile('"pickupDisplay":"(.*?)"', re.S)
        r.encoding = r.apparent_encoding
        res=re.search(pattern,r.text)
        
        if res.group(1)!='unavailable':
            if flag0==False:
                # 有货就发送邮件
                sendMail()

                # flag0和count用来实现发邮件的CoolDown
                flag0=True
                count=120
            print('=======================================')
            print('=======================================')
            print('=======================================')
            print('                有货！')
            print('=======================================')
            print('=======================================')
            print('=======================================')
            print('')
        # else:
        #     print('not available')
        if flag0:
            count=count-1
            if count==0:
                flag0=False


        #     print('无货')
        return flag0,count
    except:
        print("失败")
        return flag0,count

if __name__=='__main__':
    flag0=False
    count=120
    while 1:
        flag0,count=AppleMonitor(flag0,count)
        # 爬虫cd
        sleep(1)