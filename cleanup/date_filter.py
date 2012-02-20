#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,  time, sys

root_orig = sys.argv[1]
#root_dest = sys.argv[2]
date_filter = '08'

date_file_list = []
for root, dirs, files in os.walk(root_orig):
    for file in files:
        #print file
        stats = os.stat(root+os.sep+file)
        lastmod_date = time.localtime(stats[8])
        date_file_tuple = lastmod_date, root+os.sep+file, stats[6]
        date_file_list.append(date_file_tuple)

date_file_list.sort()
date_file_list.reverse() # newest mod date now first

total_size = 0
print "%-50s %s" % ("filename:", "last modified:")
for file in date_file_list:
    if os.path.isfile(file[1]):
        file_date = time.strftime("%y/%m/%d %H:%M:%S", file[0])
        year = time.strftime("%y", file[0])
        #dest_file = root_dest+os.sep+file[1]
        if year <= date_filter and file[1].split('.')[-1] == 'mp3' and 'CRFPA' in file[1] :
        #os.path.exists(dest_file) :
            print "%-50s %s" % (file[1], file_date)
            total_size += file[2]

            #os.system('sudo rm "' + file[1] + '"')
            #os.system('sudo touch "' + file[1] + '"')
            #os.system('sudo chown zope:zope "' + file[1] + '"')
            #os.system('sudo chmod 600 "' + file[1] + '"')

            #os.symlink(dest_file, file[1])
            #print "File linked !"

print total_size