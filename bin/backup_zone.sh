#!/bin/bash

for F in /var/named/*.zone;
do cp -vp ${F} /root/backups;done

tar -zcvf /home/backups/zone.tar.gz /home/backups/*.zone