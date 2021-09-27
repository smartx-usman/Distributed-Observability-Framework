#Rancher
helm install rancher rancher-latest/rancher   --namespace cattle-system   --set hostname=kubernetes-master

#Kafka bitnami
sudo mkdir /opt/kafka #create dir on the vm where kafka will be deployed
curl https://raw.githubusercontent.com/bitnami/charts/master/bitnami/kafka/values.yaml > kafka-values.yaml
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install bitnami -n delivery -f kafka-values.yaml bitnami/kafka

#Confluent Zookeeper Kafka Connect
#docker build -t usman476/aida-kafka-connect:latest .
#docker push -t usman476/aida-kafka-connect:latest
docker pull usman476/aida-kafka-connect

curl https://raw.githubusercontent.com/confluentinc/cp-helm-charts/master/values.yaml > confluent-values.yaml
#vim confluent-values.yaml
helm repo add confluentinc https://confluentinc.github.io/cp-helm-charts/
helm repo update
helm install confluent -n kafka -f confluent-values.yaml confluentinc/cp-helm-charts
#curl 10.152.183.30:8083/connector-plugins | jq
#curl 10.152.183.30:8083/connectors | jq

#Elasticsearch
curl https://raw.githubusercontent.com/elastic/helm-charts/7.13/elasticsearch/values.yaml > elasticsearch-values.yaml
helm repo add elastic https://helm.elastic.co
helm install elasticsearch -n elasticsearch elastic/elasticsearch -f elasticsearch-values.yaml
#curl "10.152.183.134:9200/_aliases?pretty"

#Fluentbit
curl https://raw.githubusercontent.com/fluent/helm-charts/main/charts/fluent-bit/values.yaml > fluentbit-values.yml
vim fluentbit-values.yml
helm repo add fluent https://fluent.github.io/helm-charts
helm upgrade --install -n measurement fluent-bit fluent/fluent-bit -f fluentbit-values.yml
#helm show values fluent/fluent-bit