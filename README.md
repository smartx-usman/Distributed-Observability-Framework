[![GitHub license](https://img.shields.io/github/license/smartx-usman/Distributed-Observability-Framework?logoColor=lightgrey&style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/smartx-usman/Distributed-Observability-Framework?style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/issues)
[![GitHub forks](https://img.shields.io/github/forks/smartx-usman/Distributed-Observability-Framework?style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/network)

# AIDA-Distributed-Observability-Framework
A set of monitoring and observability tools that are being developed for AIDA project.

### Prerequisites
- Kubernetes 1.23+
- Ubuntu 20.04+

### Setup a Kubernetes cluster
Please follow the instructions from [Kubeadm Ansible Installation](kubernetes/README.md) to setup a cluster using kubeadm.


### Install kubernetes ansible module
```shell
ansible-galaxy collection install kubernetes.core
pip3 install kubernetes
```

### Install DESK
```shell
ansible-playbook -i install-desk/hosts install-desk/main.yaml
```