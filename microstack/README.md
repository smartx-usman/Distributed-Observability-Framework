# Instructions for Provisioning a Microstack Cluster
These are the instructions to setup a lightweight Kubernetes cluster using Microstack.

## Provision cluster
Execute the commands from [provision-microstack-cluster.sh](provision-microstack-cluster.sh)

## Provision VMs
Execute the commands from [provision-microstack-vms.sh](provision-microstack-vms.sh)

## Create labels for nodes after Kubernetes cluster is up
Execute the commands from [create-labels.sh](create-labels.sh)


### Example how to modify cloud image to create a new user and add ssh key
- First get the cloud image from https://cloud-images.ubuntu.com/releases/20.04/release/

- Next run the following commands to modify the image and don't forget to change the ssh key.

    ```bash
    sudo guestfish --rw -a jammy-server-cloudimg-amd64.img
    ><fs> run
    ><fs> list-filesystems
    /dev/sda1: ext4
    ><fs> mount /dev/sda1 /
    ><fs> vi /etc/cloud/cloud.cfg
    users:
      - default
      - name: aida
        passwd: "aida"
        shell: /bin/bash
        lock-passwd: false
        ssh_pwauth: True
        chpasswd: { expire: False }
        sudo: ALL=(ALL) NOPASSWD:ALL
        groups: users, admin
        ssh_authorized_keys:
         - ssh-rsa xyz= abc@test-server
    
    #><fs> exit
    ```
### Installing DESK
Once MicroStack cluster is setup, you can follow DESK installation instructions from [here](../README.md).