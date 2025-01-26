#!/bin/bash

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root. Use sudo." 
   exit 1
fi


mkdir -p /opt/kosteczkator

cp kosteczkator.py /opt/kosteczkator/

cp na_nowych_final_unbalanced.keras /opt/kosteczkator/ #wstaw nazwę modelu bo może być nie aktualna

cp kosteczkator.service /etc/systemd/system

systemctl enable kosteczkator
