from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
from random import Random

from django.conf import settings
from django.core.mail import send_mail
import smtplib

# from users import models.EmailVerifyRecord
# from .models import EmailVerifyRecord
from users.models import EmailVerifyRecord


def random_str(randomlength=8):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_content = ''
    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        msg = MIMEText(email_body, 'plain', 'utf-8')
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr([u"王琨", settings.EMAIL_HOST_USER])
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = formataddr([u"ABC", email])
        msg['Subject'] = Header(email_title, 'utf-8')  # 邮件的主题，也可以说是标题

        s = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        s.ehlo()  # 向Gamil发送SMTP 'ehlo' 命令
        s.starttls()
        s.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        s.sendmail(settings.EMAIL_FROM, email, msg.as_string())
        s.quit()
        # send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        # if send_status:
        #     pass
    elif send_type == "forget":
        email_title = "慕学在线网注册密码重置链接"
        email_body = "请点击下面的链接重置密码: http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update_email":
        email_title = "慕学在线邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(code)

        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            pass
