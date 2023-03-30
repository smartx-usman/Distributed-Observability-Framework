# Instructions for Provisioning a Microstack Cluster
These are the instructions to setup a lightweight Kubernetes cluster using Microstack.

### Provision Microstack cluster
Execute the commands from [provision-microstack-cluster.sh](provision-microstack-cluster.sh)

### Create Images and Flavors for VMs
Execute the commands from [create-image-flavor.sh](create-image-flavor.sh)

### Provision VMs
Execute the commands from [provision-microstack-vms.sh](provision-microstack-vms.sh)

### Provisioning K8S Cluster Using Provisioned VMs
Once MicroStack cluster is up, you can follow k8s installation instructions from [here](../kubernetes/README.md).

### Create Labels for Nodes after Kubernetes Cluster is UP
Execute the commands from [create-labels.sh](create-labels.sh) 

### Installing DESK
Once k8s cluster is up, you can follow DESK installation instructions from [here](../README.md).


### Additional: Modify Cloud VM Image to Create a New User and Add SSH Key
If you are unable to access VM using the ssh key provided by MicroStack, you can modify the cloud image to create a new user and add your ssh key.

- First go to the directory where your cloud image resides.

- Next run the following commands to modify the image (e.g., jammy-server-cloudimg-amd64.img) and don't forget to change the ssh key. Also, make sure correct indentation after copying and pasting the below code in the cloud.cfg file.

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
    
    ><fs> exit
    ```