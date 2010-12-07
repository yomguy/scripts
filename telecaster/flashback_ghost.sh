#!/bin/sh

# Live Install ISO on USB Disk /dev/sdb BOOT
# Ghost on USB Disk /dev/sdc
# Destination SSD /dev/sda

su

if [ ! -d /mnt/root/ ]; then mkdir /mnt/root; fi
if [ ! -d /mnt/ghost_root ]; then mkdir /mnt/ghost_root; fi
if [ ! -d /mnt/ghost_home ]; then mkdir /mnt/ghost_home; fi

mount /dev/sda1 /mnt/root
mount /dev/sda2 /mnt/root/home
mount /dev/sdc1 /mnt/ghost_root
mount /dev/sdc2 /mnt/ghost_home

rsync -a /mnt/ghost_root/ /mnt/root/
rsync -a /mnt/ghost_home/ /mnt/root/home/
sync

umount  /mnt/ghost_root/
umount  /mnt/ghost_home/  

# chroot MANUALLY only to CHANGE boot / fstab options
# mount -o bind /dev /mnt/root/dev
# mount -t proc none /mnt/root/proc    
# $ ls /dev/disk/by-uuid
# $ chroot /mnt/root/
# $ nano /etc/fstab
# # (edit to get right UUID, save)
# # In the chroot :
# $ grub install /dev/sda
# $ update-grub
# $ exit
# umount /mnt/root/proc
# umount /mnt/root/dev

umount /mnt/root/home 
umount /mnt/root

reboot
