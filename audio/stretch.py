#!/usr/bin/python
# -*- coding: utf-8 -*-
# 1 mp3 to m3u
# depends: fapg

import os, sys, string

stretch_app = '/home/momo/apps/audio/paulstretch_python/paulstretch_newmethod.py'
root_dir = '/home/momo/music_local/source'
dest_dir = '/home/momo/music_local/stretch'
types = ['wav','WAV']
streches = ['0.25','0.5','2','10','50']

for root, dirs, files in os.walk(root_dir):
	for file in files:
		print file
		in_file = root+os.sep+file
		file_split = file.split('.')
		filename = file_split[len(file_split)-2]
		for s in streches:
			new_file = dest_dir+os.sep+filename+'_s'+s+'.wav'
			if not os.path.exists(new_file):
				os.system(stretch_app + ' -s '+s+' "'+in_file+'" "'+new_file+'"')
				

