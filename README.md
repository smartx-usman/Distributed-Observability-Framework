# AIDA-Distributed-Observability-Framework
A set of monitoring and observability tools that are being developed for AIDA project.

### Setup a Kubernetes cluster
Please follow the instructions from [Kubeadm Ansible Installation](kubernetes/README.md).


### Install kubernetes ansible module
```shell
ansible-galaxy collection install kubernetes.core
```

### Install DESK
```shell
ansible-playbook -i install-desk/hosts install-desk/main.yaml
```


### Deprecated Instructions (will be removed in next release)
#### Install Helm package manager
```shell
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
sudo apt-get install apt-transport-https --yes
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get -y update
sudo apt-get -y install helm
```

#### Create required namespaces
```shell
kubectl apply -f namespaces/create-namespaces.yaml
```

#### Create required persistent volumes
```shell
kubectl apply -f persistent-volumes/create-persistent-volume.yaml 
```

#### Create required directories for persistent volumes
```shell
sudo mkdir /opt/elasticsearch /opt/kafka /opt/grafana /opt/loki /opt/prometheus
sudo chown -R aida:aida /opt/*  #Replace user with real username
```

#### Install Zookeeper and Kafka via Helm
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install bitnami -n observability -f helm-configs/kafka-values.yaml bitnami/kafka
```

#### Install Elasticsearch via Helm
```shell
helm repo add elastic https://helm.elastic.co
helm upgrade --install elasticsearch -n observability elastic/elasticsearch -f helm-configs/elasticsearch-values.yaml
```

#### Install Grafana via Helm
```shell
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install -n observability grafana -f helm-configs/grafana-values.yaml grafana/grafana
#kubectl --namespace observability port-forward $POD_NAME 3000
```

#### Install Loki via Helm
```shell
helm upgrade --install loki -n=observability -f helm-configs/loki-values.yaml grafana/loki --version 2.16.0
```

#### Install Tempo via Helm
```shell
helm upgrade --install tempo -n=observability -f helm-configs/tempo-values.yaml grafana/tempo
```

#### Install otel collector via Kubectl
```shell
kubectl apply -n observability -f helm-configs/otel-collector.yaml
#kubectl apply -n observability -f helm-configs/otel-configmap.yaml
```

#### Install Prometheus via Helm
```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade --install -n observability prometheus -f helm-configs/prometheus-values.yaml prometheus-community/prometheus
```

#### Install Jaeger via Helm
````shell
# ES version 8 is not yet supported by Jaeger, so manually create index templates. they are located in extras directory. 
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm upgrade --install -n observability  jaeger jaegertracing/jaeger -f helm-configs/jaeger-values.yaml
#kubectl port-forward --namespace observability jaeger-query-74978f8888-qkgcj 16686:16686 --address 0.0.0.0
````

#### Install Promtail via Helm
```shell
helm upgrade --install promtail -n=measurement -f helm-configs/promtail-values.yaml grafana/promtail
```

#### Install Telegraf via Kubectl
```shell
kubectl apply -f tools/telegraf/telegraf-serviceaccount.yaml
kubectl apply -n measurement -f tools/telegraf/telegraf-ds-worker.yaml
kubectl apply -n measurement -f tools/telegraf/telegraf-ds-master.yaml
```

#### Install Kafka consumer via Kubectl
```shell
kubectl apply -f tools/kafka-consumers/kc-nm-deployment.yaml
```