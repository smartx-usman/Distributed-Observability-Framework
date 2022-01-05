# Use Case Example
This is a use case example to create load in the Kubernetes cluster.

## Data Flow
```shell
 --------       ------       -------       ---------- 
| Sensor | --> | MQTT | --> | Kafka | --> | Analysis | 
 --------       ------       -------       ---------- 
                 |    ^                          |
 ----------      |    |                          |
| Actuator | <---     ----------------------------
 ----------
```

## Installation
1. Create a namespace:
```shell
kubectl create namespace uc0
```

2. Add MQTT helm repo and deploy it:
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

3. Deploy MQTT Producer:
```shell
kubectl apply -n uc0 -f mqtt-publisher-pod.yaml
```

4. Deploy MQTT Subscriber and Kafka Producer:
```shell
kubectl apply -n uc0 -f mqtt-subscriber-pod.yaml
```

5. Deploy Kafka Consumer and Faust streaming analysis application:
```shell
kubectl apply -n uc0 -f temp-analyzer-pod.yaml
```

### Reading resources about MQTT and MQTT Stresser (not used here)

[MQTT-Stresser](https://github.com/flaviostutz/mqtt-stresser)

[MQTT](https://github.com/t3n/helm-charts/tree/master/mosquitto)