# User Case Example
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

##Sources
[MQTT-Stresser](https://github.com/flaviostutz/mqtt-stresser)

[MQTT](https://github.com/t3n/helm-charts/tree/master/mosquitto)