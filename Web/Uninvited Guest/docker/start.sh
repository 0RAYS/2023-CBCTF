#!/bin/bash

echo $FLAG > /flag
chown root:root /flag && chmod 400 /flag
su node
npm run start
sleep infinity
