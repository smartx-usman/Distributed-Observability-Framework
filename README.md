# IIoT-Edge-Observability
Set of monitoring and observability tools developed for AIDA project.

### Setup a Kubernetes cluster
```shell
./kubernetes/create-kubernetes-cluster.sh
```

### Install Helm package manager
```shell
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get -y update
sudo apt-get -y install helm
```

### Deploy monitoring/observability functions
```shell
sudo mkdir /opt/elasticsearch
sudo chown -R user:user /opt/elasticsearch  #Replace user with real username
```