#!/bin/sh
# Add your startup script

# DO NOT DELETE
echo $FLAG > /flag
/usr/sbin/sshd -D
sleep infinity;
