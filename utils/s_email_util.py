import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
import datetime

# 第三方 SMTP 服务
mail_host = "smtp.office365.com"  # 设置服务器
mail_port = 587  # 设置服务器
mail_user = "likeOrangeForWork@outlook.com"  # 用户名
mail_pass = "LOFWasdasd346"  # 口令

mail_sender = 'likeOrangeForWork@outlook.com'
# 接收邮件，可设置为你的QQ邮箱或者其他邮箱
receivers = ['5308511@qq.com', '1328832585@qq.com', 'likeOrange1102@outlook.com']

def mail(title,content):
    ret = True
    try:
        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        msg = MIMEText(content, 'plain', 'utf-8')
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr([u"王琨", mail_sender])
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = formataddr([u"韩站长", receivers[0]])+ \
            ';'+formataddr([u"张主任", receivers[1]])+\
            ';'+formataddr([u"王琨", receivers[2]])
        msg['Subject'] = Header(title, 'utf-8')                # 邮件的主题，也可以说是标题
        print(msg.as_string())

        # server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server = smtplib.SMTP(mail_host, mail_port)  # 发件人邮箱中的SMTP服务器，端口是25
        server.ehlo()  # 向Gamil发送SMTP 'ehlo' 命令
        server.starttls()
        server.login(mail_user, mail_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(mail_sender, receivers, msg.as_string())
        server.quit()  # 关闭连接
    except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
        print('e',repr(e))    
        
    return ret

