#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, stat, time

root = sys.argv[-1]

folders = list(os.walk(root))[1:]
folders.sort()

for folder in folders:
    if not folder[2] and not folder[1]:
        os.rmdir(folder[0])

