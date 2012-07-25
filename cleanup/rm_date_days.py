#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, stat, datetime

if len(sys.argv) <= 2:
    exit('Usage : python rm_date.py DAYS PATH')
    

dir = sys.argv[-1]
days = int(sys.argv[-2])
today = datetime.datetime.today()

for root, dirs, files in os.walk(dir):
    for filename in files:
        file  = root + os.sep + filename
        file_date = datetime.datetime.fromtimestamp(os.path.getmtime(file))
        diff = today - file_date
	if diff.days >= days:
	    os.remove(file)
	    print 'removed : ', file_date, file
	    
	    
