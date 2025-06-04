#!/bin/bash

# NOTE: you may have to run this script as a superuser (sudo ./setup.sh)

# if cron is not installed, install it
if ! sudo apt list --installed | grep -Fq "cron"; then
  echo "Installing cron..."
  sudo apt update && sudo apt install -y cron
fi

# 6:30 AM Monday-Friday
CRON_JOB="30 6 * * 1-5 python3 main.py >> crontab -e"

# Don't allow repeat cron jobs to be added
if crontab -l | grep -Fq "python3 main.py"; then
  echo "Cron job already exists."
else
  (crontab -l; echo "$CRON_JOB") | crontab -
fi