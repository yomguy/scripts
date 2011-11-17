#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ParissonMailLogger:

    def __init__(self, emails, service, txt_file=None):
        self.emails = emails
        self.server = socket.gethostbyaddr(socket.gethostname())[0]
        self.service = service
        self.user = 'logger-no-reply'
        self.user_email = self.user + '@' + self.server
        self.smtp_server = smtplib.SMTP('localhost')
        self.date = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        self.msg = self.date + ' : ' + self.service + ' has logged this information'
        self.mime_msg = MIMEMultipart()
        self.mime_msg['Subject'] = self.server + ' : ' + self.service
        self.mime_msg['To'] = ', '.join(self.emails)
        self.mime_msg['From'] = self.user_email
        self.mime_txt = MIMEText(self.msg)
        self.mime_msg.attach(self.mime_txt)
        if txt_file:
            self.txt_file = open(txt_file, 'r')
            self.mime_txt = MIMEText(self.txt_file.read())
            self.mime_msg.attach(self.mime_txt)
            self.txt_file.close()

    def send(self):
        self.smtp_server.sendmail(self.user_email, self.emails, self.mime_msg.as_string())

def main():
    txt_file = sys.argv[-1]
    service = sys.argv[-2]
    emails = ['yomguy@parisson.com', 'webmaster@parisson.com']

    p = ParissonMailLogger(emails, service, txt_file)
    p.send()
    p.smtp_server.quit()

if __name__ == '__main__':
    main()

