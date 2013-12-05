#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, stat, time

if len(sys.argv) <= 2:
    exit('Usage : python rm_smaller.py DIR')
    

dir = sys.argv[-1]
file_list = []

for root, dirs, files in os.walk(dir):
    for file in files:
        print file
        src_stats = os.stat(root+os.sep+file)
        src_lastmod_date = time.localtime(src_stats[stat.ST_MTIME])
        src_size = src_stats.st_size
        file_list.append({'path': root+os.sep+file, 'date': src_lastmod_date, 'size': src_size})

#date_file_list.sort()
#date_file_list.reverse() # newest mod date now first

for src_file in file_list:
    if os.path.isfile(src_file['path']):
        for copy_file in file_list:
            if os.path.isfile(copy_file['path']) and copy_file['date'] == src_file['date'] and copy_file['size'] == src_file['size'] and not copy_file['path'] == src_file['path']:
	    #os.remove(copy_file['path'])
	    print 'removed', copy_file['path']
	  
