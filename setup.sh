#!/bin/bash

# NOTE: you may have to run this script as a superuser (sudo ./setup.sh)

# if cron is not installed, install it
if ! sudo apt list --installed 2>/dev/null | grep -Fq "cron"; then
  echo "Installing cron..."
  sudo apt update && sudo apt install -y cron
fi

# this will get the dirname for where setup.sh is located, relative to your current working directory, 
# cd into it then pwd and get the absolute path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# echo "${SCRIPT_DIR}"

# 6:00 AM Monday-Friday
CRON_JOB="00 6 * * 1-5 python3 ${SCRIPT_DIR}/main.py"

# Don't allow repeat cron jobs to be added
if crontab -l | grep -Fq "python3 ${SCRIPT_DIR}/main.py"; then
  echo "Cron job already exists."
else
  # pipe the current cronjobs with the new one then replace the crontab with the new list
  (crontab -l; echo "$CRON_JOB") | crontab -
fi