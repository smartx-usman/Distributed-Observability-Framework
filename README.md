[![GitHub license](https://img.shields.io/github/license/smartx-usman/Distributed-Observability-Framework?logoColor=lightgrey&style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/smartx-usman/Distributed-Observability-Framework?style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/issues)
[![GitHub forks](https://img.shields.io/github/forks/smartx-usman/Distributed-Observability-Framework?style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/network)

# Distributed-Observability-Framework (DESK)
This repository contains a set of monitoring and observability tools that are being developed for AIDA project.

### Prerequisites
- Kubernetes 1.23+
- Ubuntu 20.04+

### Setup a Kubernetes cluster
Please follow the instructions from [Kubeadm Ansible Installation](kubernetes/README.md) to setup a cluster using kubeadm.


### Install Ansible on Kubernetes master node
```shell
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

### Install Kubernetes ansible module on master node
```shell
ansible-galaxy collection install kubernetes.core
pip3 install kubernetes
```

### Before installing DESK
Modify desk-install/hosts file to specify correct IP addresses of the Kubernetes cluster nodes.

### Install DESK
```shell
ansible-playbook -i install-desk/hosts install-desk/main.yaml
```