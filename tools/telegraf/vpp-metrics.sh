#!/bin/bash

# Set the file path
OUTPUT_FILE="/opt/vpp-metrics.txt"

# Create the file
sudo touch "$OUTPUT_FILE"

# Change the owner of the file to the user running the script
current_user=$(whoami)
sudo chown "$current_user" "$OUTPUT_FILE"

# Run the Linux command and capture the output
while true
do
  sudo vppctl show interface > $OUTPUT_FILE
  sleep 1
done
