# Flask App for Stress Testing
A set of monitoring and observability tools that are being developed for AIDA project.

### Prerequisites
- Kubernetes 1.12+
- Helm

### Installation Steps
How to bild docker image on macOS (not required as image exists in DockerHub):
```
docker buildx build --platform linux/amd64,linux/arm64 --push -t usman476/mqtt-kafka-faust:latest .
```

Create a namespace:
```shell
kubectl create ns uc1
```

Deploy flask application:
```shell
kubectl apply -n uc1 -f flask.yaml
```