#!/bin/bash

# http://www.cybercrimetech.com/2014/08/how-to-brute-forcing-password-cracking.html

# Using john the ripper to brute-force a luks container
startTime=$(date)
if [ $(file $1 | grep -c "LUKS encrypted file") ]; then
    john -i --stdout | while read i; do
        echo -ne "\rtrying \"$i\" "\\r
        # as root
        echo $i | cryptsetup luksOpen $1 x --test-passphrase -T1 2> /dev/null
        STATUS=$?
        if [ $STATUS -eq 0 ]; then
          echo -e "\nPassword is: \"$i\""
          break
        fi
    done
    echo "Start time $startTime"
    echo "End time $(date)"
else
        echo "The file does not appear to be a LUKS encrypted file"
fi
