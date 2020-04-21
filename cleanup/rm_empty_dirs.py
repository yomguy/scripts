#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, stat, time

root = sys.argv[-1]

folders = list(os.walk(root))[1:]

for folder in folders:
    # folder example: ('FOLDER/3', [], ['file'])
    if not folder[2]:
        os.rmdir(folder[0])

