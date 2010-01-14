#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging


class Logger:
    """A logging object"""

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def write(self, message):
        self.logger.info(message)


class ParissonMailLogger:

    def __init__(self, emails, server, service, txt_file=None):
        self.emails = emails
        self.server = server
        self.service = service
        self.user = 'logger'
        self.user_email = self.user + '@' + self.server
        self.smtp_server = smtplib.SMTP('localhost')
        self.date = time.strftime("%a, %d %b %Y %H:%M:%S +0200", time.localtime())
        self.msg = self.date + ' : ' + self.service + ' has logged this information'
        self.mime_msg = MIMEMultipart()
        self.mime_msg['Subject'] = 'URGENT ! 'self.server + ' : ' + self.service
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
    server = sys.argv[-3]
    emails = ['yomguy@sfr.fr','yomguy@parisson.com', 'janob@parisson.com']
    p = ParissonMailLogger(emails, server, service, txt_file)
    p.send()
    p.smtp_server.quit()

if __name__ == '__main__':
    main()

