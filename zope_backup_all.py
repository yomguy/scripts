#!/usr/bin/python
# Backups all zope instances (any versions)
#
# Depends : zope_instance.py

import os
import sys
from zope_instance import *


backup_dir = '/home/momo/backups/zope/'

z = ZopeInstall()
instances = z.get_instances()
instance_main_dir = z.instance_main_dir

def backup_all():
    for version in instances:
    	for instance in instances[version]:
            z = ZopeInstance(version, instance)
            #z.backup(backup_dir)
	    print version + ': ' + instance + ' backuped !'

if __name__ == '__main__':
    backup_all()
    print "Backup_all Zopes done !"

    
        
