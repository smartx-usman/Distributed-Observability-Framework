# Install microstack on all servers
sudo snap install microstack --devmode --beta

# Initialize microstack on controller node
sudo microstack init --auto --control --setup-loop-based-cinder-lvm-backend --loop-device-file-size 120

# Generate connection string
sudo microstack add-compute

# Initialize microstack on compute nodes
sudo microstack init --auto --compute --join <connection-string>

# Get key
sudo snap get microstack config.credentials.keystone-password
