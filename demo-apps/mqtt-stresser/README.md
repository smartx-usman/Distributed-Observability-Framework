# Use Case Example
This is a use case example to create load in the Kubernetes cluster.

## Data Flow
```shell
 --------       ------       -------       ---------- 
| Sensor | --> | MQTT | --> | Kafka | --> | Analysis | 
 --------       ------       -------       ---------- 
                 |    ^                          |
 ----------      |    |                          |
| Actuator | <---------    -----------------------
 ----------
```

## Installation
Create a namespace:
```shell
kubectl create namespace uc0
```

Add MQTT helm repo and deploy it:
```shell
helm repo add t3n https://storage.googleapis.com/t3n-helm-charts
helm -n uc0 upgrade --install mqtt -f mqtt-values.yaml t3n/mosquitto
```

<!-- 
Deploy mqtt-stresser:
```shell
kubectl apply -f -n uc0 mqtt-stresser-pod.yaml
```
-->

Deploy MQTT Producer:
```shell
kubectl apply -f -n uc0 mqtt-producer-pod.yaml
```

Deploy MQTT Subscriber and Kafka Producer:
```shell
kubectl apply -f -n uc0 mqtt-subscriber-pod.yaml
```

## Reading resources

[MQTT-Stresser](https://github.com/flaviostutz/mqtt-stresser)

[MQTT](https://github.com/t3n/helm-charts/tree/master/mosquitto)