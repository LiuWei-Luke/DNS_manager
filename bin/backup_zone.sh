#!/bin/bash

for F in /var/named/*.zone;
do cp -vp ${F} /root/backups;done

tar -zcvf /root/backups/zone.tar.gz /root/backups/*.zone