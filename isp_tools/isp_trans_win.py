# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# Copyright (c) 2009-2010 Guillaume Pellerin <yomguy@parisson.com>

# This file is part of YomGuy Tools.

# TimeSide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# TimeSide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with TimeSide.  If not, see <http://www.gnu.org/licenses/>.

# Author: Guillaume Pellerin <yomguy@parisson.com>

version = '0.2'
author = 'Guillaume Pellerin'

import os
import re
import sys
import xlrd
import time
import logging

from ctypes import *

#PSAPI.DLL
psapi = windll.psapi
#Kernel32.DLL
kernel = windll.kernel32

def EnumProcesses():
    procs = []
    arr = c_ulong * 256
    lpidProcess= arr()
    cb = sizeof(lpidProcess)
    cbNeeded = c_ulong()
    hModule = c_ulong()
    count = c_ulong()
    modname = c_buffer(30)
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    
    #Call Enumprocesses to get hold of process id's
    psapi.EnumProcesses(byref(lpidProcess),
                        cb,
                        byref(cbNeeded))
    
    #Number of processes returned
    nReturned = cbNeeded.value/sizeof(c_ulong())
    
    pidProcess = [i for i in lpidProcess][:nReturned]
    
    for pid in pidProcess:
        
        #Get handle to the process based on PID
        hProcess = kernel.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ,
                                      False, pid)
        if hProcess:
            psapi.EnumProcessModules(hProcess, byref(hModule), sizeof(hModule), byref(count))
            psapi.GetModuleBaseNameA(hProcess, hModule.value, modname, sizeof(modname))
            procs.append("".join([ i for i in modname if i != '\x00']))
            
            #-- Clean up
            for i in range(modname._length_):
                modname[i]='\x00'
            
            kernel.CloseHandle(hProcess)

    #print procs
    ffmpeg_procs = 0
    for proc in procs:
        if proc == 'ffmpeg.exe':
            ffmpeg_procs += 1        
    return ffmpeg_procs

def get_pid(proc,uid):
    """Get a process pid filtered by arguments and uid"""
    (list1, list2) = os.popen4('pgrep -fl -U '+str(uid)+' '+'"'+proc+'"')
    procs = list2.readlines()
    pids = []
    if procs != '':
        for proc in procs:
            pid = proc.split(' ')[0]
            command = ' '.join(proc.split(' ')[1:])[:-1]
            pids.append(pid)
    return pids


class Logger:

    def __init__(self, file):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler(file)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def write_info(self, prefix, message):
        self.logger.info(' ' + prefix + ' : ' + message.decode('utf8'))

    def write_error(self, prefix, message):
        self.logger.error(prefix + ' : ' + message.decode('utf8'))


class ISPCollection:

    def __init__(self, dir):
        self.dir = dir
        self.dir_name = self.dir.split(os.sep)[-1]
        self.file_list = os.listdir(self.dir)

    def xls_list(self):
        file_list = []
        for file in self.file_list:
            ext = os.path.splitext(file)[1]
            if (ext == '.xls' or ext == '.XLS') and not file == '.' and not file == '..':
                file_list.append(file)
        return file_list

    def media_list(self):
        list = []
        for file in self.file_list:
            ext = os.path.splitext(file)[1]
            if (ext == '.mpg' or ext == '.MPG' or ext == '.avi' or ext == '.AVI') and not file == '.' and not file == '..':
                list.append(file)
        return list


class ISPXLS:

    def __init__(self, file):
        self.first_row = 1
        self.book = xlrd.open_workbook(file)
        self.sheet = self.book.sheet_by_index(0)
        self.cam_dirs = self.get_col(0)
        self.sources = self.get_col(1)
        self.courses = self.get_col(2)
        self.dest_names = self.get_col(3)
        self.starts_mn = self.get_col(4)
        self.starts_s = self.get_col(5)
        self.ends_mn = self.get_col(6)
        self.ends_s = self.get_col(7)
        self.forces = self.get_col(8)
        self.size = len(self.sources)

    def get_col(self, col):
        col = self.sheet.col(col)
        list = []
        for cell in col[self.first_row:]:
            #if cell.ctype == 1:
            list.append(str(cell.value))
        return list

    def trans_dict(self):
        data = {}
        i = 0
        for source in self.sources:
            data[str(i)] = {}
            data[str(i)]['cam_dir'] = self.cam_dirs[i]
            data[str(i)]['source_file'] = self.sources[i]
            data[str(i)]['course'] = self.courses[i]
            data[str(i)]['dest_name'] = self.dest_names[i]
            data[str(i)]['start_mn'] = self.starts_mn[i]
            data[str(i)]['start_s'] = self.starts_s[i]
            data[str(i)]['end_mn'] = self.ends_mn[i]
            data[str(i)]['end_s'] = self.ends_s[i]
            data[str(i)]['force'] = self.forces[i]
            i += 1
        return data


