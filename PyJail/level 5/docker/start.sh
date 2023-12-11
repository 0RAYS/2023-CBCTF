#!/bin/sh
# Add your startup script

# DO NOT DELETE
echo $FLAG>/flag
/etc/init.d/xinetd start;
sleep infinity;
rm -rf start.sh