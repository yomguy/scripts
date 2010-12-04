#!/bin/bash

mount /dev/sda1 /mnt/root
mount /dev/sda2 /mnt/root/home
mount /dev/sdc1 /mnt/ghost_root
mount /dev/sdc2 /mnt/ghost_home
rsync -a /mnt/ghost_root/ /mnt/root/
rsync -a /mnt/ghost_home/ /mnt/root/home/
sync
umount  /mnt/ghost_root/
umount  /mnt/ghost_home/
mount -o bind /dev /mnt/root/dev
mount -t proc none /mnt/root/proc
chroot /mnt/root/

grub install /dev/sda
update-grub
exit

umount /mnt/root/proc
umount /mnt/root/dev
umount /mnt/root/home 
umount /mnt/root

