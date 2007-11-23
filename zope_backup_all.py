#!/usr/bin/python
# Backups all zope instances (any versions)
#
# Depends : zope_instance.py

import os
import sys
from zope_instance import *


backup_dir = '/home/momo/backups/zope/'

z = ZopeInstall()
versions = z.versions
instance_main_dir = z.instance_main_dir

def backup_all():
    for version in versions:
       dir = instance_main_dir + os.sep + 'zope' + version + os.sep + 'instance'
       if os.path.exists(dir):
           instances = os.listdir(dir)
           for instance in instances:
               z = ZopeInstance(version, instance)
               z.backup(backup_dir)
	       #print instance 

if __name__ == '__main__':
    backup_all()
    print "Backup_all Zopes done !"

    
        
