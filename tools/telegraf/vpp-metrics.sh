#!/bin/bash

# Set the file path
INTERFACE_RAW_FILE="/opt/vpp-interface-metrics.txt"
INTERFACE_OUTPUT_FILE="/opt/interface_metrics.txt"
RATE_RAW_FILE="/opt/vpp-rate-metrics.txt"
RATE_OUTPUT_FILE="/opt/vpp_rate.txt"

# Create the output files
sudo touch "$INTERFACE_OUTPUT_FILE" "$INTERFACE_RAW_FILE" "$RATE_OUTPUT_FILE" "$RATE_RAW_FILE"

# Change the owner of the file to the user running the script
current_user=$(whoami)
sudo chown "$current_user" "$INTERFACE_RAW_FILE"
sudo chown "$current_user" "$INTERFACE_OUTPUT_FILE"
sudo chown "$current_user" "$RATE_RAW_FILE"
sudo chown "$current_user" "$RATE_OUTPUT_FILE"

# Run the Linux commands and capture the output
while true
do
  sudo vppctl show interface > $INTERFACE_RAW_FILE
  sudo vppctl show runtime | grep memif0 > $RATE_RAW_FILE

  # Normalize line endings to Unix-style (\n)
  # This assumes the input file has Windows-style line endings (\r\n)
  tr -d '\r' < "$INTERFACE_RAW_FILE" > "$INTERFACE_OUTPUT_FILE"
  tr -d '\r' < "$RATE_RAW_FILE" > "$RATE_OUTPUT_FILE"
  sleep 5
done
