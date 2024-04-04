#!/bin/bash

# Set the file path
RAW_FILE="/opt/vpp-metrics.txt"
OUTPUT_FILE="/opt/metrics.txt"

# Create the file
sudo touch "$OUTPUT_FILE"
sudo touch "$RAW_FILE"

# Change the owner of the file to the user running the script
current_user=$(whoami)
sudo chown "$current_user" "$OUTPUT_FILE"
sudo chown "$current_user" "$RAW_FILE"

# Run the Linux command and capture the output
while true
do
  sudo vppctl show interface > $RAW_FILE
  # Normalize line endings to Unix-style (\n)
  # This assumes the input file has Windows-style line endings (\r\n)
  tr -d '\r' < "$RAW_FILE" > "$OUTPUT_FILE"
  sleep 1
done
