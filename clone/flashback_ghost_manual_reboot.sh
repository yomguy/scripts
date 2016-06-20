#!/bin/sh

# Live Install ISO on USB Disk /dev/sdb BOOT
# Ghost on USB Disk /dev/sdc
# Destination SSD /dev/sda

umount /mnt/root/proc
umount /mnt/root/dev

umount /mnt/root/home 
umount /mnt/root

reboot
