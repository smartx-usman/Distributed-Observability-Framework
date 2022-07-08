# Cassandra Stress Testing
A set of monitoring and observability tools that are being developed for AIDA project.

### Prerequisites
- Kubernetes 1.12+
- Helm

### Installation Steps
Create a namespace:
```shell
kubectl create ns uc1
```

Add Cassandra helm repo and deploy it:
```shell
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install cassandra -n=uc1 -f cassandra-values.yaml bitnami/cassandra
```

Deploy stress testing application:
```shell
kubectl apply -n uc1 -f pod.yaml
```