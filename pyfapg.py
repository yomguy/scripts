#!/usr/bin/python
# 1 mp3 to m3u
# depends: fapg

import os, sys, string

host = 'audio.pre-barreau.com'
root_dir = '/home/pro-barreau/www/audio'
web_dir = '/'
types = ['mp3','ogg','flac']

#s.chdir(root_dir)

for root, dirs, files in os.walk(root_dir+web_dir):
    #print root
    for file in files:
        file_split = file.split('.')
        filename = file_split[len(file_split)-2]
        #print filename
        if not os.path.exists(root+os.sep+filename+'.m3u'):
            fileext = file_split[len(file_split)-1]
            if fileext in types :
                os.chdir(root_dir)
                prefix = 'http://'+host+'/'
                dest_dir = string.replace(root,'/home/pro-barreau/www/audio/','')
                file_new = string.replace(file,' ','_')
                filename_new = string.replace(filename,' ','_')
                if file_new != file: 
                    os.system('mv "'+dest_dir+os.sep+file+'" "'+dest_dir+os.sep+file_new+'"')
                os.system('fapg -f m3u -p '+prefix+' -o "'+root+os.sep+filename_new+'.m3u" "'+dest_dir+os.sep+file_new+'"')

