#Create telegraf user on each node in cluster
sudo useradd -M telegraf
sudo usermod -aG docker telegraf

sudo groupmod -g 1002 telegraf
sudo groupmod -g 1001 docker

# Also change permission on the file /var/lib/docker.sock

#Create monitoring functions namespaces
kubectl apply -f namespaces/create-namespaces.yaml

#Create persistent volumes
kubectl apply -f volumes/create-persistent-volume.yaml

#Taint master node
kubectl taint nodes muhammad-vm-1 key1=value1:NoSchedule

#Kafka bitnami
sudo mkdir /opt/kafka #create dir on the vm where kafka will be deployed
#curl https://raw.githubusercontent.com/bitnami/charts/master/bitnami/kafka/values.yaml > kafka-values.yaml
helm repo add bitnami https://charts.bitnami.com/bitnami
helm upgrade --install bitnami -n monitoring -f kafka-values.yaml bitnami/kafkaf

#Elasticsearch
curl https://raw.githubusercontent.com/elastic/helm-charts/7.13/elasticsearch/values.yaml > elasticsearch-values.yaml
helm repo add elastic https://helm.elastic.co
helm upgrade --install elasticsearch -n monitoring elastic/elasticsearch -f elasticsearch-values.yaml
#curl "10.152.183.134:9200/_aliases?pretty"

#Prometheus
sudo mkdir /opt/prometheus #create dir on the node where prometheus will be deployed
#curl https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/prometheus/values.yaml > prometheus-values.yaml
# Change prometheus-values.yaml
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install -n monitoring prometheus -f prometheus-values.yaml prometheus-community/prometheus
#Grafana URL: http://prometheus-server.store.svc.cluster.local

#Prometheus node exporter
#curl https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/prometheus-node-exporter/values.yaml > node-exporter.values.yaml
helm upgrade --install node-exporter -n monitoring -f node-exporter-values.yaml prometheus-community/prometheus-node-exporter

#Kubernetes cluster metrics
curl https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-state-metrics/values.yaml > kube-state-metrics-values.yaml
helm upgrade --install kube-state-metrics -n monitoring -f node-exporter-values.yaml prometheus-community/kube-state-metrics

#Grafana
sudo mkdir /opt/grafana #create dir on the vm where grafana data will be stored
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install -n monitoring grafana -f grafana-values.yaml grafana/grafana
#kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
#export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
#kubectl --namespace monitoring port-forward $POD_NAME 3000

#Prometheus datasource url (http://prometheus-server.monitoring.svc.cluster.local/)


#Grafan Loki for logs (server)
sudo mkdir /opt/loki #create dir on the vm where loki will be deployed
curl https://raw.githubusercontent.com/grafana/helm-charts/tempo-distributed-0.9.14/charts/loki/values.yaml > loki-values.yaml
helm upgrade --install loki -n=monitoring -f loki-values.yaml grafana/loki
#Grafana URL: http://loki-0.loki-headless.store.svc.cluster.local:3100

#Promtail for logs (collection)
curl https://raw.githubusercontent.com/grafana/helm-charts/promtail-3.9.1/charts/promtail/values.yaml > promtail-values.yaml
helm upgrade --install promtail -n=measurement -f promtail-values.yaml grafana/promtail

# Tempo for traces
curl https://raw.githubusercontent.com/grafana/helm-charts/main/charts/tempo/values.yaml > tempo-values.yaml
helm upgrade --install tempo -n=tracing -f tempo-values.yaml grafana/tempo
#Grafana URL: http://tempo.traces.svc.cluster.local:3100

# Open Telemetry Collector
kubectl apply -n monitoring -f https://raw.githubusercontent.com/antonioberben/examples/master/opentelemetry-collector/otel.yaml
kubectl apply -n monitoring -f otel-configmap.yaml

# Telegraf Agents
kubectl apply -f tools/telegraf/telegraf-serviceaccount.yaml
kubectl apply -n measurement -f tools/telegraf/telegraf-deployment.yaml