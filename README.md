[![GitHub license](https://img.shields.io/github/license/smartx-usman/Distributed-Observability-Framework?logoColor=lightgrey&style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/smartx-usman/Distributed-Observability-Framework?style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/issues)
[![GitHub forks](https://img.shields.io/github/forks/smartx-usman/Distributed-Observability-Framework?style=plastic)](https://github.com/smartx-usman/Distributed-Observability-Framework/network)

# Distributed-Observability-Framework (DESK)
This repository contains a set of monitoring and observability tools that are being developed for infra, platform and applications performance observability.

### Prerequisites
- Kubernetes 1.23+
- Ubuntu 20.04+
- Identical OS user (e.g., user with name 'aida') on all the cluster nodes with root privileges

### Get the DESK Repository
```shell
git clone https://github.com/smartx-usman/Distributed-Observability-Framework.git
cd Distributed-Observability-Framework
```

### Install Required Tools for Initiating DESK Installation
```shell
sudo ./install-deps.sh
```

### Before Installing DESK
#### Setup Ansible Inventory and SSH Access
Modify [install-desk/hosts](install-desk/hosts) file to specify correct ansible_user and IP addresses of the Kubernetes cluster nodes. Also, make sure password-less SSH access is enabled to all the cluster nodes from the master node.

#### Taint Kubernetes Master Node
Set taint on the master node to avoid scheduling of pods on it. Change <master-node-name> to the actual name of the master node.
```shell
kubectl taint nodes <master-node-name> node-role.kubernetes.io/control-plane=:NoSchedule
```

#### Create Node Label
Set label on the kubernetes nodes where these monitoring services will be installed (if not already done).
```shell
kubectl label nodes observability disktype=ssd ostype=normal appstype=observability flavor=large
```

### Install DESK
Before starting the installation process, please modify 00-install-desk.yaml file to enable which services you want to install. By default, all services are disabled.
```shell
cd install-desk
ansible-playbook -i hosts 00-install-desk.yaml 
```

### Citation
This work is published in EuCNC/6G Summit'23. Please add citation:
```bibtex
@INPROCEEDINGS{10188344,
  author={Usman, Muhammad and Ferlin, Simone and Brunstrom, Anna and Taheri, Javid},
  booktitle={2023 Joint European Conference on Networks and Communications & 6G Summit (EuCNC/6G Summit)}, 
  title={DESK: Distributed Observability Framework for Edge-Based Containerized Microservices}, 
  year={2023},
  pages={617-622},
  keywords={Image edge detection;Microservice architectures;Data visualization;Integrated design;Hardware;Internet of Things;Observability;Edge Computing;Internet of Things (IoT);Microservices;Monitoring;Observability;5G/6G},
  doi={10.1109/EuCNC/6GSummit58263.2023.10188344}}
```