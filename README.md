[![GitHub license](https://img.shields.io/github/license/smartx-usman/Distributed-Observability-Framework?logoColor=lightgrey&style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/smartx-usman/Distributed-Observability-Framework?style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/issues)
[![GitHub forks](https://img.shields.io/github/forks/smartx-usman/Distributed-Observability-Framework?style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/network)

# Distributed-Observability-Framework (DESK)
This repository contains a set of monitoring and observability tools that are being developed for infra, platform and applications performance observability.

### Prerequisites
- Kubernetes 1.23+
- Ubuntu 20.04+
- Identical OS user (e.g., user with name 'aida') on all the cluster nodes with root privileges

### Setup a Kubernetes cluster
Please follow the instructions from [Kubeadm Ansible Installation](kubernetes/README.md) to setup a cluster using kubeadm.


### Install Required Dependencies
#### Ansible on Kubernetes master node
```shell
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

#### Install Kubernetes ansible module on master node
```shell
ansible-galaxy collection install kubernetes.core
pip3 install kubernetes
```

### Before installing DESK
Modify desk-install/hosts file to specify correct IP addresses of the Kubernetes cluster nodes.

#### Create Node Label
Set label on the kubernetes nodes where these monitoring services will be installed (if not already done).
```shell
kubectl label nodes worker3 disktype=ssd ostype=normal appstype=observability flavor=large
```

#### Install DESK
Before starting the installation process, please modify install-observability-services.yaml file to enable which services you want to install. By default, all services are disabled.
```shell
cd install-desk
ansible-playbook -i hosts 00-install-desk.yaml 
```