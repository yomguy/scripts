#!/usr/bin/python

import os
 

class Migration(object):

    def __init__(self, name, app, args=None):
        self.name = name
        self.app = app
        self.args = args

    def command(self):
        return self.app + ' ' + self.args

    def run(self):
        os.system(self.command)


class Migrator(object):

    def __init__(self, in_host, out_host):
        self.migrations = []
        self.in_host = in_host
        self.out_host = out_host

    def add(self, migration):
        self.migrations.append(migration['name'], migration['app'], migration['args'])

    def run(self):
        for migration in self.migrations:
            migration.run()



migrations = [
    {'app': 'rsync', 'args': '-aA /etc/ momo@angus.parisson.com:/home/momo/backups/ns206309/etc/'},
    {'app': 'rsync', 'args': '-aA /home/momo/backups/mysql/daily/ momo@angus:~/backups/ns206309/mysql/'},
    
    ]
    