class ISPTrans(object):

    def __init__(self, source_dir, dest_dir, log_file):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        if not os.path.exists(self.dest_dir):
            os.makedirs(self.dest_dir)
        self.logger = Logger(log_file)
        
        self.collection = ISPCollection(self.source_dir)
        #self.sources = self.collection.media_list()
        self.xls_file = self.collection.xls_list()
        self.xls = ISPXLS(self.source_dir + os.sep + self.xls_file[0])
        self.trans_dict = self.xls.trans_dict()
        #print self.trans_dict

        self.format = 'flv'
        self.size = '480x270'
        self.vb = '336k'
        self.ab = '64k'
        self.ar = '44100'
        self.async = '500'

        self.server = 'parisson.com'
        self.user = 'videojur'
        self.server_dir = '/home/%s/videos/' % self.user
        
        mess = 'version %s started with the folowing parameters :' % version
        self.logger.write_info('isp_trans', mess)
        mess = 'format : %s , size : %s , vb : %s , ab : %s , ar : %s , async : %s' % \
                (self.format, self.size, self.vb, self.ab, self.ar, self.async)
        self.logger.write_info('ffmpeg', mess)

    def rsync_out(self):
        command = 'rsync -av --update %s/ %s@%s:%s/ & ' % (self.dest_dir, self.user, self.server, self.server_dir)
        os.system(command)

    def transcode_command(self, source_file, start_time, duration, dest_file):
    
        # logo inlay
        #command = 'ffmpeg -ss %s -t %s -i %s -vhook "/usr/lib/vhook/imlib2.so -x 517 -y 516 -i %s" -f %s -s %s -vb %s -acodec libmp3lame -ab %s -ar %s -async %s -y %s' % (start_time, duration, source_file, self.water_img, self.format, self.size, self.vb, self.ab, self.ar, self.async, dest_file)
            
        ## logo watermark
        #command = 'ffmpeg -ss %s -t %s -i %s -vhook "/usr/lib/vhook/watermark.so -f %s" -f %s -s %s -vb %s -acodec libmp3lame -ab %s -ar %s -async %s -y %s &' % (start_time, duration, source_file, self.water_img, self.format, self.size, self.vb, self.ab, self.ar, self.async, dest_file)
            
        # normal
        if duration == '-1':
            command = 'ffmpeg -ss %s -i "%s" -f %s -s %s -vb %s -acodec libmp3lame -ac 1 -ab %s -ar %s -async %s -y %s & ' % (start_time, source_file, self.format, self.size, self.vb, self.ab, self.ar, self.async, dest_file)
        else:
            command = 'ffmpeg -ss %s -t %s -i "%s" -f %s -s %s -vb %s -acodec libmp3lame -ac 1 -ab %s -ar %s -async %s -y %s & ' % (start_time, duration, source_file, self.format, self.size, self.vb, self.ab, self.ar, self.async, dest_file)
        return command

    def process(self):
        counter = 0
        for source in self.trans_dict.iteritems():
            source_dict = source[1]
            cam_dir = source_dict['cam_dir']
            source_file = source_dict['source_file']
            media = self.source_dir + os.sep + cam_dir + os.sep + source_file
            course = source_dict['course']
            name = str(source_dict['dest_name'])
            dest_dir = self.dest_dir + os.sep + 'videos' + course
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            dest = dest_dir + os.sep + name + '.' + self.format

            #print '<p class="decale"><a href="index.php?contenu=cours&prepa=\'.$donneeseleves[\'prepa\'].\'&matiere=%s&nomvideo=%s">%s</a></p>' % (course, name, part)
            
            start_mn = int(float(source_dict['start_mn']))
            start_s = int(float(source_dict['start_s']))
            end_mn = int(float(source_dict['end_mn']))
            end_s = int(float(source_dict['end_s']))
            start = int(60 * start_mn + start_s)
            if end_mn == -1 or end_s == -1:
                duration = -1
            else:
                end = 60 * end_mn + end_s
                duration = int(end - start)
            force_mode = source_dict['force']

            if not os.path.exists(media):
                mess = 'does NOT exists ! Continuing...'
                self.logger.write_error(media, mess)
                print media, mess
                continue
            else:
                if not os.path.exists(dest) or force_mode != '':
                    mess = 'transcoding from %s:%s to %s:%s -> %s' \
                            % (str(int(float(start_mn))), str(int(float(start_s))), str(int(float(end_mn))), str(int(float(end_s))), dest)
                    self.logger.write_info(media, mess)
                    command = self.transcode_command(media, str(start), str(duration), dest)
                    if not counter % 2:                         
                        while EnumProcesses() > 1:
                            # Only 2 threads for 2 cores and then sleeping
                            time.sleep(10)
                    os.system(command)
                    counter += 1


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print """isp_tools.py
version : %s
author : %s
Dependencies : python, python-xlrd, ffmpeg, libmp3lame0

Usage : python isp_trans.py /path/to/source_dir /path/to/transcoded_source_dir /path/to/log_file /path/to/watermark_image
""" % (version, author)
    
    else:
        source_dir = sys.argv[-3]
        dest_dir = sys.argv[-2]
        log_file = sys.argv[-1]
        i = ISPTrans(source_dir, dest_dir, log_file)
        i.process()
