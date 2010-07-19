#!/usr/bin/python
# -*- coding: utf-8 -*-
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

version = '0.1'


import os
import re
import sys
import xlrd
import logging


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
            if (ext == '.mpg' or ext == '.MPG') and not file == '.' and not file == '..':
                list.append(file)
        return list


class ISPXLS:

    def __init__(self, file):
        self.first_row = 1
        self.book = xlrd.open_workbook(file)
        self.sheet = self.book.sheet_by_index(0)
        self.sources = self.get_col(0)
        self.starts_mn = self.get_col(1)
        self.starts_s = self.get_col(2)
        self.ends_mn = self.get_col(3)
        self.ends_s = self.get_col(4)
        self.forces = self.get_col(5)
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
            data[source] = {}
            data[source]['start_mn'] = self.starts_mn[i]
            data[source]['start_s'] = self.starts_s[i]
            data[source]['end_mn'] = self.ends_mn[i]
            data[source]['end_s'] = self.ends_s[i]
            data[source]['force'] = self.forces[i]
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
        self.sources = self.collection.media_list()
        self.xls_file = self.collection.xls_list()
        self.xls = ISPXLS(self.source_dir + os.sep + self.xls_file[0])
        self.trans_dict = self.xls.trans_dict()
        #print self.trans_dict

        self.format = 'flv'
        self.size = '480x270'
        self.vb = '500k'
        self.ab = '96k'
        self.ar = '44100'
        self.async = '500'

    def transcode_command(self, source_file, start_time, duration, dest_file):
        command = 'ffmpeg -ss %s -t %s -i %s -f %s -s %s -vb %s -ab %s -ar %s -async %s -y %s'  \
                  % (start_time, duration, source_file, self.format, self.size, self.vb, self.ab, self.ar, self.async, dest_file)
        return command

    def process(self):
        for source in self.trans_dict.iteritems():
            media = self.source_dir + os.sep + source[0]
            name = os.path.splitext(source[0])[0]
            dest = self.dest_dir + os.sep + name + '.' + self.format

            source_dict = source[1]
            start_mn = source_dict['start_mn']
            start_s = source_dict['start_s']
            end_mn = source_dict['end_mn']
            end_s = source_dict['end_s']
            start = int(60 * float(start_mn) + float(start_s))
            end = 60 * float(end_mn) + float(end_s)
            duration = int(end - start)
            force_mode = source_dict['force']

            if not source[0] in self.sources:
                self.logger.write_error(media, 'La source n\'existe pas !')
                continue
            else:
                if not os.path.exists(dest) or force_mode != '':
                    mess = 'Transcoding from %s:%s to %s:%s -> %s ...' % (start_mn, start_s, end_mn, end_s, dest)
                    self.logger.write_info(media, mess)
                    command = self.transcode_command(media, str(start), str(duration), dest)
                    os.system(command)


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print """
        Usage : python isp_trans.py /path/to/source_dir /path/to/transcoded_source_dir /path/to/log_file

        Dependencies : python, python-xlrd, ffmpeg

        """
    else:
        source_dir = sys.argv[-3]
        dest_dir = sys.argv[-2]
        log_file = sys.argv[-1]
        i = ISPTrans(source_dir, dest_dir, log_file)
        i.process()



