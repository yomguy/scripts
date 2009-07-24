#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,  time, sys

root = sys.argv[1] # one specific folder

date_file_list = []
for root, dirs, files in os.walk(root):
    for file in files:
        #print file
        stats = os.stat(root+os.sep+file)
        lastmod_date = time.localtime(stats[8])
        date_file_tuple = lastmod_date, root+os.sep+file
        date_file_list.append(date_file_tuple)

date_file_list.sort()
date_file_list.reverse() # newest mod date now first

print "%-40s %s" % ("filename:", "last modified:")
for file in date_file_list:
    if os.path.isfile(file[1]):
        #folder, file_name = os.path.split(file[1])
        file_date = time.strftime("%y/%m/%d %H:%M:%S", file[0])
        #print "%-40s %s" % (file_name, file_date)
        print "%-50s %s" % (file[1], file_date)
