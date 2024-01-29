#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, stat, time

if len(sys.argv) <= 2:
    exit('Usage : python rm_date.py DAY MONTH YEAR PATH')

dir = sys.argv[-1]
year = int(sys.argv[-2])
month = int(sys.argv[-3])
day = int(sys.argv[-4])

date_file_list = []
for root, dirs, files in os.walk(dir):
    for file in files:
        #print file
        stats = os.stat(root+os.sep+file)
        lastmod_date = time.strftime("%d_%m_%Y",time.localtime(stats[stat.ST_MTIME]))
        date_file_tuple = lastmod_date, root+os.sep+file
        date_file_list.append(date_file_tuple)

date_file_list.sort()
date_file_list.reverse() # newest mod date now first

for file in date_file_list:
    if os.path.isfile(file[1]):
	date = file[0].split('_')
        d = int(date[0])
	m = int(date[1])
	y = int(date[2])
	if y <= year and m <= month and d <= day:
	    #os.remove(file[1])
	    print 'removed : ', y, m, d, file
