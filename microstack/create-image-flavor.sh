# Fetch cloud images
wget https://cloud.debian.org/images/cloud/bullseye/latest/debian-11-generic-amd64.qcow2
wget https://cloud-images.ubuntu.com/focal/current/focal-server-cloudimg-amd64.img
wget https://cloud-images.ubuntu.com/releases/jammy/release/ubuntu-22.04-server-cloudimg-amd64.img

# Create Ubuntu 20.04/22.04 and Debian 9 images
microstack.openstack image create --file focal-server-cloudimg-amd64.img --disk-format qcow2 \
        --container-format bare --public ubuntu20.04
microstack.openstack image create --file jammy-server-cloudimg-amd64.img --disk-format qcow2 \
        --container-format bare --public ubuntu22.04
microstack.openstack image create --file debian-11-generic-amd64.qcow2 --disk-format qcow2 \
        --property os_type=linux --property os_distro=debian --property os_admin_user=debian \
        --container-format bare --public debian-11

# Create flavors
microstack.openstack flavor create m2.tiny --id 6 --ram 1024 --disk 10 --vcpus 1 --rxtx-factor 1
microstack.openstack flavor create m2.small --id 7 --ram 4096 --disk 80 --vcpus 2 --rxtx-factor 1
microstack.openstack flavor create m2.large --id 8 --ram 8192 --disk 120 --vcpus 4 --rxtx-factor 1