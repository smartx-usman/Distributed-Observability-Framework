#Rancher
helm install rancher rancher-latest/rancher   --namespace cattle-system   --set hostname=kubernetes-master

#Confluent Zookeeper Kafka Connect
#docker build -t usman476/aida-kafka-connect:latest .
#docker push -t usman476/aida-kafka-connect:latest
docker pull usman476/aida-kafka-connect

curl https://raw.githubusercontent.com/confluentinc/cp-helm-charts/master/values.yaml > confluent-values.yaml
#vim confluent-values.yaml
helm repo add confluentinc https://confluentinc.github.io/cp-helm-charts/
helm repo update
helm upgrade --install confluent -n delivery -f confluent-values.yaml confluentinc/cp-helm-charts
#curl 10.103.247.74:8083/connector-plugins | jq
#curl 10.103.247.74:8083/connectors | jq

#Kibana
helm install kibana --version 7.13.4 -n monitoring -f kibana-values.yaml elastic/kibana
#helm install kibana -n elasticsearch -f kibana-values.yaml elastic/kibana
#kubectl -n elasticsearch port-forward svc/kibana-kibana 5601:5601

#Fluentbit
curl https://raw.githubusercontent.com/fluent/helm-charts/main/charts/fluent-bit/values.yaml > fluentbit-values.yml
vim fluentbit-values.yml
helm repo add fluent https://fluent.github.io/helm-charts
helm upgrade --install -n measurement fluent-bit fluent/fluent-bit -f fluentbit-values.yml
#helm show values fluent/fluent-bit