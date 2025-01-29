#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Use sudo." 
   exit 1
fi

systemctl disable --now fan

rm /etc/systemd/system/fan.service

rm -r /opt/fan
