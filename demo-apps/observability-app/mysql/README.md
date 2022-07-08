# MySQL Stress Testing
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
helm upgrade --install mysql -n=uc1 -f mysql-values.yaml bitnami/mysql
```

Deploy stress testing application:
```shell
kubectl apply -n uc1 -f pod.yaml
```