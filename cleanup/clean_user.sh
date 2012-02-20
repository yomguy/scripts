#!/bin/sh

u=$1
sudo deluser $u
sudo rm -rf /home/$u

