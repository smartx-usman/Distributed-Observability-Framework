# Use Case Example
This is a use case example to create load in the Kubernetes cluster. A single Docker image is created for all these tools. However, multiple pods are created using this Docker image to perform different functionalites.

## Data Generation and Processing Pipeline
```shell
 --------------           -------------------------------- 
| K8S Worker-1 |         |          K8S Worker-2          |          
 --------------          |--------------------------------|          
|   --------   |    1    |  -----------    2     -------  |       
|  | Sensor |  | ------> | | (topic-s) |  --->  | Kafka | |  
|   --------   |         | |           |         -------  |       
|              |         | |    MQTT   |         3  |     |
|  ----------  |    5    | |           |   4  ----------  |
| | Actuator | | <------ | | (topic-a) | <---| Analysis | | 
|  ----------  |         |  -----------       ----------  |
 --------------           -------------------------------- 
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

3. Deploy simulated value generator and MQTT Publisher:
```shell
kubectl apply -n uc0 -f publisher/mqtt-publisher-pod.yaml
```

4. Deploy MQTT Subscriber and Kafka Producer:
```shell
kubectl apply -n uc0 -f subscriber/mqtt-subscriber-pod.yaml
```

5. Deploy Kafka Consumer and Faust streaming analysis application:
```shell
kubectl apply -n uc0 -f analyzer/temp-analyzer-pod.yaml
```

6. Deploy actuator to read actions from MQTT:
```shell
kubectl apply -n uc0 -f actuator/temp-actuator-pod.yaml
```

## Parameters Description
| Name                       | Description                                                | Default value                                                     |
|:---------------------------|:-----------------------------------------------------------|:------------------------------------------------------------------|
| `MQTT_BROKER`              | MQTT broker address.                                       | mqtt-mosquitto.uc0.svc.cluster.local                              |
| `MQTT_BROKER_PORT`         | MQTT broker port.                                          | 1883                                                              |
| `MQTT_SENSOR_TOPIC`        | MQTT topic for sending generated data by Sensor.           | mqtt/temperature/readings                                         |
| `MQTT_ACTUATOR_TOPIC`      | MQTT topic for sending actions from Analyzer.              | mqtt/temperature/actions                                          |
| `KAFKA_BROKER`             | Kafka broker address.                                      | bitnami-kafka-0.bitnami-kafka-headless.uc0.svc.cluster.local:9092 |
| `KAFKA_TOPIC`              | Kafka topic for sending generated data by MQTT Subscriber. | temperature-readings                                              |
| `SENSORS`                  | Number of threads to start generating sensor data.         | 1                                                                 | 
| `MESSAGE_DELAY`            | Delay between generating sensor data.                      | 1                                                                 |
| `START_VALUE`              | Generated data value start range.                          | 1                                                                 |
| `END_VALUE`                | Generated data value end range.                            | 10                                                                |
| `VALUE_TYPE`               | Generated data value type.                                 | integer                                                           |
| `INVALID_VALUE_OCCURRENCE` | Invalid value occurence frequency.                         | 10                                                                |
| `INVALID_VALUE`            | Invalid value to be added to generated data.               | 99                                                                |


### Reading resources about MQTT and MQTT Stresser (not used here)

[MQTT-Stresser](https://github.com/flaviostutz/mqtt-stresser)

[MQTT](https://github.com/t3n/helm-charts/tree/master/mosquitto)