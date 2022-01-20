# Create a Kubernetes Cluster Using Kubeadm on Ubuntu 20.04
In this guide, we will set up a Kubernetes cluster from scratch using Ansible and Kubeadm, and then deploy a containerized Nginx application to it.

## Introduction
Kubernetes is a container orchestration system that manages containers at scale. Initially developed by Google based on its experience running containers in production, Kubernetes is open source and actively developed by a community around the world.

Kubeadm automates the installation and configuration of Kubernetes components such as the API server, Controller Manager, and Kube DNS. It does not, however, create users or handle the installation of operating-system-level dependencies and their configuration. For these preliminary tasks, it is possible to use a configuration management tool like Ansible or SaltStack. Using these tools makes creating additional clusters or recreating existing clusters much simpler and less error-prone.
## Goals
Our cluster will include the following physical/Virtual resources:
- **One Control Plane node**

    The control plane node (a node in Kubernetes refers to a server) is responsible for managing the state of the cluster. 


- **Two worker nodes**

    Worker nodes are the servers where our workloads (i.e., containerized applications and services) will run. A worker will continue to run your workload once they’re assigned to it, even if the control plane goes down once scheduling is complete. We can increase the cluster’s capacity by adding workers.

## Prerequisites
- An SSH key pair on our local Linux/macOS/BSD machine. 
- Three servers running Ubuntu 20.04 with at least 2GB RAM and 2 vCPUs each. We should be able to SSH into each server as the root user with your SSH key pair.
- Ansible should be installed on our local machine. 

## Installation Steps
**Step 1** — Set up the Ansible Inventory File

**Step 2** — Creating a on-Root User on All Remote Servers
```bash
ansible-playbook -i hosts create_user.yaml
```

**Step 3** — Installing Kubernetes’ Dependencies
```bash
ansible-playbook -i hosts install_dependencies.yaml
```

**Step 4** — Setting Up the Control Plane Node
```bash
ansible-playbook -i hosts setup_control-plane.yaml
```

**Step 5** — Setting Up the Worker Nodes
```bash
ansible-playbook -i hosts setup_worker_nodes.yaml
```

**Step 6** — Verifying the Cluster
```bash
ssh aida@control_plane_ip
```
Then execute the following command to get the status of the cluster:
```bash
kubectl get nodes 
```

**Step 7** — Running an Application on the Cluster
```bash
kubectl create deployment nginx --image=nginx
```

