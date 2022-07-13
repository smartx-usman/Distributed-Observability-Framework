# Flask App for Stress Testing
A set of monitoring and observability tools that are being developed for AIDA project.

### Prerequisites
- Kubernetes 1.12+
- Helm

### Installation Steps
Create a namespace:
```shell
kubectl create ns uc1
```

Deploy flask application:
```shell
kubectl apply -n uc1 -f flask.yaml
```