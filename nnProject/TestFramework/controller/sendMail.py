#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/23

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
# SMTP server
mail_host = "smtp.exmail.qq.com"  # setup servers
mail_user = "baoting.zhang@westwell-lab.com"  # user mail
mail_pass = "Zhang@2018"   # password

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_mail(f, to_addr):
    """
    :param f: Attachment path
    :param to_addr: addressee list []
    :return:
    """
    from_addr = mail_user
    password = mail_pass

    smtp_server = mail_host

    msg = MIMEMultipart()

    # msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
    msg['From'] = _format_addr('Good Luck<%s>' % from_addr)
    msg['To'] = _format_addr('God <%s>' % to_addr)
    msg['Subject'] = Header('CI test result……', 'utf-8').encode()      # Email Subject

    msg.attach(MIMEText('interface test result.', 'plain', 'utf-8'))   # Email content
    part = MIMEApplication(open(f, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=f)
    msg.attach(part)

    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(0)       # set print level
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()


if __name__ == '__main__':
    attachment_path = "G:\\Doc\\README.md"
    tomail = "baoting.zhang@westwell-lab.com"
    # tomail = "zhangbaoting_china@126.com"
    print tomail
    send_mail(f=attachment_path, to_addr=tomail)
    print "it's ok, this is test for sendmail"