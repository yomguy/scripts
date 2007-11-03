#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 Guillaume Pellerin <yomguy@parisson.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Guillaume Pellerin <yomguy@parisson.com>


import os
import sys
from optparse import OptionParser


class ZopeInstance:
    """Expose Zope instances to several python methods that simplifies admins' life
    (backup, recover, import, etc...)"""
    
    def __init__(self, version, instance, backup_dir):
        self.backup_dir = backup_dir
        self.versions = ['2.7', '2.9', '2.8', '2.10']
        self.instance_main_dir = '/var/lib'
        self.zope_main_dir = '/usr/lib'
          
        self.version = version
        self.instance = instance
        self.instance_dir = self.instance_main_dir + os.sep + 'zope' + version + os.sep + \
                        'instance' + os.sep + self.instance
        self.instance_data = self.instance_dir + os.sep + 'var' + os.sep + 'Data.fs'
        self.instance_products =self.instance_dir + os.sep + 'Products' + os.sep
        self.instance_var =self.instance_dir + os.sep + 'var' + os.sep
        self.instance_backup_dir = self.backup_dir + os.sep + version + os.sep + instance
        self.repozo = self.zope_main_dir + os.sep + 'zope' + self.version + os.sep + 'bin' + os.sep + 'repozo.py'

    def get_instances(self):
        dict = {}
        for version in self.versions:
            #print version
            path = self.instance_main_dir + os.sep + 'zope' + version + os.sep + 'instance'
            if os.path.exists(path):
                dict[version] = os.listdir(path)
                #print dict
        return dict

    def backup(self):
        path = self.instance_backup_dir+ os.sep + 'Data'
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(self.instance_data):
            command = 'sudo ' + self.repozo +' -Bvz -r ' + path + ' -f ' + self.instance_data
            os.system(command)
            command = 'sudo chmod 700 ' + path + os.sep + '*'
            os.system(command)
        else:
            print self.instance_data + ' does not exists !'
        if not os.path.exists(self.instance_backup_dir):
            os.makedirs(self.instance_backup_dir)
        if os.path.exists(self.instance_products):
            command = 'sudo tar czf ' + self.instance_backup_dir + os.sep + \
                      'Products.tar.gz ' + self.instance_products
            os.system(command)
        if os.path.exists(self.instance_var):
            command = 'sudo tar czf --exclude="Data.fs" ' + self.instance_backup_dir + os.sep + \
                      'var.tar.gz ' + self.instance_var
            os.system(command)
        print self.instance + ' backuped !'

    def recover(self):
        command = 'sudo ' + self.repozo + ' -Rvz -r ' + self.instance_backup_dir + os.sep + \
                    'Data -o ' + self.instance_data
        if os.path.exists(self.instance_data):
            os.system(command)
        else:
            print self.instance_data + ' does not exists !'
        os.chdir(self.instance_backup_dir)
        command = 'sudo tar xzf '+self.instance_backup_dir+os.sep+'Products.tar.gz && ' + \
                  'sudo rsync -a --delete ' + self.instance_backup_dir+os.sep+self.instance_products + \
                               ' ' + self.instance_products + os.sep + ' && ' + \
                  'sudo chown -R zope:zope ' + self.instance_products + ' && ' + \
                  'sudo rm -rf ' + self.instance_backup_dir+os.sep+'var'
        os.system(command)
        command = 'sudo tar xzf '+self.instance_backup_dir+os.sep+'var.tar.gz && ' + \
                  'sudo rsync -a --delete ' + self.instance_backup_dir + os.sep  + self.instance_var + \
                                ' ' + self.instance_var + os.sep + ' && ' + \
                  'sudo chown -R zope:zope ' + self.instance_var + ' && ' + \
                  'sudo rm -rf ' + self.instance_backup_dir+os.sep+'var'
        os.system(command)
        command = 'sudo ' + self.instance_dir+os.sep+'bin'+os.sep+'zopectl restart'            
        os.system(command)
        print self.instance + ' recovered !'

        
    def import_from(self, user, server):
        command = 'sudo rsync -a --rsh="ssh -l '+user+'" ' + \
                  user+'@'+server+':'+self.instance_backup_dir+os.sep + ' ' + self.instance_backup_dir+os.sep
        os.system(command)

    def export_to(self, user, server):
        command = 'sudo rsync -a --rsh="ssh -l '+user+'" ' + \
                  self.instance_backup_dir+os.sep  + ' ' + user+'@'+server+':'+self.instance_backup_dir+os.sep
        os.system(command)


