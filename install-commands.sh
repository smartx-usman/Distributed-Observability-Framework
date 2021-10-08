#Create monitoring functions namespaces
kubectl apply -f namespaces/create-namespaces.yaml

#Create persistent volumes
kubectl apply -f volumes/create-persistent-volume.yaml

#Taint master node
kubectl taint nodes muhammad-vm-1 key1=value1:NoSchedule

#Prometheus
sudo mkdir /opt/prometheus #create dir on the node where prometheus will be deployed
curl https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/prometheus/values.yaml > prometheus-values.yaml
# Change prometheus-values.yaml
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install -n store prometheus -f prometheus-values.yaml prometheus-community/prometheus
#Grafana URL: http://prometheus-server.store.svc.cluster.local

#Prometheus node exporter
curl https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/prometheus-node-exporter/values.yaml > node-exporter.values.yaml
helm upgrade --install node-exporter -n measurement -f node-exporter-values.yaml prometheus-community/prometheus-node-exporter

#Kubernetes cluster metrics
curl https://raw.githubusercontent.com/prometheus-community/helm-charts/main/charts/kube-state-metrics/values.yaml > kube-state-metrics-values.yaml
helm upgrade --install kube-state-metrics -n measurement -f node-exporter-values.yaml prometheus-community/kube-state-metrics

#Grafana
sudo mkdir /opt/grafana #create dir on the vm where grafana data will be stored
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm upgrade --install -n visualization grafana -f grafana-values.yaml grafana/grafana
#kubectl get secret --namespace visualization grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
#export POD_NAME=$(kubectl get pods --namespace visualization -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
#kubectl --namespace visualization port-forward $POD_NAME 3000


#Grafan Loki for logs (server)
sudo mkdir /opt/loki #create dir on the vm where loki will be deployed
curl https://raw.githubusercontent.com/grafana/helm-charts/tempo-distributed-0.9.14/charts/loki/values.yaml > loki-values.yaml
helm upgrade --install loki -n=store -f loki-values.yaml grafana/loki
#Grafana URL: http://loki-0.loki-headless.store.svc.cluster.local:3100

#Promtail for logs (collection)
curl https://raw.githubusercontent.com/grafana/helm-charts/tempo-distributed-0.9.14/charts/promtail/values.yaml > promtail.yaml
helm upgrade --install promtail -n=measurement -f promtail.yaml grafana/promtail

#Kibana
helm install kibana --version 7.13.4 -n visualization -f kibana-values.yaml elastic/kibana
#helm install kibana -n elasticsearch -f kibana-values.yaml elastic/kibana
#kubectl -n elasticsearch port-forward svc/kibana-kibana 5601:5601

# Tempo for traces
curl https://raw.githubusercontent.com/grafana/helm-charts/main/charts/tempo/values.yaml > tempo-values.yaml
helm upgrade --install tempo -n=tracing -f tempo-values.yaml grafana/tempo
#Grafana URL: http://tempo.traces.svc.cluster.local:3100

# Open Telemetry Collector
kubectl apply -n tracing -f https://raw.githubusercontent.com/antonioberben/examples/master/opentelemetry-collector/otel.yaml
kubectl apply -n tracing -f otel-configmap.yaml