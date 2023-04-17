#!/bin/bash

Red='\033[0;31m'
Green='\e[32m'
Yellow='\033[0;33m'
Blue='\e[34m'
BBlue='\e[44m'
FDefault='\e[49m'

LOGFILE="./deps-log.log"
exec 3>&1 1>"$LOGFILE" 2>&1

set -ex # Prints commands, prefixing them with a character stored in an environmental variable ($PS4)

trap "echo -e '$Red ERROR: An error occurred during execution, check log $LOGFILE for details.' >&3" ERR
trap '{ set +x; } 2>/dev/null; echo -n "[$(date -Is)]  "; set -x' DEBUG

echo -e "$Yellow Installing required tools for initiating DESK deployment..." >&3
echo -e "$BBlue Install Python3 pip" >&3
sudo apt install -y ansible python3-pip

echo -e "$BBlue Install Ansible" >&3
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible

echo -e "$BBlue Install Kubernetes ansible module $FDefault" >&3
ansible-galaxy collection install kubernetes.core
pip3 install kubernetes

echo -e "\n" >&3
echo -e "$Green Successfully installed required tools for initiating DESK deployment.\n" >&3