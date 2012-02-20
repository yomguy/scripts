#!/usr/bin/python
#
# Depends : zope_instance.py
# Copyright (C) 2007-2008 Guillaume Pellerin

import os
import sys
from zope_instance import *

version = '0.2'
info = 'zope_check v'+version+'\n'+ \
       """Copyright (C) 2007-2008 Guillaume Pellerin
       Usage: zope_backup DIRECTORY
       where DIRECTORY is the directory where you want to backup 
       the instances of the different versions of zope."""

#if len(sys.argv) < 2:
#    sys.exit(info)
#else :
#    backup_dir = sys.argv[1]

z = ZopeInstall()
instances = z.get_instances()
instance_main_dir = z.instance_main_dir

def get_zope_port(main_dir):
    conf_path = main_dir + os.sep + 'etc' + os.sep + 'zope.conf'
    conf = open(conf_path, 'r')
    lines = conf.readlines()
    for line in lines:
        if 'HTTPPORT' in line:
	    return main_dir+': ' + line

def check_all():
    for version in instances:
    	for instance in instances[version]:
            z = ZopeInstance(version, instance)
	    print get_zope_port(z.get_instance_dir())

if __name__ == '__main__':
    check_all()

    
        
