#!/usr/bin/python
# Backups all zope instances (any versions)
#
# Depends : zope_instance.py
# Copyright (C) 2007-2008 Guillaume Pellerin

import os
import sys
from zope_instance import *

version = '0.2'
info = 'zope_backup v'+version+'\n'+ \
       """Copyright (C) 2007-2008 Guillaume Pellerin
       Usage: zope_backup DIRECTORY
       where DIRECTORY is the directory where you want to backup 
       the instances of the different versions of zope."""

if len(sys.argv) < 2:
    sys.exit(info)
else :
    backup_dir = sys.argv[1]

z = ZopeInstall()
instances = z.get_instances()
instance_main_dir = z.instance_main_dir

def backup_all():
    for version in instances:
    	for instance in instances[version]:
            z = ZopeInstance(version, instance)
	    print z.get_instance_dir()
            z.backup(backup_dir)
	    print version + ': ' + instance + ' backuped !'

if __name__ == '__main__':
    backup_all()
    print "Backup_all Zopes done !"

    
        
