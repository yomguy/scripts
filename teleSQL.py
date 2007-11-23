#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007-2007 Guillaume Pellerin <yomguy@parisson.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/d-fuzz/DFuzzLicense.
#
# Author: Guillaume Pellerin <yomguy@parisson.com>


import os
import sys
import datetime
import codecs
import string
import MySQLdb
from sqltools import *


class TeleSQL:

    def __init__(self, db1, db2):
        self.db1 = db1['db']
        self.host1 = db1['host']
        self.user1 = db1['user']
        self.passwd1 = db1['passwd']
        self.port1 = int(db1['port'])

        self.db2 = db2['db']
        self.host2 = db2['host']
        self.user2 = db2['user']
        self.passwd2 = db2['passwd']
        self.port2 = int(db2['port'])
        
        self.sql_db1 = sql_db(self.db1, self.host1, self.user1, self.passwd1, self.port1)
        self.sql_db2 = sql_db(self.db2, self.host2, self.user2, self.passwd2, self.port2)
            
    def upgrade_secondary_table(self, dict):
        """Update incremental tables in colums of the DB n°2 from some colums in
        the main DB n°1 respectively to a given filter dictionnary (see example below)"""

        table1 = dict['table1']
        table2 = dict['table2']
        col1tocol2 = dict['col1tocol2']
        filter_dict = filetodict(dict['filter'])
        default_value = dict['default']
        
        col1 = col1tocol2.keys()
        col1 = col1[0]
        col2 = col1tocol2[col1]
        print table1 + ' ('+col1+') => '+table2+' ('+ col2 +')'
        
        data1_t = sql_command_fetch(self.sql_db1, "SELECT " + col1 + " from %s.%s " % (self.db1, table1))
        #print data1_t
        data1_l = tuple2list2_latin(data1_t)
        #print data1_l

        data2_t = sql_command_fetch(self.sql_db2, "SELECT " + col2 + " from %s.%s " % (self.db2, table2))
        data2_l = tuple2list2_latin(data2_t)
        data2_l_low = tuple2list2_low_latin(data2_t)
        data2_l_cap = tuple2list2_cap_latin(data2_t)

        count = 0
        wrong_data = open(self.db2 + '_' + table2 + '_bonus' +'.csv','w')
        
        for data in data1_l:
            data = unicode(data)
            data_corr = get_data_corr(data, filter_dict)
            #print data_corr
                
            if not data_corr in data2_l and \
                not data_corr.lower() in data2_l_low and \
                not data_corr.lower() in data2_l and \
                not data_corr.capitalize() in data2_l_cap and \
                not data_corr.capitalize() in data2_l:

                db2c = self.sql_db2.cursor()
                db2c.execute("INSERT INTO "+table2+" ("+col2+") VALUES (%("+col2+")s)", {col2: data_corr})
                #print 'INSERTED'
                data2_t = sql_command_fetch(self.sql_db2, "SELECT " + col2 + " from %s.%s" % (self.db2, table2))
                data2_l = tuple2list2_latin(data2_t)
                data2_l_low = tuple2list2_low_latin(data2_t)
                data2_l_cap = tuple2list2_cap_latin(data2_t)
                count = count + 1
                wrong_data.write(data_corr.encode('utf-8')+'\n')
            else:
                pass
                #print 'EXISTS'

        print table2 + ': ' +str(count) +' updated'
        print '========================================================================'
        wrong_data.close()
        self.sql_db2.commit()
        self.sql_db1.close()
        self.sql_db2.close()



    def update_main_table(self, dict):
        
        table1 = dict['table1']
        table2 = dict['table2']
        col1tocol2 = dict['col1tocol2']
        date_limit = dict['date_limit']
        meta_dict = dict['meta_dict']
        
        col1_t = sql_command_fetch(self.sql_db1,'SHOW columns from '+ self.db1 + '.' + table1)
        #print col1_t
        col1_l = []
        for col in col1_t:
            col1_l.append(col[0])

        col2_t = sql_command_fetch(self.sql_db2,'SHOW columns from '+ self.db2 + '.' + table2)
        #print col2_t
        col2_l = []
        for col in col2_t:
            col2_l.append(col[0])
        
        print "-----------------------------------------"
        print 'Table 1:'
        print col1_l
        print 'Table 2:'
        print col2_l

        # Fetch all data
        data1_t = sql_command_fetch(self.sql_db1, """SELECT * from %s.%s """ % (self.db1, table1))
        data2_t = sql_command_fetch(self.sql_db2, """SELECT * from %s.%s """ % (self.db2, table2))

        #sys.exit()
        
        dates_ok = 0
        dates = 0

        for data in data1_t:
            
            #print data
            dict_1 = tuple2dict(col1_l, data)
            #print dict_1
            dict_2 = tuple2dict(col2_l)
            #print dict_3
            dict_2 = dict1todict2(dict_1, col1tocol2, dict_2)
            
            #print meta_dict.keys()

            for item in meta_dict.keys():
                #print item
                item_table = meta_dict[item]['table']
                item_default = meta_dict[item]['default']
                item_cols = sql_command_fetch(self.sql_db1,'SHOW columns from '+ self.db2 + '.' + item_table)
                item_cols_l = []
                for col in item_cols:
                    item_cols_l.append(col[0])
                
                item_data = sql_command_fetch(self.sql_db2, """SELECT * from %s.%s """ % (self.db2, item_table))
                item_data_d = []
                for dat in item_data:
                    item_data_d.append(tuple2dict(item_cols_l, dat))
                    
                #item_data_d = tuple2dict(item_data)
                item_dict = filetodict(meta_dict[item]['filter'])
                item_value = dict_1[item].decode('latin1')
                item_id_name = meta_dict[item]['id']

                #print item_dict
                
                if item_value in item_dict.keys():
                    item_value = get_data_corr(item_value, item_dict, item_default)
                
                for value in item_data_d:
                    #print value
                    value_new = value['nom'].decode('latin1')
                    if item_value ==  value_new or \
                        item_value ==  value_new.lower() or \
                        item_value ==  value_new.capitalize() or \
                        item_value.lower() ==  value_new.lower() or \
                        item_value.capitalize() ==  value_new.capitalize():

                        #print item_value +': ' + item_id_name + ' = ' + str(value['id'])
                        dict_2[item_id_name] = value['id']

            db2c = self.sql_db2.cursor()
            db2c.execute("""INSERT INTO emissions (titre, date_diffusion, realisateur_id, duree, genre_id, resume, master, position, radio_id) VALUES (%(titre)s, %(date_diffusion)s, %(realisateur_id)s, %(duree)s, %(genre_id)s, %(resume)s, %(master)s, %(position)s, %(radio_id)s)""", dict_2)
            dates_ok = dates_ok + 1
            dates = dates + 1
            #print dates

            #if dates == 10:
            #    break

        self.sql_db2.commit()
        self.sql_db1.close()
        self.sql_db2.close()

        print "--------------------------------------------"
        print "Number of items inserted :" + str(dates_ok)
        print "Total number of items :" + str(dates)
       

