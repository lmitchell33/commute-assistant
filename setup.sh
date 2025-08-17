#!/usr/bin/env bash

echo "--- Setting up the Commute Assistant ---"

if ! apt list --installed 2>/dev/null | grep -Fq "cron"; then
  echo "Please install cron before running this script: sudo apt install cron"
  exit 1
fi

# Prompt the user for the necessary address/information
DEFAULT_START="5947 Southland Drive, Erie, PA, 16509"
DEFAULT_END="1010 Murry Ridge Ln, Murrsville, PA 15668"
DEFAULT_METHOD="WALK"
DEFAULT_TIME="0 5 * * 1-5"  # Default to 5 AM on weekdays

read -p "Start address [1234 Example Street, City, State, Zip]: " START
START="${START:-$DEFAULT_START}"

read -p "End address [1234 Example Street, City, State, Zip]: " END
END="${END:-$DEFAULT_END}"

if [[ -z "$START" || -z "$END" ]]; then
  echo "Both start and end addresses are required. Please ensure the form you provide follows the designated pattern."
  exit 1
fi

read -p "Travel method [DRIVE, WALK, BICYCLE, TRANSIT]: " METHOD
METHOD="${METHOD:-$DEFAULT_METHOD}"

if [[ ! "$METHOD" =~ ^(DRIVE|WALK|BICYCLE|TRANSIT)$ ]]; then
  echo "Invalid travel method. Please choose from DRIVE, WALK, BICYCLE, or TRANSIT."
  exit 1
fi

read -p "Notification time [min hour day months days_of_week]: " TIME
TIME="${TIME:-$DEFAULT_TIME}"

CRON_REGEX='^([0-9*,-/]+)\s+([0-9*,-/]+)\s+([0-9*,-/]+)\s+([0-9*,-/]+)\s+([0-9*,-/]+)$'
if [[ ! "$TIME" =~ $CRON_REGEX ]]; then
    return 1
fi

# for now, default to 5 AM on weekdays
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_JOB="$TIME python3 $SCRIPT_DIR/main.py \
  --start \"$START\" \
  --end \"$END\" \
  --method \"$METHOD\""

echo "-- Full cron job to be added: $CRON_JOB ---"

# Don't allow repeat cron jobs to be added
if crontab -l | grep -Fq "$CRON_JOB"; then
  echo "Cron job already exists."
  exit 0
else
  (crontab -l; echo "$CRON_JOB") | crontab -
fi

echo "--- Successfully added cron job ---"