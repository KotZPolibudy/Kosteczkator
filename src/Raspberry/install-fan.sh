#!/bin/bash

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Use sudo." 
   exit 1
fi


mkdir -p /opt/fan

cp fan.py /opt/fan/

cp fan.service /etc/systemd/system

systemctl enable fan