# -----------------------------------------------

db1 = {'host':   'localhost',
          'user':    'epra',
          'passwd':  'testepra',
          'db':      'epra_fm',
          'port':    '3306'}


#db1 = {'host':   '66.70.82.200',
          #'user':    'eprafr',
          #'passwd':  'trc47AM9',
          #'db':      'eprafr',
          #'port':    '3306'}


db2 = {'host':   'localhost',
          'user':    'epra',
          'passwd':  'testepra',
          'db':      'epra',
          'port':    '3306'}

vector1 = {'table1': 'diffusions',
            'table2': 'radios',
            'col1tocol2': {'station': 'nom'},
            'default': 'Radio',
            'filter': 'FM.Stations_filter_2.csv'}

vector2 = {'table1': 'diffusions',
            'table2': 'realisateurs',
            'col1tocol2': {'auteur': 'nom'},
            'default': '',
            'filter': 'FM.Realisateurs_filter.csv',
            'split': '1'}

vector3 = {'table1': 'diffusions',
            'table2': 'genres',
            'col1tocol2': {'genre': 'nom'},
            'default': '',
            'filter': 'FM.Genres_filter.csv'}

vector4 = {'table1': 'diffusions',
           'table2': 'emissions',
           'col1tocol2': {'titre': 'titre',
                        'date_diffusion': 'datedifsat' ,
                        'duree': 'dureedif',
                        'resume': 'resume',
                        'master': 'nummaster',
                        'position': 'positionsat'},
           'date_limit': '20021201',
           'meta_dict': {'station': {'table': 'radios', 'id': 'radio_id', 'default':'Radio', 'filter': 'FM.Stations_filter_2.csv'},
                           'genre': {'table': 'genres', 'id': 'genre_id', 'default': '', 'filter': 'FM.Genres_filter.csv'},
                           'auteur': {'table': 'realisateurs', 'id': 'realisateur_id', 'default': '', 'filter': 'FM.Realisateurs_filter.csv'}
                           }}

secondary_vectors = (vector1, vector2, vector3)
main_vector = vector4


def main():    
    for vector in secondary_vectors:
        sql_db = TeleSQL(db1, db2)
        sql_db.upgrade_secondary_table(vector)
    sql_db = TeleSQL(db1, db2)
    sql_db.update_main_table(main_vector)
    print 'Done !'
    
if __name__ == '__main__':
    main()
            
