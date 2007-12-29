#!/usr/bin/python

import os
import time

service = 'apache2'
mails = ['yomguy@sfr.fr','pellerin@parisson.com']
server = 'ns37892'
file = '/tmp/restartd_apache.tmp'

def touch_and_mail(server, service, mails, file):
    for mail in mails:
        command = 'echo "'+service+' crashed" | mail -s"'+server+'" '+mail
        os.system('touch '+file)
        os.system(command)


if not os.path.exists(file):
    touch_and_mail(server, service, mails, file)

date = os.path.getmtime(file)
laps = time.time() - date
print laps
if laps > 120:
    touch_and_mail(server, service, mails, file)


