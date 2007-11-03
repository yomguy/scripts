#!/usr/bin/python
# Create thumbs of webpages from a list of URLs

# depends : webthumb, imagemagick

import os
import sys

img_dir = '/var/www/img/thumbs'
site_list_file = '/var/www/img/thumbs/url_list.txt'

def main(site_list_file, img_dir):
    site_list = open(img_dir + os.sep + site_list_file,'r')
    for site in site_list.readlines():
        site = site[0:len(site)-1]
        command = 'webthumb http://'+ site +' | pnmscale -xysize 650 400 | ' + \
                  'pnmtopng | convert -crop 510x275+5+60 - ' + site +'.png'
        print command
        os.system(command)
    site_list.close()
    print 'Webthumbs created !'

if __name__ == '__main__':
    main(site_list_file, img_dir)