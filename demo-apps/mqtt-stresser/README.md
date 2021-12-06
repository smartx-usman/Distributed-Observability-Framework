# Use Case Example
This is a use case example to create load in the Kubernetes cluster.

### Data Flow
```shell
 ---------------       ------       -------       ---------- 
| MQTT-Stresser | --> | MQTT | --> | Kafka | --> | Analysis | 
 ---------------       ------       -------       ---------- 
                       |    ^                          |
 ----------            |    |                          |
| Actuator | <----------    ----------------------------
 ----------
```

###Sources

[MQTT-Stresser](https://github.com/flaviostutz/mqtt-stresser)

[MQTT](https://github.com/t3n/helm-charts/tree/master/mosquitto)

###Installation
Create a namespace:
```shell
kubectl create namespace uc0
```

Add helm repo for MQTT and deploy:
```shell
helm repo add t3n https://storage.googleapis.com/t3n-helm-charts
helm -n uc0 upgrade --install mqtt -f mqtt-values.yaml t3n/mosquitto
```

Deploy mqtt-stresser:
```shell
kubectl apply -f -n uc0 mqtt-stresser-pod.yaml
```

