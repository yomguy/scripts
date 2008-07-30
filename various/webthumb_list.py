#!/usr/bin/python
# Create thumbs of webpages from a list of URLs

# depends : webthumb, imagemagick

import os
import sys
from webthumb import get_thumbnail

img_dir = '/var/www/img/webthumbs'
site_list_file = '/var/www/img/webthumbs/webthumb_list.txt'

def main(site_list_file, img_dir):
    site_list = open(site_list_file,'r')
    for site in site_list.readlines():
        site = site[0:len(site)-1]
        print site
        get_thumbnail('http://'+site, img_dir+os.sep+site+'.png','large')
        #command = 'webthumb http://'+ site +' | pnmscale -xysize 650 400 | ' + \
        #          'pnmtopng | convert -crop 510x275+5+60 - ' + img_dir + os.sep + site +'.png'
        #print command
        #os.system(command)
    site_list.close()
    print 'Webthumbs created !'

if __name__ == '__main__':
    main(site_list_file, img_dir)
