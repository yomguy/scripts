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
            if ext == '.xls' or ext == '.XLS':
                file_list.append(file)
        return file_list

    def wav_list(self):
        list = []
        for file in self.file_list:
            ext = os.path.splitext(file)[1]
            if ext == '.wav' or ext == '.WAV':
                list.append(file)
        return list


class ISPXLS:

    def __init__(self, file):
        self.first_row = 8
        self.original_col = 0
        self.new_col = 1
        self.book = xlrd.open_workbook(file)
        self.sheet = self.book.sheet_by_index(0)
        self.original_refs = self.original_refs()
        self.new_refs = self.new_refs()
        #print len(self.new_refs)
        while True:
            if len(self.original_refs) == 0 or len(self.new_refs) == 0:
                break
            else:
                if not 'CNRS' in self.new_refs[0].encode('utf8') \
                 and not  self.original_refs[0].encode('utf8') == '':
                    self.original_refs = self.original_refs[1:]
                    self.new_refs = self.new_refs[1:]
                else:
                    break

        self.size = max(len(self.new_refs), len(self.original_refs))

    def original_refs(self):
        col = self.sheet.col(self.original_col)
        list = []
        for cell in col[self.first_row:]:
            if cell.ctype == 1:
                list.append(cell.value)
        return list

    def new_refs(self):
        col = self.sheet.col(self.new_col)
        list = []
        for cell in col[self.first_row:]:
            if cell.ctype == 1:
                list.append(cell.value)
        return list


class ISPItemFile:

    def __init__(self):
        self.media = ''

    def set_media(self, media):
        self.media = media

    def is_wav(self):
        try:
            audio_file = audiolab.Sndfile(self.media, 'r')
            if audio_file.nframes and audio_file.nframes != 0:
                return True
        except IOError:
            return False

    def properties(self):
        self.frames = self.audio_file.get_nframes()
        self.samplerate = self.audio_file.get_samplerate()
        self.channels = self.audio_file.get_channels()
        self.format = self.audio_file.get_file_format()
        self.encoding = self.audio_file.get_encoding()


class ISPTrans(object):

    def __init__(self, media_dir, img_dir):
        self.root_dir = media_dir
        self.img_dir = img_dir
        self.scheme = GrapherScheme()
        self.width = self.scheme.width
        self.height = self.scheme.height
        self.bg_color = self.scheme.bg_color
        self.color_scheme = self.scheme.color_scheme
        self.force = self.scheme.force

        self.media_list = self.get_media_list()
        if not os.path.exists(self.img_dir):
            os.mkdir(self.img_dir)
        self.path_dict = self.get_path_dict()

    def get_media_list(self):
        media_list = []
        for root, dirs, files in os.walk(self.root_dir):
            if root:
                for file in files:
                    ext = file.split('.')[-1]
                    if ext == 'mp3' or ext == 'MP3':
                        media_list.append(root+os.sep+file)
        return media_list

    def get_path_dict(self):
        path_dict = {}
        for media in self.media_list:
            name = os.path.splitext(media)
            name = name[0].split(os.sep)[-1]
            path_dict[media] = self.img_dir + os.sep + name + '.png'
        return path_dict

    def process(self):
        for source, image in self.path_dict.iteritems():
            if not os.path.exists(image) or self.force:
                print 'Rendering ', source, ' to ', image, '...'
                audio = os.path.join(os.path.dirname(__file__), source)
                decoder  = timeside.decoder.FileDecoder(audio)
                waveform = timeside.grapher.Waveform(width=self.width, height=self.height, output=image,
                                            bg_color=self.bg_color, color_scheme=self.color_scheme)
                (decoder | waveform).run()
                print 'frames per pixel = ', waveform.graph.samples_per_pixel
                waveform.render()


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print """
        Usage : python isp_trans.py /path/to/media_dir /path/to/transcoded_media_dir

        Dependencies : python, python-xlrd, ffmpeg

        """
    else:
        media_dir = sys.argv[-2]
        trans_dir = sys.argv[-1]
        i = ISPTrans(media_dir, trans_dir)
        i.process()



